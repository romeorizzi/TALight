mod problem;
mod proto;
mod util;

use clap::Clap;
use log::{error, info, warn};
use proto::{Command, Packet};
use sha2::{Digest, Sha512};
use std::collections::HashMap;
use std::fs::{canonicalize, read_dir, read_to_string};
use std::net::TcpListener;
use std::net::TcpStream;
use std::path::PathBuf;
use std::process;
use std::process::{exit, Stdio};
use std::thread::spawn;
use tungstenite::error::Error;
use tungstenite::error::Error::ConnectionClosed;
use tungstenite::handshake::server::{ErrorResponse, Request, Response};
use tungstenite::protocol::WebSocket;
use tungstenite::Message::{Binary, Text};

#[derive(Clap)]
#[clap(name = "Rust Turing Arena Light Server")]
struct CliArgs {
    #[clap(short, long, about = "Problems root directory", default_value = ".")]
    directory: PathBuf,
    #[clap(short, long, about = "Bind address", default_value = "127.0.0.1")]
    bind_address: String,
    #[clap(short('p'), long, about = "Listen port", default_value = "8080")]
    listen_port: u16,
    #[clap(short, long, about = "Connection timeout (in seconds)", default_value = "60")]
    timeout: f64,
}

fn handle_connection(ws: &mut WebSocket<TcpStream>, mut evaluator: PathBuf, args: HashMap<String, String>, timeout_ms: u64) {
    let mut eval = process::Command::new(&evaluator);
    let process_name = evaluator.to_str().unwrap_or("NULL".into()).to_string();
    evaluator.pop();
    eval.current_dir(evaluator);
    for (argname, argvalue) in args {
        eval.env("TAL_".to_string() + &argname, argvalue);
    }
    eval.stdin(Stdio::piped());
    eval.stdout(Stdio::piped());
    match eval.spawn() {
        Ok(x) => util::connect_process(ws, x, false, timeout_ms),
        Err(x) => fail!("Cannot spawn evaluator process {}: {}", process_name, x),
    };
}

