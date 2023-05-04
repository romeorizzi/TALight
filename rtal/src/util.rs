use futures_util::{Sink, SinkExt, Stream, StreamExt};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fmt::Display;
use tokio_tungstenite::tungstenite::Error as TsError;
use tokio_tungstenite::tungstenite::Message;

pub const BUFFER_SIZE: usize = 1 << 20;

#[derive(Serialize, Deserialize, Debug)]
pub enum StreamMessage {
    BinaryDataHeader {
        name: String,
        size: usize,
        hash: [u8; 32],
    },
}

pub async fn send_binary_data<T: Sink<Message> + Unpin>(
    wsout: &mut T,
    name: &str,
    data: &[u8],
) -> Result<(), String>
where
    <T as Sink<Message>>::Error: Display,
{
    let header = StreamMessage::BinaryDataHeader {
        name: name.to_string(),
        size: data.len(),
        hash: Sha256::digest(data).into(),
    };
    let serialized_header = match serde_json::to_string(&header) {
        Ok(x) => x,
        Err(x) => return Err(format!("Cannot serialize binary header: {}", x)),
    };
    if let Err(x) = wsout.send(Message::Text(serialized_header)).await {
        return Err(format!("Cannot send binary header: {}", x));
    }
    for offset in (0..data.len()).step_by(BUFFER_SIZE) {
        let slice = &data[offset..data.len().min(offset + BUFFER_SIZE)];
        if let Err(x) = wsout.send(Message::Binary(slice.to_vec())).await {
            return Err(format!("Cannot send binary data: {}", x));
        }
    }
    Ok(())
}

pub async fn recv_binary_data<U: Stream<Item = Result<Message, TsError>> + Unpin>(
    wsin: &mut U,
) -> Result<(String, Vec<u8>), String> {
    let header = loop {
        match wsin.next().await {
            Some(Ok(Message::Text(x))) => break x,
            Some(Ok(_)) => continue,
            Some(Err(x)) => return Err(format!("Error while receiving binary header: {}", x)),
            None => {
                return Err(format!(
                    "Connection interrupted while waiting for binary header"
                ))
            }
        }
    };
    let (name, size, hash) = match serde_json::from_str::<StreamMessage>(&header) {
        Ok(StreamMessage::BinaryDataHeader { name, size, hash }) => (name, size, hash),
        Err(x) => return Err(format!("Received invalid binary header: {}", x)),
    };
    let mut buffer = Vec::new();
    loop {
        if buffer.len() >= size {
            break;
        }
        let mut data = match wsin.next().await {
            Some(Ok(Message::Binary(x))) => x,
            Some(Ok(_)) => continue,
            Some(Err(x)) => return Err(format!("Error while receiving binary data: {}", x)),
            None => {
                return Err(format!(
                    "Connection interrupted while waiting for binary data"
                ))
            }
        };
        buffer.append(&mut data);
    }
    if Into::<[u8; 32]>::into(Sha256::digest(&buffer)) != hash {
        return Err(format!("Received corrupted binary data"));
    }
    Ok((name, buffer))
}
