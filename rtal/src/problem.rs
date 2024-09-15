use regex::Regex;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use tokio::fs::{read, read_dir};
use tracing::warn;
use std::{env, fs};
use std::process::{Command, Stdio};

pub const META: &str = "meta.yaml";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Problem {
    pub name: String,
    pub root: PathBuf,
    pub meta: Meta,
}

#[derive(Debug, Default, Serialize, Deserialize, Clone)]
pub struct Meta {
    pub public_folder: PathBuf,
    pub services: HashMap<String, Service>,
}

#[derive(Debug, Default, Serialize, Deserialize, Clone)]
pub struct Service {
    pub evaluator: Vec<String>,
    pub wasm_evaluator_source: Option<String>,
    pub args: Option<HashMap<String, Arg>>,
    pub files: Option<Vec<String>>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Arg {
    #[serde(with = "serde_regex")]
    pub regex: Regex,
    pub default: Option<String>,
}

pub async fn load_all_meta(root: &Path) -> HashMap<String, Meta> {
    let mut result = HashMap::new();
    for problem in load_all(root).await.into_values() {
        result.insert(problem.name, problem.meta);
    }
    result
}

pub async fn load_all(root: &Path) -> HashMap<String, Problem> {
    let mut result = HashMap::new();
    let mut it = match read_dir(root).await {
        Ok(x) => x,
        Err(x) => {
            warn!("Cannot open problems directory: {}", x);
            return result;
        }
    };
    loop {
        let entry = match it.next_entry().await {
            Ok(Some(x)) => x,
            Ok(None) => break,
            Err(x) => {
                warn!("Error while reading problems: {}", x);
                break;
            }
        };
        let kind = match entry.file_type().await {
            Ok(x) => x,
            Err(x) => {
                warn!("Cannot get file type of {:?}: {}", entry.path(), x);
                continue;
            }
        };
        match (kind.is_dir(), kind.is_symlink()) {
            (true, _) => {}
            (_, true) => match tokio::fs::read_link(entry.path()).await {
                Ok(x) => {
                    let x = if x.is_relative() {
                        entry.path().parent().unwrap().to_path_buf()
                    } else {
                        x.to_path_buf()
                    };
                    if !x.is_dir() {
                        warn!("{:?} is not a directory", x);
                        continue;
                    }
                }
                Err(x) => {
                    warn!("Cannot read link {:?}: {}", entry.path(), x);
                    continue;
                }
            },
            _ => {
                warn!("{:?} is not a directory", entry.path());
                continue;
            }
        }
        let problem_name = match entry.file_name().to_str() {
            Some(x) => x.to_string(),
            None => {
                warn!("{:?} is not a valid problem name", entry.file_name());
                continue;
            }
        };
        if let Some(problem) = load(root, &problem_name).await {
            result.insert(problem_name, problem);
        }
    }
    result
}

fn deploy_wasm(p: &Problem) -> Result<(), String> {
    for (_, service) in &p.meta.services {
        if service.evaluator.get(0) != Some(&String::from("wasmtime")) {
            continue;
        }
        if service.evaluator.len() < 2 {
            return Err(format!("{}: Missing wasmtime argument in evaluator vector", &p.name));
        }
        let mut wasm_file = PathBuf::from(&p.root);
        wasm_file.push(&service.evaluator[1]);
        if wasm_file.exists() {
            continue;
        }
        let src = match &service.wasm_evaluator_source {
            Some(src) => src,
            None => return Err(format!("{}: Missing wasm_evaluator_source field", &p.name)),
        };
        let mut source_path = PathBuf::from(&p.root);
        source_path.push(src);
        if !source_path.exists() {
            return Err(format!("{}: wasm_evaluator_source file doesn't exist", &p.name));
        }
        let wasi = format!("--sysroot={}/share/wasi-sysroot", env::var("WASI_SDK_PATH").unwrap_or_default());
        let (command_string, command_args) = match source_path.extension().and_then(|ext| ext.to_str()) {
            Some("rs") => {
                let mut cargo_path = PathBuf::from(&p.root);
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
            _ => return Err(format!("{}: wasm_evaluator_source doesn't have a valid extension", &p.name)),
        };
        let status = Command::new(command_string)
            .args(&command_args)
            .current_dir(&p.root)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status();
        if status.is_err() {
            return Err(format!("{}: Cannot compile to wasm", &p.name));
        }
        if command_string == "cargo" {
            let mut target_path = PathBuf::from(&p.root);
            target_path.push("target/wasm32-wasip1/release");
            if let Ok(entries) = fs::read_dir(&target_path) {
                for entry in entries.flatten() {
                    if entry.path().extension().and_then(|ext| ext.to_str()) == Some("wasm") {
                        let mut dest_path = PathBuf::from(&p.root);
                        dest_path.push(&service.evaluator[1]);
                        if fs::copy(entry.path(), dest_path).is_err() {
                            return Err(format!("{}: Cannot move .wasm to main folder", &p.name));
                        }
                        break;
                    }
                }
            }
        }
        if !wasm_file.exists() {
            return Err(format!("{}: Could not generate evaluator", &p.name));
        }
    }
    Ok(())
}

pub async fn load(root: &Path, problem: &str) -> Option<Problem> {
    let mut root = root.to_path_buf();
    root.push(problem);
    let problem_root = root.clone();
    root.push(META);
    let content = match read(root).await {
        Ok(x) => x,
        Err(x) => {
            warn!("Cannot read {} of problem {}: {}", META, problem, x);
            return None;
        }
    };
    let meta: Meta = match serde_yaml::from_slice(&content) {
        Ok(x) => x,
        Err(x) => {
            warn!("Error while parsing {} of problem {}: {}", META, problem, x);
            return None;
        }
    };
    let problem = Problem {
        name: problem.to_string(),
        meta: meta,
        root: problem_root,
    };
    match deploy_wasm(&problem) {
        Ok(_) => Some(problem),
        Err(e) => {
            warn!(e);
            None
        }
    }
}
