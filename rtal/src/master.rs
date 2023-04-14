use crate::connection::Client;
use crate::CliArgs;
use std::error::Error;
use tokio::io::{AsyncRead, AsyncWrite};
use tokio::net::TcpListener;
use tokio::spawn;
use tokio_tungstenite::accept_hdr_async;
use tokio_tungstenite::tungstenite::handshake::server as tuns;
use tracing::{error, info, warn};

#[cfg(unix)]
use {
    nix::{
        sys::stat::{umask, Mode},
        unistd::unlink,
    },
    tokio::net::UnixListener,
};

async fn handle_raw_socket<T: AsyncRead + AsyncWrite + Unpin>(
    socket: T,
    mut address: String,
    args: CliArgs,
) {
    let headers_callback = |request: &tuns::Request,
                            response: tuns::Response|
     -> Result<tuns::Response, tuns::ErrorResponse> {
        if let Some(x) = request.headers().get("x-forwarded-for") {
            if let Ok(x) = x.to_str() {
                address = x.to_string();
            }
        }
        Ok(response)
    };
    let websocket = match accept_hdr_async(socket, headers_callback).await {
        Ok(x) => x,
        Err(x) => {
            warn!(address = address.as_str(), "Cannot start connection: {}", x);
            return;
        }
    };
    let client = Client::new(websocket, args, &address);
    client.start(&address).await;
}

async fn tcp_listener(args: CliArgs) -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind((args.bind_address.clone(), args.listen_port)).await?;
    info!("Server up and running!");
    loop {
        let args = args.clone();
        let incoming_connection = listener.accept().await;
        spawn(async move {
            let (socket, addr) = match incoming_connection {
                Ok(x) => x,
                Err(x) => {
                    warn!("Connection refused: {}", x);
                    return;
                }
            };
            let address = format!("{}", addr);
            if let Err(x) = socket.set_nodelay(true) {
                warn!(address = address.as_str(), "Cannot set TCP_NODELAY: {}", x);
            }
            handle_raw_socket(socket, address, args).await;
        });
    }
}

#[cfg(unix)]
async fn uds_listener(args: CliArgs) -> Result<(), Box<dyn Error>> {
    umask(Mode::empty());
    drop(unlink(args.bind_address.as_str()));
    let listener = UnixListener::bind(args.bind_address.clone())?;
    info!("Server up and running!");
    loop {
        let args = args.clone();
        let incoming_connection = listener.accept().await;
        spawn(async move {
            let (socket, addr) = match incoming_connection {
                Ok(x) => x,
                Err(x) => {
                    warn!("Connection refused: {}", x);
                    return;
                }
            };
            handle_raw_socket(socket, format!("{:?}", addr), args).await;
        });
    }
}

pub(crate) async fn start(args: CliArgs) {
    if let Some(ref auth) = args.authentication {
        if let Err(x) = crate::connection::AuthData::load(auth).await {
            warn!("Authentication data {:?} not available: {}", auth, x);
        }
    }
    #[cfg(unix)]
    let result = if args.unix_domain_socket {
        uds_listener(args).await
    } else {
        tcp_listener(args).await
    };
    #[cfg(not(unix))]
    let result = tcp_listener(args).await;
    match result {
        Ok(()) => {}
        Err(x) => error!("Fatal error: {}", x),
    };
}
