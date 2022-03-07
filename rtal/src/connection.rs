use crate::problem::{load, load_all_meta, Problem, Service};
use crate::proto::{self, Reply, Request};
use crate::util::{recv_binary_data, send_binary_data};
use crate::CliArgs;
use futures_util::sink::Sink;
use futures_util::stream::Stream;
use futures_util::{SinkExt, StreamExt};
use path_absolutize::Absolutize;
use sanitize_filename::sanitize;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::fmt::Display;
use std::path::{Path, PathBuf};
use std::process::Stdio;
use tempfile::tempdir;
use tokio::io::{AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt};
use tokio::process::Command;
use tokio::select;
use tokio::time::{timeout, Duration};
use tokio_tungstenite::tungstenite::protocol::Message;
use tokio_tungstenite::tungstenite::Error as TsError;
use tokio_tungstenite::WebSocketStream;
use tracing::{error, info, instrument, warn};

const PING_TIMEOUT: f64 = 25.0;
const BUFFER_SIZE: usize = 1 << 16;

#[derive(Debug)]
pub(crate) struct Client<T: AsyncRead + AsyncWrite + Unpin> {
    ws: WebSocketStream<T>,
    args: CliArgs,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct AuthData {
    tokens: Vec<String>,
    save_directory: PathBuf,
}

impl AuthData {
    pub async fn load(path: &Path) -> Result<AuthData, String> {
        let file = match tokio::fs::read(path).await {
            Ok(x) => x,
            Err(x) => return Err(format!("Auth file missing: {}", x)),
        };
        let auth: AuthData = match serde_yaml::from_slice(&file) {
            Ok(x) => x,
            Err(x) => return Err(format!("Cannot parse auth file: {}", x)),
        };
        Ok(auth)
    }
}

#[derive(Debug, Clone)]
struct TokenInfo {
    token: String,
    path: PathBuf,
}

macro_rules! wsrecv {
    ($wsin:expr) => {{
        timeout(Duration::from_secs_f64(PING_TIMEOUT), $wsin.next())
    }};
}

macro_rules! wssend {
    ($out:expr, $reply:expr) => {{
        let msg = match Reply::forge(&$reply) {
            Ok(x) => x,
            Err(x) => {
                error!("Cannot forge reply: {}", x);
                break;
            }
        };
        if let Err(x) = $out.send(Message::Text(msg)).await {
            warn!("Cannot send reply: {}", x);
            break;
        }
    }};
}

macro_rules! wssend2 {
    ($out:expr, $reply:expr) => {{
        let msg = match Reply::forge(&$reply) {
            Ok(x) => x,
            Err(x) => {
                return Err(format!("Cannot forge reply: {}", x));
            }
        };
        if let Err(x) = $out.send(Message::Text(msg)).await {
            return Err(format!("Cannot send reply: {}", x));
        }
    }};
}

macro_rules! handle_ping {
    ($msg:expr, $wsout:expr) => {{
        match $msg {
            Ok(x) => x,
            Err(_) => match $wsout.send(Message::Ping(Vec::new())).await {
                Ok(()) => continue,
                Err(x) => {
                    error!("Cannot send ping: {}", x);
                    break;
                }
            },
        }
    }};
}

macro_rules! reunite {
    ($field:expr, $in:expr, $out:expr) => {
        $field = match $in.reunite($out) {
            Ok(x) => x,
            Err(x) => {
                error!("Could not reunite streams: {}", x);
                return;
            }
        };
    };
}

impl<T: AsyncRead + AsyncWrite + Unpin> Client<T> {
    pub fn new(ws: WebSocketStream<T>, args: CliArgs) -> Client<T> {
        Client { ws, args }
    }

