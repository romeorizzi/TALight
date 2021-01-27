use regex::Regex;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::PathBuf;

pub const META: &str = "meta.yaml";

#[derive(Debug, Default, Serialize, Deserialize)]
pub struct Meta {
    pub codename: String,
    pub public_folder: PathBuf,
    pub services: HashMap<String, Service>,
}

#[derive(Debug, Default, Serialize, Deserialize)]
pub struct Service {
    pub evaluator: String,
    pub args: Option<HashMap<String, Arg>>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Arg {
    #[serde(with = "serde_regex")]
    pub regex: Regex,
    pub default: String,
}
