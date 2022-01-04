use crate::fail;
use log::error;
use rustls::{ClientSession, StreamOwned};
use std::io::ErrorKind;
use std::io::Read;
use std::io::Write;
use std::net::TcpStream;
use std::process;
use std::sync::mpsc::{self, TryRecvError};
use std::thread::spawn;
use std::time::Duration;
use std::time::Instant;
use termcolor::{Color, ColorChoice, ColorSpec, StandardStream, WriteColor};
use tungstenite::error::Error::Io;
use tungstenite::protocol::WebSocket;
use tungstenite::stream::Stream;
use tungstenite::Message::Binary;

const TICK_DURATION_MS: u64 = 10;
const BUFFER_SIZE: usize = 1 << 20;

pub trait StreamOp {
    fn set_read_timeout(&mut self, dur: Option<Duration>) -> std::io::Result<()>;
    fn set_nodelay(&mut self, toggle: bool) -> std::io::Result<()>;
}

impl StreamOp for TcpStream {
    fn set_read_timeout(&mut self, dur: Option<Duration>) -> std::io::Result<()> {
        TcpStream::set_read_timeout(self, dur)
    }
    fn set_nodelay(&mut self, toggle: bool) -> std::io::Result<()> {
        TcpStream::set_nodelay(self, toggle)
    }
}

impl StreamOp for Stream<TcpStream, StreamOwned<ClientSession, TcpStream>> {
    fn set_read_timeout(&mut self, dur: Option<Duration>) -> std::io::Result<()> {
        match &mut *self {
            Stream::Plain(x) => x.set_read_timeout(dur),
            Stream::Tls(x) => x.get_mut().set_read_timeout(dur),
        }
    }
    fn set_nodelay(&mut self, toggle: bool) -> std::io::Result<()> {
        match &mut *self {
            Stream::Plain(x) => TcpStream::set_nodelay(x, toggle),
            Stream::Tls(x) => TcpStream::set_nodelay(x.get_mut(), toggle),
        }
    }
}

fn ignore_result<T, E>(_: Result<T, E>) {}

macro_rules! cwrite {
    ($stream:expr, $color:expr, $($arg:tt)+) => {
        {
            ignore_result($stream.set_color(ColorSpec::new().set_bold(true).set_fg(Some($color))));
            ignore_result(write!(&mut $stream, $($arg)+));
            ignore_result($stream.set_color(ColorSpec::new().set_bold(false).set_fg(None)));
        }
    }
}

pub fn connect_streams<T: Read + Write + StreamOp, R: 'static + Read + Send, W: Write>(ws: &mut WebSocket<T>, mut pout: R, mut pin: W, echo: bool, timeout_ms: u64) {
    let mut stdout = StandardStream::stdout(ColorChoice::Auto);
    match ws.get_mut().set_read_timeout(Some(Duration::from_millis(TICK_DURATION_MS))) {
        Ok(()) => {}
        Err(x) => fail!("Cannot set_read_timeout: {}", x),
    };
    match ws.get_mut().set_nodelay(true) {
        Ok(()) => {}
        Err(x) => fail!("Cannot set_nodelay: {}", x),
    };
    let (tx, rx) = mpsc::channel();
    spawn(move || {
        let mut buffer = vec![0_u8; BUFFER_SIZE];
        while let Ok(size) = pout.read(&mut buffer) {
            if size == 0 {
                break;
            }
            match tx.send(buffer[..size].to_vec()) {
                Ok(()) => {}
                Err(_) => break,
            };
        }
    });
    let mut start = Instant::now();
    loop {
        let msg = match ws.read_message() {
            Ok(x) => x,
            Err(Io(x)) if x.kind() == ErrorKind::WouldBlock || x.kind() == ErrorKind::TimedOut => {
                if Instant::now().duration_since(start) >= Duration::from_millis(timeout_ms) {
                    break;
                }
                match rx.try_recv() {
                    Err(TryRecvError::Empty) => continue,
                    Err(TryRecvError::Disconnected) => break,
                    Ok(x) => {
                        start = Instant::now();
                        if echo {
                            cwrite!(stdout, Color::Green, "{}", String::from_utf8_lossy(&x));
                        }
                        match ws.write_message(Binary(x)) {
                            Ok(()) => continue,
                            Err(_) => break,
                        }
                    }
                }
            }
            Err(_) => break,
        };
        match msg {
            Binary(x) => {
                start = Instant::now();
                if echo {
                    cwrite!(stdout, Color::Yellow, "{}", String::from_utf8_lossy(&x));
                }
                match pin.write_all(&x) {
                    Ok(()) => continue,
                    Err(_) => break,
                };
            }
            _ => {}
        };
    }
    match ws.get_mut().set_read_timeout(None) {
        Ok(()) => {}
        Err(x) => fail!("Cannot set_read_timeout: {}", x),
    };
    match ws.get_mut().set_nodelay(false) {
        Ok(()) => {}
        Err(x) => fail!("Cannot set_nodelay: {}", x),
    };
}

pub fn connect_process<T: Read + Write + StreamOp>(ws: &mut WebSocket<T>, mut ps: process::Child, echo: bool, timeout_ms: u64) {
    let stdin = match ps.stdin.take() {
        Some(x) => x,
        None => fail!("Cannot take control of stdin"),
    };
    let stdout = match ps.stdout.take() {
        Some(x) => x,
        None => fail!("Cannot take control of stdout"),
    };
    connect_streams(ws, stdout, stdin, echo, timeout_ms);
    match ps.kill() {
        _ => {}
    }
    match ps.wait() {
        _ => {}
    }
}

#[macro_export]
macro_rules! crash {
    ($($arg:tt)+) => {
        {
            error!($($arg)+);
            exit(1)
        }
    }
}

#[macro_export]
macro_rules! fail {
    ($($arg:tt)+) => {
        {
            error!($($arg)+);
            return;
        }
    }
}