fn main() {
    pretty_env_logger::init();
    let opts = CliArgs::parse();
    let listener = match TcpListener::bind((opts.bind_address.as_str(), opts.listen_port)) {
        Ok(x) => x,
        Err(x) => crash!("Cannot listen on [{}:{}]: {}", opts.bind_address, opts.listen_port, x),
    };
    let dir_abs = match canonicalize(&opts.directory) {
        Ok(x) => x,
        Err(x) => crash!("Cannot obtain absolute path of {}: {}", opts.directory.to_str().unwrap_or("NULL"), x),
    };
    let timeout_ms = (opts.timeout * 1000.0) as u64;
    info!("Rust Turing Arena Light up and running!");
    for client in listener.incoming() {
        let directory = dir_abs.clone();
        spawn(move || {
            let client = match client {
                Ok(x) => x,
                Err(x) => fail!("Error on incoming connection: {}", x),
            };
            let mut address = match client.peer_addr() {
                Ok(x) => format!("{:?}", x),
                Err(_) => String::from("NULL"),
            };
            let header_cb = |request: &Request, response: Response| -> Result<Response, ErrorResponse> {
                if let Some(x) = request.headers().get("x-forwarded-for") {
                    if let Ok(x) = x.to_str() {
                        address = x.to_string();
                    }
                }
                Ok(response)
            };
            let mut client = match tungstenite::server::accept_hdr(client, header_cb) {
                Ok(x) => x,
                Err(x) => fail!("Error on WebSocket negotiation: {}", x),
            };
            info!("[{}] Client connected", address);
            loop {
                let msg = match client.read_message() {
                    Ok(x) => x,
                    Err(ConnectionClosed) => {
                        info!("[{}] Connection closed", address);
                        return;
                    }
                    Err(x) => fail!("[{}] Error in received message: {}", address, x),
                };
                match msg {
                    Text(x) => {
                        let msg = match serde_json::from_str::<proto::Packet>(&x) {
                            Ok(x) => x,
                            Err(x) => fail!("[{}] Invalid JSON sent: {}", address, x),
                        };
                        let response = if !msg.valid() {
                            Packet::new(Command::WrongMagic)
                        } else {
                            Packet::new(match msg.command {
                                Command::ListRequest => {
                                    let mut dirs = proto::ListResponse::default();
                                    if let Ok(reader) = read_dir(&directory) {
                                        for entry in reader {
                                            let dir = match entry {
                                                Ok(x) => x,
                                                Err(_) => continue,
                                            };
                                            if let Ok(metadata) = dir.metadata() {
                                                if metadata.is_dir() {
                                                    let mut meta = dir.path();
                                                    meta.push(problem::META);
                                                    let problem = match read_to_string(&meta) {
                                                        Ok(x) => x,
                                                        Err(x) => {
                                                            warn!("Error while opening {:?}: {}", &meta, x);
                                                            continue;
                                                        }
                                                    };
                                                    let problem = match serde_yaml::from_str::<problem::Meta>(&problem) {
                                                        Ok(x) => x,
                                                        Err(x) => {
                                                            warn!("{:?} is not a valid {} file: {}", meta, problem::META, x);
                                                            continue;
                                                        }
                                                    };
                                                    dirs.problems.push(proto::Problem::from(&problem));
                                                }
                                            }
                                        }
                                    } else {
                                        fail!("[{}] Cannot read file system", address);
                                    }
                                    Command::ListResponse(dirs)
                                }
                                Command::ConnectionRequest(req) if req.codename.contains("..") => Command::ConnectionDenied("Invalid problem codename".into()),
                                Command::ConnectionRequest(req) => {
                                    let mut directory = directory.clone();
                                    directory.push(req.codename);
                                    let mut evaluator = directory.clone();
                                    directory.push(problem::META);
                                    match read_to_string(&directory) {
                                        Ok(x) => {
                                            let meta = match serde_yaml::from_str::<problem::Meta>(&x) {
                                                Ok(x) => x,
                                                Err(x) => fail!("[{}] Requested invalid problem: {}", address, x),
                                            };
                                            if let Some(service) = meta.services.get(&req.service) {
                                                evaluator.push(&service.evaluator);
                                                let mut error = None;
                                                let mut args: HashMap<String, String> = HashMap::new();
                                                if let Some(meta_args) = &service.args {
                                                    for (argname, argstruct) in meta_args {
                                                        if let Some(cval) = req.args.get(argname) {
                                                            if argstruct.regex.is_match(cval) {
                                                                args.insert(argname.into(), cval.into());
                                                            } else {
                                                                error = Some(format!("{} is not a valid value for parameter {}", cval, argname))
                                                            }
                                                        } else {
                                                            args.insert(argname.into(), argstruct.default.clone());
                                                        }
                                                    }
                                                }
                                                if let Some(error) = error {
                                                    Command::ConnectionDenied(error)
                                                } else {
                                                    let response = match serde_json::to_string(&Packet::new(Command::ConnectionBegin)) {
                                                        Ok(x) => x,
                                                        Err(x) => fail!("[{}] Error crafting response: {}", address, x),
                                                    };
                                                    match client.write_message(Text(response)) {
                                                        Ok(()) => {}
                                                        Err(x) => fail!("[{}] Error sending response: {}", address, x),
                                                    };
                                                    match client.write_pending() {
                                                        Ok(()) => {}
                                                        Err(x) => fail!("[{}] Error flushing response: {}", address, x),
                                                    };
                                                    info!("[{}] Connection began with problem \"{}\", service \"{}\"", address, meta.codename, req.service);
                                                    handle_connection(&mut client, evaluator, args, timeout_ms);
                                                    break;
                                                }
                                            } else {
                                                Command::ConnectionDenied("No such service".into())
                                            }
                                        }
                                        Err(_) => Command::ConnectionDenied("Invalid problem codename".into()),
                                    }
                                }
                                Command::AttachmentRequest(req) if req.contains("..") => Command::AttachmentDenied("Invalid problem codename".into()),
                                Command::AttachmentRequest(req) => {
                                    let mut directory = directory.clone();
                                    directory.push(req);
                                    let mut att = directory.clone();
                                    directory.push(problem::META);
                                    match read_to_string(&directory) {
                                        Ok(x) => {
                                            let meta = match serde_yaml::from_str::<problem::Meta>(&x) {
                                                Ok(x) => x,
                                                Err(x) => fail!("[{}] Requested invalid problem: {}", address, x),
                                            };
                                            att.push(meta.public_folder);
                                            let mut archive = tar::Builder::new(Vec::new());
                                            let attpath = att.to_str().unwrap_or("NULL").to_string();
                                            match archive.append_dir_all(meta.codename, att) {
                                                Ok(()) => {}
                                                Err(x) => fail!("[{}] Error while creating archive from {}: {}", address, attpath, x),
                                            };
                                            let archive = match archive.into_inner() {
                                                Ok(x) => x,
                                                Err(x) => fail!("[{}] Error while creating archive from {}: {}", address, attpath, x),
                                            };
                                            let hash = format!("{:x}", Sha512::digest(&archive));
                                            let response = match serde_json::to_string(&Packet::new(Command::AttachmentBegin(hash))) {
                                                Ok(x) => x,
                                                Err(x) => fail!("[{}] Error crafting response: {}", address, x),
                                            };
                                            match client.write_message(Text(response)) {
                                                Ok(()) => {}
                                                Err(x) => fail!("[{}] Error sending response: {}", address, x),
                                            };
                                            match client.write_pending() {
                                                Ok(()) => {}
                                                Err(x) => fail!("[{}] Error flushing response: {}", address, x),
                                            };
                                            match client.write_message(Binary(archive)) {
                                                Ok(()) => {}
                                                Err(x) => fail!("[{}] Error while sending attachment: {}", address, x),
                                            };
                                            break;
                                        }
                                        Err(_) => Command::AttachmentDenied("Invalid problem codename".into()),
                                    }
                                }
                                _ => Command::InvalidCommand,
                            })
                        };
                        let response = match serde_json::to_string(&response) {
                            Ok(x) => x,
                            Err(x) => fail!("[{}] Error crafting response: {}", address, x),
                        };
                        match client.write_message(Text(response)) {
                            Ok(()) => {}
                            Err(x) => fail!("[{}] Error sending response: {}", address, x),
                        };
                    }
                    _ => {}
                };
            }
            const ERROR_STRING: &str = "Connection closed abruptly";
            match client.close(None) {
                Ok(()) => {}
                Err(Error::AlreadyClosed) | Err(Error::ConnectionClosed) => {}
                Err(x) => fail!("{}: {}", ERROR_STRING, x),
            }
            loop {
                match client.write_pending() {
                    Ok(()) => {}
                    Err(Error::AlreadyClosed) | Err(Error::ConnectionClosed) => break,
                    Err(x) => fail!("{}: {}", ERROR_STRING, x),
                }
                match client.read_message() {
                    Ok(_) => {}
                    Err(Error::AlreadyClosed) | Err(Error::ConnectionClosed) => break,
                    Err(x) => fail!("{}: {}", ERROR_STRING, x),
                }
            }
            info!("[{}] Connection closed", address);
        });
    }
}
