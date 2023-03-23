use crate::problem::Meta;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

pub const MAGIC: &str = "rtal";
pub const VERSION: u64 = 3;

#[derive(Serialize, Deserialize, Debug)]
pub enum Request {
    Handshake {
        magic: String,
        version: u64,
    },
    MetaList {},
    Attachment {
        problem: String,
    },
    ConnectBegin {
        problem: String,
        service: String,
        args: HashMap<String, String>,
        tty: bool,
        token: Option<String>,
        files: Vec<String>,
    },
    ConnectStop {},
}

#[derive(Serialize, Deserialize, Debug)]
pub enum Reply {
    Handshake { magic: String, version: u64 },
    MetaList { meta: HashMap<String, Meta> },
    Attachment { status: Result<(), String> },
    ConnectBegin { status: Result<Vec<String>, String> },
    ConnectStart { status: Result<(), String> },
    ConnectStop { status: Result<Vec<String>, String> },
}

#[allow(dead_code)]
impl Request {
    pub fn forge(&self) -> Result<String, String> {
        match serde_json::to_string(self) {
            Ok(x) => Ok(x),
            Err(x) => Err(format!("Cannot forge request: {}", x)),
        }
    }
    pub fn parse(req: &str) -> Result<Request, String> {
        match serde_json::from_str(req) {
            Ok(x) => Ok(x),
            Err(x) => Err(format!("Cannot parse request: {}", x)),
        }
    }
}

#[allow(dead_code)]
impl Reply {
    pub fn forge(&self) -> Result<String, String> {
        match serde_json::to_string(self) {
            Ok(x) => Ok(x),
            Err(x) => Err(format!("Cannot forge request: {}", x)),
        }
    }
    pub fn parse(req: &str) -> Result<Reply, String> {
        match serde_json::from_str(req) {
            Ok(x) => Ok(x),
            Err(x) => Err(format!("Cannot parse request: {}", x)),
        }
    }
}
