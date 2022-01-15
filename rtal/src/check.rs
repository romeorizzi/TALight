#[allow(dead_code)]
mod problem;

use clap::Parser;
use std::fs::metadata;
use std::path::PathBuf;
use tokio::runtime::Runtime;
use tracing::{error, warn};

#[cfg(target_family = "unix")]
use std::os::unix::fs::MetadataExt;

#[derive(Parser, Debug, Clone)]
struct CliArgs {
    #[clap(help = "Problem directory")]
    problem: PathBuf,
}

macro_rules! cerror {
    ($($arg:tt)+) => {
        {
            error!($($arg)+);
            return;
        }
    }
}

fn init_logging() {
    if let Err(x) = tracing_subscriber::fmt()
        .event_format(
            tracing_subscriber::fmt::format()
                .without_time()
                .with_target(false),
        )
        .try_init()
    {
        println!("Cannot enable logging service: {}", x);
    }
}

fn main() {
    init_logging();
    let args = CliArgs::parse();
    let problem = match args.problem.file_name() {
        Some(x) => match x.to_str() {
            Some(x) => x,
            None => cerror!("{:?} is not a valid problem name", x),
        },
        None => cerror!("Invalid problem path: no directory name"),
    };
    let mut path = args.problem.clone();
    path.pop();
    let meta = match Runtime::new() {
        Ok(rt) => rt.block_on(async move { problem::load(&path, &problem).await }),
        Err(x) => cerror!("Cannot create tokio runtime: {}", x),
    };
    let meta = match meta {
        Some(x) => x,
        None => cerror!(
            "Problem \"{}\" does not exists at path {:?}",
            problem,
            args.problem
        ),
    };
    let mut dir = meta.root;
    let meta = meta.meta;
    dir.push(meta.public_folder);
    match metadata(&dir) {
        Ok(x) if !x.is_dir() => error!("public_folder is not a directory"),
        Err(x) => error!("public_folder missing: {}", x),
        Ok(_) => {}
    };
    dir.pop();
    for (name, service) in meta.services.iter() {
        if service.evaluator.len() > 0 {
            let mut eval = dir.clone();
            eval.push(&service.evaluator[0]);
            // TODO: might be on PATH
            #[cfg(not(target_family = "unix"))]
            match metadata(&eval) {
                //Err(x) => error!("Service \"{}\" evaluator missing: {}", name, x),
                Ok(x) if !x.is_file() => {
                    error!("Evaluator of service \"{}\" is not a file", name)
                }
                _ => {}
            };
            #[cfg(target_family = "unix")]
            match metadata(&eval) {
                //Err(x) => error!(stdout, "Service \"{}\" evaluator missing: {}", name, x),
                Ok(x) if !x.is_file() => {
                    error!("Evaluator of service \"{}\" is not a file", name)
                }
                Ok(x) if x.mode() & 0o111 != 0o111 => {
                    error!("Evaluator of service \"{}\" is not executable", name)
                }
                Ok(x) if x.mode() & 0o444 != 0o444 => {
                    warn!("Evaluator of service \"{}\" is not readable", name)
                }
                _ => {}
            };
        } else {
            error!("Evaluator of service \"{}\" is empty", name);
        }
        if let Some(args) = &service.args {
            for (argname, arg) in args.iter() {
                if let Some(def) = &arg.default {
                    if !arg.regex.is_match(def) {
                        error!("Default argument for \"{}\" for service \"{}\" does not match its regex", argname, name);
                    }
                }
            }
        }
    }
}
