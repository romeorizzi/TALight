#![cfg(python)]
#[allow(dead_code)]
mod problem;
mod proto;
#[allow(dead_code)]
mod util;

use proto::{Reply, Request};
use pyo3::exceptions::PyRuntimeError as PRE;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use pythonize::pythonize;
use std::collections::{HashMap, HashSet};
use std::net::TcpStream;
use tracing::warn;
use tungstenite::{connect, stream::MaybeTlsStream, Message, WebSocket};
use twox_hash::xxh3::hash128;
use util::{BinaryDataHeader, BUFFER_SIZE};

fn oneshot_request(
    request: Request,
    ws: &mut WebSocket<MaybeTlsStream<TcpStream>>,
) -> Result<Reply, String> {
    let request = match Request::forge(&request) {
        Ok(x) => Message::Text(x),
        Err(x) => return Err(format!("Cannot forge request: {}", x)),
    };
    if let Err(x) = ws.write_message(request) {
        return Err(format!("Cannot send request: {}", x));
    };
    loop {
        match ws.read_message() {
            Ok(Message::Text(x)) => match Reply::parse(&x) {
                Ok(x) => break Ok(x),
                Err(x) => break Err(format!("Could not parse server reply: {}", x)),
            },
            Err(x) => break Err(format!("Connection lost while waiting for reply: {}", x)),
            Ok(_) => {}
        }
    }
}

fn oneshot_reply(ws: &mut WebSocket<MaybeTlsStream<TcpStream>>) -> Result<Reply, String> {
    loop {
        match ws.read_message() {
            Ok(Message::Text(x)) => match Reply::parse(&x) {
                Ok(x) => break Ok(x),
                Err(x) => break Err(format!("Could not parse server reply: {}", x)),
            },
            Err(x) => break Err(format!("Connection lost while waiting for reply: {}", x)),
            Ok(_) => {}
        }
    }
}

fn send_binary_data(
    ws: &mut WebSocket<MaybeTlsStream<TcpStream>>,
    name: &str,
    data: &[u8],
) -> Result<(), String> {
    let header = BinaryDataHeader {
        name: name.to_string(),
        size: data.len(),
        hash: hash128(data),
    };
    let serialized_header = match serde_json::to_string(&header) {
        Ok(x) => x,
        Err(x) => return Err(format!("Cannot serialize binary header: {}", x)),
    };
    if let Err(x) = ws.write_message(Message::Text(serialized_header)) {
        return Err(format!("Cannot send binary header: {}", x));
    }
    for offset in (0..data.len()).step_by(BUFFER_SIZE) {
        let slice = &data[offset..data.len().min(offset + BUFFER_SIZE)];
        if let Err(x) = ws.write_message(Message::Binary(slice.to_vec())) {
            return Err(format!("Cannot send binary data: {}", x));
        }
    }
    Ok(())
}

fn recv_binary_data(
    ws: &mut WebSocket<MaybeTlsStream<TcpStream>>,
) -> Result<(String, Vec<u8>), String> {
    let header = loop {
        match ws.read_message() {
            Ok(Message::Text(x)) => break x,
            Ok(_) => continue,
            Err(x) => return Err(format!("Error while receiving binary header: {}", x)),
        }
    };
    let header = match serde_json::from_str::<BinaryDataHeader>(&header) {
        Ok(x) => x,
        Err(x) => return Err(format!("Received invalid binary header: {}", x)),
    };
    let mut buffer = Vec::new();
    loop {
        if buffer.len() >= header.size {
            break;
        }
        let mut data = match ws.read_message() {
            Ok(Message::Binary(x)) => x,
            Ok(_) => continue,
            Err(x) => return Err(format!("Error while receiving binary data: {}", x)),
        };
        buffer.append(&mut data);
    }
    if hash128(&buffer) != header.hash {
        return Err(format!("Received corrupted binary data"));
    }
    Ok((header.name, buffer))
}

#[pyclass]
struct RTAL {
    ws: WebSocket<MaybeTlsStream<TcpStream>>,
    url: String,
}

#[pyclass]
struct RTALConn {
    rtal: RTAL,
    output: Option<HashMap<String, Vec<u8>>>,
}

impl RTALConn {
    fn handle_close(&mut self, files: Vec<String>) -> Result<(), String> {
        let mut result = HashMap::new();
        for _ in 0..files.len() {
            let (name, data) = recv_binary_data(&mut self.rtal.ws)?;
            result.insert(name, data);
        }
        self.output = Some(result);
        Ok(())
    }
}

