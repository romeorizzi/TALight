#![allow(dead_code)]

mod problem;
mod proto;
mod util;

use clap::Clap;
use fwdansi::write_ansi;
use log::{error, info};
use regex::Regex;
use rustls::{ClientSession, StreamOwned};
use sha2::{Digest, Sha512};
use std::collections::HashMap;
use std::fs;
use std::io::{self, ErrorKind, Read, Write};
use std::net::{TcpStream, ToSocketAddrs};
use std::process::{self, exit, Stdio};
use std::sync::Arc;
use termcolor::{ColorChoice, StandardStream};
use tungstenite::stream::Stream;
use tungstenite::{error, Message, WebSocket};
use url::{Origin, Url};

#[derive(Clap, Debug)]
struct CliArgs {
    #[clap(short, long, about = "Server URL", default_value = "ws://127.0.0.1:8080/")]
    server: String,
    #[clap(subcommand)]
    subcommand: SubCommand,
}

#[derive(Clap, Debug)]
enum SubCommand {
    #[clap(about = "List available problems")]
    List(ListCommand),
    #[clap(about = "Connect to problem evaluator")]
    Connect(ConnectCommand),
    #[clap(about = "Download problem attachments")]
    Get(GetCommand),
}

#[derive(Clap, Debug)]
struct ListCommand {
    #[clap(about = "Filter problems with a regex")]
    filter: Option<Regex>,
    #[clap(short, long, parse(from_occurrences), about = "List services and parameters, add more than one to list more information")]
    verbose: u8,
}

#[derive(Clap, Debug)]
struct ConnectCommand {
    #[clap(short, long, about = "Echo messages on console")]
    echo: bool,
    #[clap(short, long, about = "Connection timeout (in seconds)", default_value = "3600")]
    timeout: f64,
    #[clap(about = "Remote problem to connect to")]
    problem: String,
    #[clap(about = "Service wanted", default_value = "solve")]
    service: String,
    #[clap(short('a'), long, multiple = true, number_of_values = 1, about = "Service arguments, can be specified multiple times with -a arg=val")]
    service_args: Vec<String>,
    #[clap(about = "Local executable and executable arguments", raw = true)]
    program: Vec<String>,
}

#[derive(Clap, Debug)]
struct GetCommand {
    #[clap(about = "Name of the problem to download the attachments")]
    problem: String,
    #[clap(short, long, about = "Path to output the attachments [default: <problemname>.tar]")]
    output: Option<String>,
}

struct ColorStdout {
    stream: StandardStream,
}

impl Write for ColorStdout {
    fn write(&mut self, data: &[u8]) -> io::Result<usize> {
        write_ansi(&mut self.stream, data).map(|_| data.len())
    }

    fn flush(&mut self) -> io::Result<()> {
        self.stream.flush()
    }
}

