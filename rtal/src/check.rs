#[allow(dead_code)]
mod problem;

use clap::Parser;
use std::fs::metadata;
use std::path::PathBuf;
use tokio::runtime::Runtime;
use tracing::{error, warn};
use std::{env, fs};
use std::process::{Stdio, Command};

#[cfg(target_family = "unix")]
use std::os::unix::fs::MetadataExt;
use crate::problem::Service;

#[derive(Parser, Debug, Clone)]
#[clap(version)]
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

fn deploy_wasm(service: &Service, service_name: &str, service_root: &PathBuf) -> Result<(), String> {
    if service.evaluator.len() < 2 {
        return Err(format!("{}: Missing wasmtime argument in evaluator vector", service_name));
    }
    let mut wasm_file = PathBuf::from(&service_root);
    wasm_file.push(&service.evaluator[1]);
    if !wasm_file.exists() {
        let src = match &service.wasm_evaluator_source {
            Some(src) => src,
            None => return Err(format!("{}: Missing wasm_evaluator_source field", service_name))
        };
        let mut source_path = PathBuf::from(&service_root);
        source_path.push(src);
        if !source_path.exists() {
            return Err(format!("{}: wasm_evaluator_source file doesn't exist", service_name));
        }
        let wasi = format!("--sysroot={}/share/wasi-sysroot", env::var("WASI_SDK_PATH").unwrap_or_default());
        let (command_string, command_args) = match source_path.extension().and_then(|ext| ext.to_str()) {
            Some("rs") => {
                let mut cargo_path = PathBuf::from(&service_root);
                cargo_path.push("Cargo.toml");
                if source_path.components().any(|comp| comp == std::path::Component::Normal("src".as_ref()))
                    && cargo_path.exists() {
                    ("cargo", vec!["build", "--target", "wasm32-wasip1", "--release"])
                } else {
                    ("rustc", vec![src, "-o", &service.evaluator[1], "--target", "wasm32-wasip1"])
                }
            }
            Some("cpp") | Some("cc") => {
                ("clang++", vec!["--target=wasm32-wasip1", &wasi, src, "-o", &service.evaluator[1]])
            }
            Some("c") => {
                ("clang", vec!["--target=wasm32-wasip1", &wasi, src, "-o", &service.evaluator[1]])
            }
            _ => return Err(format!("{}: wasm_evaluator_source doesn't have a valid extension", service_name))
        };
        let status = Command::new(command_string)
            .args(&command_args)
            .current_dir(&service_root)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status();
        if status.is_err() {
            return Err(format!("{}: Cannot compile to wasm", service_name));
        }
        if command_string == "cargo" {
            let mut target_path = PathBuf::from(&service_root);
            target_path.push("target/wasm32-wasip1/release");
            if let Ok(entries) = fs::read_dir(&target_path) {
                for entry in entries.flatten() {
                    if entry.path().extension().and_then(|ext| ext.to_str()) == Some("wasm") {
                        let mut dest_path = PathBuf::from(&service_root);
                        dest_path.push(&service.evaluator[1]);
                        if fs::copy(entry.path(), dest_path).is_err() {
                            return Err(format!("{}: Cannot move .wasm to main folder", service_name));
                        }
                        break;
                    }
                }
            }
        }
        if !wasm_file.exists() {
            return Err(format!("{}: Could not generate evaluator", service_name));
        }
    }
    Ok(())
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
            if service.evaluator.get(0) == Some(&String::from("wasmtime")) {
                if let Err(e) = deploy_wasm(service, name, &dir) {
                    error!(e);
                }
            }
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
