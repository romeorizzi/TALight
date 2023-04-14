mod connection;
mod master;
mod problem;
mod proto;
mod util;

use clap::Parser;
use std::path::PathBuf;
use tokio::runtime::Runtime;
use tracing::error;

#[derive(Parser, Debug, Clone)]
#[clap(version)]
struct CliArgs {
    #[clap(short, long, help = "Problems root directory", default_value = ".")]
    directory: PathBuf,
    #[clap(short, long, help = "Bind address", default_value = "127.0.0.1")]
    bind_address: String,
    #[clap(short('p'), long, help = "Listen port", default_value = "8008")]
    listen_port: u16,
    #[clap(
        short,
        long,
        help = "Connection timeout (in seconds)",
        default_value = "60"
    )]
    timeout: f64,
    #[clap(short, long, help = "Authentication data file")]
    authentication: Option<PathBuf>,
    #[clap(short = 'x', long, help = "Accept only authenticated connections")]
    only_auth: bool,
    #[cfg(unix)]
    #[clap(short, long, help = "Use bind address as a Unix Domain Socket")]
    unix_domain_socket: bool,
}

fn main() {
    let args = CliArgs::parse();
    tracing_subscriber::fmt::init();
    match Runtime::new() {
        Ok(rt) => rt.block_on(async move { master::start(args).await }),
        Err(x) => error!("Cannot create tokio runtime: {}", x),
    };
}