fn main() {
    pretty_env_logger::init();
    let opts = CliArgs::parse();
    let url = match Url::parse(&opts.server) {
        Ok(x) => x,
        Err(x) => crash!("{} is not a valid URL: {}", &opts.server, x),
    };
    let mut ws = match url.origin() {
        Origin::Opaque(_) => crash!("{} is not a valid URL", url),
        Origin::Tuple(proto, host, port) => match proto.as_str() {
            "ws" | "wss" => {
                let addrs = match (host.to_string(), port).to_socket_addrs() {
                    Ok(x) => x,
                    Err(x) => crash!("DNS resolve error: {}", x),
                };
                let mut sock = None;
                for addr in addrs {
                    if let Ok(s) = TcpStream::connect(addr) {
                        sock = Some(s);
                        break;
                    };
                }
                let sock = match sock {
                    Some(x) => x,
                    None => crash!("Cannot connect to {}", url),
                };
                let ws = match proto.as_str() {
                    "ws" => tungstenite::client::client::<Stream<TcpStream, StreamOwned<ClientSession, TcpStream>>, Url>(url, Stream::Plain(sock)),
                    "wss" => {
                        let mut config = rustls::ClientConfig::new();
                        config.root_store.add_server_trust_anchors(&webpki_roots::TLS_SERVER_ROOTS);
                        let shost = host.to_string();
                        let domain = match webpki::DNSNameRef::try_from_ascii_str(&shost) {
                            Ok(x) => x,
                            Err(x) => crash!("{} is not a valid ASCII domain: {}", host, x),
                        };
                        let client = rustls::ClientSession::new(&Arc::new(config), domain);
                        let stream = StreamOwned::new(client, sock);
                        tungstenite::client::client::<Stream<TcpStream, StreamOwned<ClientSession, TcpStream>>, Url>(url, Stream::Tls(stream))
                    }
                    _ => unreachable!(),
                };
                match ws {
                    Ok(x) => x.0,
                    Err(x) => crash!("Connection failed: {}", x),
                }
            }
            _ => crash!("{} is not a valid protocol", proto),
        },
    };
    match opts.subcommand {
        SubCommand::List(mut cmd) => {
            let res = match send_and_wait(&mut ws, proto::Command::ListRequest) {
                proto::Command::ListResponse(x) => x,
                _ => crash!("Invalid response for problem list request"),
            };
            cmd.verbose += if cmd.filter.is_some() { 1 } else { 0 };
            for problem in res.problems {
                if let Some(filter) = &cmd.filter {
                    if !filter.is_match(&problem.codename) {
                        continue;
                    }
                }
                println!("- {}", problem.codename);
                if cmd.verbose >= 1 {
                    for (servname, servargs) in problem.services {
                        println!("  * {}", servname);
                        if let Some(args) = servargs.args {
                            for (argname, arg) in args {
                                if cmd.verbose >= 2 {
                                    println!("    # {} [{}] {{ {} }}", argname, arg.default, arg.regex);
                                } else {
                                    println!("    # {} [{}]", argname, arg.default);
                                }
                            }
                        }
                    }
                }
            }
        }
        SubCommand::Connect(cmd) => {
            let mut args: HashMap<String, String> = HashMap::new();
            for arg in cmd.service_args {
                let sarg: Vec<_> = arg.split("=").collect();
                if sarg.len() != 2 {
                    crash!("Incorrect format for service argument \"{}\"", arg);
                }
                args.insert(sarg[0].into(), sarg[1].into());
            }
            let request = proto::Command::ConnectionRequest(proto::ConnectionRequest {
                codename: cmd.problem,
                service: cmd.service,
                args: args,
                isatty: cmd.program.len() == 0,
            });
            match send_and_wait(&mut ws, request) {
                proto::Command::ConnectionBegin => {}
                proto::Command::ConnectionDenied(x) => crash!("Connection denied: {}", x),
                _ => crash!("Invalid response for connect request"),
            };
            info!("Connection established!");
            if cmd.program.len() > 0 {
                let mut program = process::Command::new(&cmd.program[0]);
                for i in 1..cmd.program.len() {
                    program.arg(&cmd.program[i]);
                }
                program.stdout(Stdio::piped());
                program.stdin(Stdio::piped());
                match program.spawn() {
                    Ok(x) => util::connect_process(&mut ws, x, cmd.echo, (cmd.timeout * 1000.0) as u64),
                    Err(x) => crash!("Cannot spawn {}: {}", &cmd.program[0], x),
                };
            } else {
                let stdin = std::io::stdin();
                let stdout = StandardStream::stdout(ColorChoice::Auto);
                util::connect_streams(&mut ws, stdin, stdout, false, (cmd.timeout * 1000.0) as u64);
            }
        }
        SubCommand::Get(cmd) => {
            let output = cmd.output.unwrap_or(cmd.problem.clone() + ".tar");
            let hash = match send_and_wait(&mut ws, proto::Command::AttachmentRequest(cmd.problem)) {
                proto::Command::AttachmentBegin(x) => x,
                proto::Command::AttachmentDenied(x) => crash!("Request denied: {}", x),
                _ => crash!("Invalid response for problem list request"),
            };
            let mut buffer = Vec::new();
            loop {
                let response = match ws.read_message() {
                    Ok(x) => x,
                    Err(error::Error::AlreadyClosed) | Err(error::Error::ConnectionClosed) => break,
                    Err(error::Error::Io(x)) if x.kind() == ErrorKind::ConnectionAborted => break,
                    Err(x) => crash!("Cannot receive response: {}", x),
                };
                match response {
                    Message::Binary(mut x) => buffer.append(&mut x),
                    _ => continue,
                }
            }
            if format!("{:x}", Sha512::digest(&buffer)) != hash {
                crash!("Received corrupted attachment!");
            }
            match fs::write(&output, buffer) {
                Ok(()) => {}
                Err(x) => crash!("Couldn't write {}: {}", output, x),
            };
        }
    };
    close_connection(ws);
}

fn prepare_message(msg: proto::Command) -> Message {
    let raw = match serde_json::to_string(&proto::Packet::new(msg)) {
        Ok(x) => x,
        Err(x) => crash!("Cannot craft command: {}", x),
    };
    Message::Text(raw)
}

fn send_and_wait<T: Read + Write>(ws: &mut WebSocket<T>, msg: proto::Command) -> proto::Command {
    let msg = prepare_message(msg);
    match ws.write_message(msg) {
        Ok(()) => {}
        Err(x) => crash!("Cannot send command: {}", x),
    };
    let response = loop {
        let response = match ws.read_message() {
            Ok(x) => x,
            Err(x) => crash!("Cannot receive response: {}", x),
        };
        match response {
            Message::Text(x) => break x,
            _ => continue,
        }
    };
    let response = match serde_json::from_str::<proto::Packet>(&response) {
        Ok(x) => x,
        Err(x) => crash!("Cannot decode response: {}", x),
    };
    match response.command {
        proto::Command::WrongMagic => crash!("Wrong protocol version, make sure the client and server are of the same version"),
        proto::Command::InvalidCommand => crash!("Invalid command sent"),
        _ => response.command,
    }
}

fn close_connection<T: Read + Write>(mut ws: WebSocket<T>) {
    const ERROR_STRING: &str = "Connection closed abruptly";
    match ws.close(None) {
        Ok(()) => {}
        Err(error::Error::AlreadyClosed) | Err(error::Error::ConnectionClosed) => {}
        Err(error::Error::Io(x)) if x.kind() == ErrorKind::ConnectionAborted => {}
        Err(x) => crash!("{}: {}", ERROR_STRING, x),
    }
    loop {
        match ws.write_pending() {
            Ok(()) => {}
            Err(error::Error::AlreadyClosed) | Err(error::Error::ConnectionClosed) => break,
            Err(error::Error::Io(x)) if x.kind() == ErrorKind::ConnectionAborted => break,
            Err(x) => crash!("{}: {}", ERROR_STRING, x),
        }
        match ws.read_message() {
            Ok(_) => {}
            Err(error::Error::AlreadyClosed) | Err(error::Error::ConnectionClosed) => break,
            Err(error::Error::Io(x)) if x.kind() == ErrorKind::ConnectionAborted => break,
            Err(x) => crash!("{}: {}", ERROR_STRING, x),
        }
    }
}