    #[instrument(name = "client", skip(self))]
    pub async fn start(mut self, address: &str) {
        info!("Client connected");
        self.args.directory = match self.args.directory.absolutize() {
            Ok(x) => x.into(),
            Err(x) => {
                error!("Cannot absolutize problems directory: {}", x);
                self.args.directory
            }
        };
        let (mut wsout, mut wsin) = self.ws.split();
        loop {
            let msg = wsrecv!(wsin).await;
            let msg = match handle_ping!(msg, wsout) {
                Some(x) => x,
                None => break,
            };
            match msg {
                Ok(Message::Text(msg)) => match Request::parse(&msg) {
                    Ok(Request::Handshake { magic, version }) => {
                        match Reply::forge(&Reply::Handshake {
                            magic: proto::MAGIC.to_string(),
                            version: proto::VERSION,
                        }) {
                            Ok(msg) => {
                                if let Err(x) = wsout.send(Message::Text(msg)).await {
                                    warn!("Cannot send reply: {}", x);
                                } else if magic == proto::MAGIC && version == proto::VERSION {
                                    reunite!(self.ws, wsin, wsout);
                                    return self.main().await;
                                }
                            }
                            Err(x) => error!("Cannot forge handshake reply: {}", x),
                        }
                    }
                    Ok(_) => warn!("Wrong message while handshaking"),
                    Err(x) => warn!("Invalid request from client: {}", x),
                },
                Err(x) => warn!("Connection error: {}", x),
                _ => continue,
            }
            break;
        }
        reunite!(self.ws, wsin, wsout);
        return self.stop().await;
    }

    async fn main(mut self) {
        let (mut wsout, mut wsin) = self.ws.split();
        'req: loop {
            let msg = match handle_ping!(wsrecv!(wsin).await, wsout) {
                Some(Ok(Message::Text(x))) => x,
                Some(Ok(_)) => continue,
                Some(Err(x)) => {
                    warn!("Connection error: {}", x);
                    break;
                }
                None => break,
            };
            let req = match Request::parse(&msg) {
                Ok(x) => x,
                Err(x) => {
                    warn!("Invalid request from client: {}", x);
                    break;
                }
            };
            match req {
                Request::MetaList {} => wssend!(
                    wsout,
                    Reply::MetaList {
                        meta: load_all_meta(&self.args.directory).await
                    }
                ),
                Request::Attachment { problem } => {
                    let problem = sanitize(problem);
                    let meta = match load(&self.args.directory, &problem).await {
                        Some(x) => x,
                        None => {
                            wssend!(
                                wsout,
                                Reply::Attachment {
                                    status: Err(format!("Problem \"{}\" does not exists", problem))
                                }
                            );
                            continue;
                        }
                    };
                    let mut folder = meta.root.clone();
                    folder.push(meta.meta.public_folder);
                    let mut tar = tokio_tar::Builder::new(Vec::new());
                    if let Err(x) = tar.append_dir_all(&problem, &folder).await {
                        error!("Cannot open {:?}: {}", &folder, x);
                        break;
                    }
                    let tar = match tar.into_inner().await {
                        Ok(x) => x,
                        Err(x) => {
                            error!("Cannot create tar for {}: {}", problem, x);
                            break;
                        }
                    };
                    wssend!(wsout, Reply::Attachment { status: Ok(()) });
                    if let Err(x) =
                        send_binary_data(&mut wsout, &format!("{}.tar", problem), &tar).await
                    {
                        warn!("Cannot send attachment of problem {}: {}", problem, x);
                        break;
                    }
                }
                Request::ConnectBegin {
                    problem,
                    service,
                    args,
                    tty,
                    token,
                    files,
                } => {
                    let problem = sanitize(problem);
                    let problem = match load(&self.args.directory, &problem).await {
                        Some(x) => x,
                        None => {
                            wssend!(
                                wsout,
                                Reply::ConnectBegin {
                                    status: Err(format!("Problem {} does not exists", problem))
                                }
                            );
                            continue;
                        }
                    };
                    let service_name = service.clone();
                    let service = match problem.meta.services.get(&service) {
                        Some(x) => x.clone(),
                        None => {
                            wssend!(
                                wsout,
                                Reply::ConnectBegin {
                                    status: Err(format!(
                                        "Problem {} does not have a {} service",
                                        problem.name, service
                                    ))
                                }
                            );
                            continue;
                        }
                    };
                    let mut sargs = HashMap::new();
                    if let Some(ref fargs) = service.args {
                        for (fk, fv) in fargs {
                            if let Some(uv) = args.get(fk) {
                                if fv.regex.is_match(uv) {
                                    sargs.insert(fk.clone(), uv.clone());
                                } else {
                                    wssend!(
                                        wsout,
                                        Reply::ConnectBegin {
                                            status: Err(format!(
                                                "{} is not a valid value for argument {}",
                                                uv, fk
                                            ))
                                        }
                                    );
                                    continue 'req;
                                }
                            } else if let Some(ref dv) = fv.default {
                                sargs.insert(fk.clone(), dv.clone());
                            } else {
                                wssend!(
                                    wsout,
                                    Reply::ConnectBegin {
                                        status: Err(format!(
                                            "You must supply a value for argument {}",
                                            fk
                                        ))
                                    }
                                );
                                continue 'req;
                            }
                        }
                    }
                    let mut tinfo = None;
                    if let Some(t) = token {
                        if let Some(ref auth) = self.args.authentication {
                            let auth = match AuthData::load(auth).await {
                                Ok(x) => x,
                                Err(x) => {
                                    error!("{}", x);
                                    break;
                                }
                            };
                            if !auth.tokens.into_iter().any(|x| x == t) {
                                wssend!(
                                    wsout,
                                    Reply::ConnectBegin {
                                        status: Err(format!("Invalid token"))
                                    }
                                );
                                continue;
                            }
                            let log_path = match auth.save_directory.absolutize() {
                                Ok(x) => x,
                                Err(x) => {
                                    error!("Cannot absolutize save directory: {}", x);
                                    break;
                                }
                            };
                            tinfo = Some(TokenInfo {
                                token: t,
                                path: log_path.into(),
                            });
                        }
                    } else if self.args.only_auth {
                        wssend!(
                            wsout,
                            Reply::ConnectBegin {
                                status: Err(format!("You must send your authentication token"))
                            }
                        );
                        continue;
                    }
                    wssend!(
                        wsout,
                        Reply::ConnectBegin {
                            status: Ok(service.files.clone().unwrap_or(Vec::new()))
                        }
                    );
                    if let Err(x) = Self::connect(
                        &mut wsin,
                        &mut wsout,
                        problem,
                        service,
                        service_name,
                        sargs,
                        tty,
                        tinfo,
                        self.args.timeout,
                        files,
                    )
                    .await
                    {
                        error!("Connect failed: {}", x);
                        break;
                    }
                }
                _ => {
                    warn!("Request not valid for current state: {:?}", req);
                    break;
                }
            };
        }
        reunite!(self.ws, wsin, wsout);
        return self.stop().await;
    }

