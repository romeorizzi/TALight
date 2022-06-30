#[allow(dead_code)]
mod problem;
mod proto;

use proto::{Reply, Request};
use pyo3::exceptions::PyRuntimeError as PRE;
use pyo3::prelude::*;
use std::net::TcpStream;
use tracing::warn;
use tungstenite::{connect, stream::MaybeTlsStream, Message, WebSocket};

#[pyclass]
struct RTAL {
    ws: WebSocket<MaybeTlsStream<TcpStream>>,
}

#[pymethods]
impl RTAL {
    #[new]
    #[args(url = "\"ws://127.0.0.1/\"")]
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
        Ok(RTAL { ws })
    }
}

#[pymodule]
fn pyrtal(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<RTAL>()?;
    Ok(())
}