#[pymethods]
impl RTALConn {
    fn write(&mut self, data: &[u8]) -> PyResult<()> {
        if let Err(x) = self.rtal.ws.write_message(Message::Binary(data.to_vec())) {
            return Err(PRE::new_err(format!("Cannot send data: {}", x)));
        }
        Ok(())
    }

    fn read<'p>(&mut self, py: Python<'p>) -> PyResult<Option<&'p PyBytes>> {
        loop {
            break match self.rtal.ws.read_message() {
                Ok(Message::Binary(x)) => Ok(Some(PyBytes::new(py, &x))),
                Ok(Message::Text(x)) => match Reply::parse(&x) {
                    Ok(Reply::ConnectStop { status }) => match status {
                        Ok(x) => {
                            let client_ended = Request::ConnectStop {};
                            let client_ended = match client_ended.forge() {
                                Ok(x) => x,
                                Err(x) => {
                                    return Err(PRE::new_err(format!(
                                        "Cannot forge request: {}",
                                        x
                                    )))
                                }
                            };
                            if let Err(x) = self.rtal.ws.write_message(Message::Text(client_ended))
                            {
                                return Err(PRE::new_err(format!("Cannot send request: {}", x)));
                            }
                            self.handle_close(x).map_err(|x| PRE::new_err(x))?;
                            return Ok(None);
                        }
                        Err(x) => Err(PRE::new_err(format!("Error on the server: {}", x))),
                    },
                    Ok(_) => Err(PRE::new_err("Unexpected reply from server")),
                    Err(x) => Err(PRE::new_err(format!("Cannot parse reply: {}", x))),
                },
                Ok(_) => continue,
                Err(x) => Err(PRE::new_err(format!("Cannot read data: {}", x))),
            };
        }
    }

    fn close<'p>(&mut self, py: Python<'p>) -> PyResult<HashMap<String, &'p PyBytes>> {
        if let Some(ref output) = self.output {
            let mut result = HashMap::new();
            for (name, data) in output.iter() {
                result.insert(name.clone(), PyBytes::new(py, data));
            }
            return Ok(result);
        }
        let client_ended = Request::ConnectStop {};
        let client_ended = match client_ended.forge() {
            Ok(x) => x,
            Err(x) => return Err(PRE::new_err(format!("Cannot forge request: {}", x))),
        };
        if let Err(x) = self.rtal.ws.write_message(Message::Text(client_ended)) {
            return Err(PRE::new_err(format!("Cannot send request: {}", x)));
        }
        loop {
            break match self.rtal.ws.read_message() {
                Ok(Message::Text(x)) => match Reply::parse(&x) {
                    Ok(Reply::ConnectStop { status }) => match status {
                        Ok(x) => self.handle_close(x).map_err(|x| PRE::new_err(x))?,
                        Err(x) => return Err(PRE::new_err(format!("Error on the server: {}", x))),
                    },
                    Ok(_) => return Err(PRE::new_err("Unexpected reply from server")),
                    Err(x) => return Err(PRE::new_err(format!("Cannot parse reply: {}", x))),
                },
                Ok(_) => continue,
                Err(x) => return Err(PRE::new_err(format!("Cannot read data: {}", x))),
            };
        }
        self.close(py)
    }
}

