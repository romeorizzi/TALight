use regex::Regex;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use tokio::fs::{read, read_dir};
use tracing::warn;

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
    Some(problem)
}