    async fn connect<X: Sink<Message> + Unpin, Y: Stream<Item = Result<Message, TsError>> + Unpin>(
        wsin: &mut Y,
        wsout: &mut X,
        problem: Problem,
        service: Service,
        service_name: String,
        args: HashMap<String, String>,
        tty: bool,
        token_info: Option<TokenInfo>,
        conn_timeout: f64,
        declared_files: Vec<String>,
    ) -> Result<(), String>
    where
        <X as Sink<Message>>::Error: Display,
    {
        let infile_dir = match tempdir() {
            Ok(x) => x,
            Err(x) => return Err(format!("Cannot create temporary directory: {}", x)),
        };
        let outfile_dir = match tempdir() {
            Ok(x) => x,
            Err(x) => return Err(format!("Cannot create temporary directory: {}", x)),
        };
        let logfile_dir = match tempdir() {
            Ok(x) => x,
            Err(x) => return Err(format!("Cannot create temporary directory: {}", x)),
        };
        let mut difference = Vec::new();
        let declared_files: HashSet<_> = declared_files.into_iter().collect();
        if let Some(filenames) = service.files {
            let filenames: HashSet<_> = filenames.into_iter().collect();
            let mut received = HashSet::new();
            for _ in 0..declared_files.len() {
                let (name, data) = match recv_binary_data(wsin).await {
                    Ok(x) => x,
                    Err(x) => return Err(x),
                };
                let name = sanitize(name);
                if let Err(x) = tokio::fs::write(infile_dir.path().join(&name), data).await {
                    return Err(format!("Cannot write received file: {}", x));
                }
                received.insert(name);
            }
            difference = received.difference(&filenames).cloned().collect();
        }
        if difference.len() > 0 {
            wssend2!(
                wsout,
                Reply::ConnectStart {
                    status: Err(format!("The following files are invalid: {:?}", difference))
                }
            );
            return Ok(());
        }
        if service.evaluator.len() == 0 {
            return Err(format!(
                "Evaluator for problem {} service {} has no program",
                problem.name, service_name
            ));
        }
        let mut evaluator = Command::new(&service.evaluator[0]);
        evaluator.current_dir(&problem.root);
        if service.evaluator.len() > 1 {
            evaluator.args(&service.evaluator[1..]);
        }
        for (k, v) in args {
            evaluator.env(format!("TAL_{}", k), v);
        }
        evaluator.env("TAL_META_DIR", &problem.root);
        evaluator.env("TAL_META_CODENAME", &problem.name);
        evaluator.env("TAL_META_SERVICE", &service_name);
        evaluator.env("TAL_META_TTY", if tty { "1" } else { "0" });
        evaluator.env("TAL_META_INPUT_FILES", infile_dir.path());
        evaluator.env("TAL_META_OUTPUT_FILES", outfile_dir.path());
        if token_info.is_some() {
            evaluator.env("TAL_META_LOG_FILES", logfile_dir.path());
        }
        if let Some(ref token_info) = token_info {
            evaluator.env("TAL_META_EXP_TOKEN", &token_info.token);
            evaluator.env("TAL_META_EXP_LOG_DIR", &token_info.path);
        }
        evaluator.stdin(Stdio::piped());
        evaluator.stdout(Stdio::piped());
        let mut process = match evaluator.spawn() {
            Ok(x) => x,
            Err(x) => return Err(format!("Cannot spawn process: {}", x)),
        };
        let mut ev_stdin = process.stdin.take();
        let mut ev_stdout = match process.stdout.take() {
            Some(x) => x,
            None => return Err(format!("Child born without a stdout channel")),
        };
        let mut ev_stdout_ignore = false;
        wssend2!(wsout, Reply::ConnectStart { status: Ok(()) });
        let mut client_closed = false;
        let mut buffer = [0; BUFFER_SIZE];
        let mut out_files = Vec::new();
        let mut log_files = Vec::new();
        loop {
            select! {
                msg = timeout(Duration::from_secs_f64(conn_timeout), wsrecv!(wsin)) => {
                    let msg = match msg {
                        Ok(x) => x,
                        Err(_) => {
                            warn!("Connection timed out");
                            return Ok(());
                        }
                    };
                    let msg = match handle_ping!(msg, wsout) {
                        Some(Ok(Message::Binary(x))) => x,
                        Some(Ok(Message::Text(x))) => match Request::parse(&x) {
                            Ok(Request::ConnectStop {}) => {
                                ev_stdin = None;
                                ev_stdout_ignore = true;
                                client_closed = true;
                                continue;
                            }
                            Ok(_) => {
                                warn!("Invalid command sent");
                                return Ok(());
                            }
                            Err(x) => return Err(format!("Cannot parse request: {}", x)),
                        }
                        Some(Ok(_)) => continue,
                        Some(Err(x)) => return Err(format!("{}", x)),
                        None => return Ok(()),
                    };
                    if let Some(ref mut stdin) = ev_stdin {
                        if let Err(x) = stdin.write_all(&msg).await {
                            return Err(format!("Cannot write to process stdin: {}", x));
                        }
                    }
                }
                size = ev_stdout.read(&mut buffer) => {
                    let size = match size {
                        Ok(x) => x,
                        Err(x) => return Err(format!("Pipe closed by evaluator process: {}", x)),
                    };
                    if ev_stdout_ignore {
                        continue;
                    }
                    if let Err(x) = wsout.send(Message::Binary(buffer[..size].into())).await {
                        warn!("Lost connection while communicating: {}", x);
                        return Ok(());
                    }
                }
                status = process.wait() => {
                    let status = match status {
                        Ok(x) => x,
                        Err(x) => return Err(format!("Cannot get exit status of evaluator process: {}", x)),
                    };
                    if !status.success() {
                        wssend2!(wsout, Reply::ConnectStop {status: Err(format!("Evaluator crashed"))});
                        return Err(format!("Evaluator crashed"));
                    }
                    let mut dir = match tokio::fs::read_dir(outfile_dir.path()).await {
                        Ok(x) => x,
                        Err(x) => return Err(format!("Output file directory is no longer accessible: {}", x)),
                    };
                    while let Ok(Some(file)) = dir.next_entry().await {
                        let data = match tokio::fs::read(file.path()).await {
                            Ok(x) => x,
                            Err(x) => {
                                error!("Cannot read {:?}: {}", file.path(), x);
                                continue;
                            }
                        };
                        let name = match file.file_name().into_string() {
                            Ok(x) => x,
                            Err(x) => {
                                error!("Cannot convert {:?} to string", x);
                                continue;
                            }
                        };
                        out_files.push((name, data));
                    }
                    let mut dir = match tokio::fs::read_dir(logfile_dir.path()).await {
                        Ok(x) => x,
                        Err(x) => return Err(format!("Log file directory is no longer accessible: {}", x)),
                    };
                    while let Ok(Some(file)) = dir.next_entry().await {
                        let data = match tokio::fs::read(file.path()).await {
                            Ok(x) => x,
                            Err(x) => {
                                error!("Cannot read {:?}: {}", file.path(), x);
                                continue;
                            }
                        };
                        let name = match file.file_name().into_string() {
                            Ok(x) => x,
                            Err(x) => {
                                error!("Cannot convert {:?} to string", x);
                                continue;
                            }
                        };
                        log_files.push((name, data));
                    }
                    let file_names = out_files.iter().map(|x| x.0.clone()).collect();
                    wssend2!(wsout, Reply::ConnectStop { status: Ok(file_names) });
                    while !client_closed {
                        let msg = match handle_ping!(wsrecv!(wsin).await, wsout) {
                            Some(Ok(Message::Text(x))) => x,
                            Some(Ok(_)) => continue,
                            Some(Err(x)) => return Err(format!("Connection error: {}", x)),
                            None => return Ok(()),
                        };
                        let req = match Request::parse(&msg) {
                            Ok(x) => x,
                            Err(x) => {
                                warn!("Invalid request from client: {}", x);
                                return Ok(());
                            }
                        };
                        match req {
                            Request::ConnectStop {} => client_closed = true,
                            _ => {
                                warn!("Invalid client request");
                                return Ok(());
                            }
                        };
                    }
                    break;
                }
            }
        }
        if let Some(mut info) = token_info {
            let time = chrono::Local::now();
            let timestamp = time.format("%Y-%m-%d_%H-%M-%S_%3f");
            let dirname = format!("{}+{}", info.token, timestamp);
            info.path.push(dirname);
            if let Err(x) = tokio::fs::create_dir_all(&info.path).await {
                return Err(format!("Cannot create directory {:?}: {}", info.path, x));
            }
            for (name, data) in log_files {
                let path = info.path.join(name);
                if let Err(x) = tokio::fs::write(&path, data).await {
                    return Err(format!("Cannot write {:?}: {}", path, x));
                }
            }
        }
        for (name, data) in out_files {
            send_binary_data(wsout, &name, &data).await?;
        }
        Ok(())
    }

    async fn stop(mut self) {
        match self.ws.close(None).await {
            Ok(()) | Err(TsError::ConnectionClosed) => info!("Client disconnected"),
            Err(x) => warn!("Could not close connection gracefully: {}", x),
        }
    }
}
