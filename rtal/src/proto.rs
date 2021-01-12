use crate::problem::Arg;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

pub const MAGIC: &str = "rtal";
pub const VERSION: u32 = 1;

#[derive(Serialize, Deserialize, Debug)]
pub struct Packet {
    pub magic: String,
    pub version: u32,
    pub command: Command,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum Command {
    ListRequest,
    ListResponse(ListResponse),
    WrongMagic,
    InvalidCommand,
    ConnectionRequest(ConnectionRequest),
    ConnectionBegin,
    ConnectionDenied(String),
    AttachmentRequest(String),
    AttachmentDenied(String),
    AttachmentBegin(String),
}

#[derive(Serialize, Deserialize, Debug, Default)]
pub struct ConnectionRequest {
    pub codename: String,
    pub service: String,
    pub args: HashMap<String, String>,
}

#[derive(Serialize, Deserialize, Debug, Default)]
pub struct ListResponse {
    pub problems: Vec<Problem>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Problem {
    pub codename: String,
    pub services: HashMap<String, Service>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Service {
    pub args: Option<HashMap<String, Arg>>,
}

impl Packet {
    pub fn new(command: Command) -> Packet {
        Packet {
            magic: MAGIC.to_string(),
            version: VERSION,
            command: command,
        }
    }

    pub fn valid(&self) -> bool {
        return self.magic == MAGIC && self.version == VERSION;
    }
}

impl Problem {
    pub fn from(meta: &crate::problem::Meta) -> Problem {
        let mut services = HashMap::new();
        for (name, service) in &meta.services {
            services.insert(name.clone(), Service { args: service.args.clone() });
        }
        Problem {
            codename: meta.codename.clone(),
            services: services,
        }
    }
}