#[pymethods]
impl RTAL {
    #[args(
        args = "HashMap::new()",
        tty = "false",
        token = "None",
        files = "HashMap::new()"
    )]
    fn connect(
        &self,
        problem: &str,
        service: &str,
        args: HashMap<String, String>,
        tty: bool,
        token: Option<String>,
        files: HashMap<String, Vec<u8>>,
    ) -> PyResult<RTALConn> {
        let mut rtal = RTAL::new(&self.url)?;
        let request = Request::ConnectBegin {
            problem: problem.into(),
            service: service.into(),
            args: args.into_iter().collect(),
            tty: tty,
            token: token,
            files: files.keys().cloned().collect(),
        };
        let allowed_files =
            match oneshot_request(request, &mut rtal.ws).map_err(|x| PRE::new_err(x))? {
                Reply::ConnectBegin { status: Ok(x) } => x,
                Reply::ConnectBegin { status: Err(x) } => {
                    return Err(PRE::new_err(format!("Cannot connect: {}", x)))
                }
                _ => return Err(PRE::new_err(format!("Server sent an invalid response"))),
            };
        let provided_files = files;
        let allowed_files: HashSet<_> = allowed_files.into_iter().collect();
        let mut to_upload = Vec::new();
        for (name, data) in provided_files {
            if !allowed_files.contains(&name) {
                return Err(PRE::new_err(format!("File \"{}\" is not allowed", &name)));
            }
            to_upload.push((name, data));
        }
        for (name, data) in to_upload {
            if let Err(x) = send_binary_data(&mut rtal.ws, &name, &data) {
                return Err(PRE::new_err(format!("Cannot send input file: {}", x)));
            }
        }
        match oneshot_reply(&mut rtal.ws).map_err(|x| PRE::new_err(x))? {
            Reply::ConnectStart { status: Ok(()) } => {}
            Reply::ConnectStart { status: Err(x) } => {
                return Err(PRE::new_err(format!("Cannot start connection: {}", x)))
            }
            _ => return Err(PRE::new_err(format!("Server sent an invalid response"))),
        };
        Ok(RTALConn { rtal, output: None })
    }

    fn list(&mut self, py: Python<'_>) -> PyResult<PyObject> {
        let meta = match oneshot_request(Request::MetaList {}, &mut self.ws)
            .map_err(|x| PRE::new_err(x))?
        {
            Reply::MetaList { meta } => meta,
            _ => return Err(PRE::new_err("Unexpected reply")),
        };
        Ok(pythonize(py, &meta)?)
    }

    fn get<'p>(&mut self, problem: &str, py: Python<'p>) -> PyResult<(String, &'p PyBytes)> {
        let request = Request::Attachment {
            problem: problem.into(),
        };
        match oneshot_request(request, &mut self.ws).map_err(|x| PRE::new_err(x))? {
            Reply::Attachment { status: Ok(()) } => {}
            Reply::Attachment { status: Err(x) } => {
                return Err(PRE::new_err(format!("Cannot download attachment: {}", x)))
            }
            _ => return Err(PRE::new_err(format!("Server sent an invalid response"))),
        };
        let (name, data) = match recv_binary_data(&mut self.ws) {
            Ok(x) => x,
            Err(x) => {
                return Err(PRE::new_err(format!(
                    "Error while downloading the attachment: {}",
                    x
                )))
            }
        };
        Ok((name, PyBytes::new(py, &data)))
    }

    #[new]
    #[args(url = "\"ws://127.0.0.1:8008/\"")]
    fn new(url: &str) -> PyResult<RTAL> {
        let (mut ws, _) = connect(url).map_err(|x| PRE::new_err(x.to_string()))?;
        if let Err(x) = match ws.get_mut() {
            &mut MaybeTlsStream::Plain(ref mut x) => x.set_nodelay(true),
            &mut MaybeTlsStream::Rustls(ref mut x) => x.get_mut().set_nodelay(true),
            &mut _ => unreachable!("Using stream other than Plain or Rustls"),
        } {
            warn!("Failed to set nodelay: {}", x);
        }
        let handshake_request = match Request::forge(&Request::Handshake {
            magic: proto::MAGIC.to_string(),
            version: proto::VERSION,
        }) {
            Ok(x) => Message::Text(x),
            Err(x) => {
                return Err(PRE::new_err(format!(
                    "Cannot forge handshake request: {}",
                    x
                )))
            }
        };
        if let Err(x) = ws.write_message(handshake_request) {
            return Err(PRE::new_err(format!(
                "Cannot send handshake request: {}",
                x
            )));
        };
        let handshake_reply = loop {
            match ws.read_message() {
                Ok(Message::Text(x)) => match Reply::parse(&x) {
                    Ok(Reply::Handshake { magic, version }) => break (magic, version),
                    Ok(_) => {
                        return Err(PRE::new_err(format!("Server performed a wrong handshake")))
                    }
                    Err(x) => {
                        return Err(PRE::new_err(format!(
                            "Could not parse server handshake: {}",
                            x
                        )))
                    }
                },
                Err(x) => {
                    return Err(PRE::new_err(format!(
                        "Connection lost while performing handshake: {}",
                        x
                    )))
                }
                Ok(_) => {}
            }
        };
        if !(handshake_reply.0 == proto::MAGIC && handshake_reply.1 == proto::VERSION) {
            return if handshake_reply.0 == proto::MAGIC {
                Err(PRE::new_err(format!(
                    "Protocol version mismatch: local={}, server={}",
                    proto::VERSION,
                    handshake_reply.1
                )))
            } else {
                Err(PRE::new_err(format!(
                    "\"{}\" is not a Turing Arena Light server",
                    url
                )))
            };
        }
        Ok(RTAL {
            ws,
            url: url.into(),
        })
    }
}

#[pymodule]
fn pyrtal(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<RTAL>()?;
    Ok(())
}
