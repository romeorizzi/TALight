use futures_util::{Sink, SinkExt, Stream, StreamExt};
use serde::{Deserialize, Serialize};
use std::fmt::Display;
use tokio_tungstenite::tungstenite::Error as TsError;
use tokio_tungstenite::tungstenite::Message;
use twox_hash::xxh3::hash128;

pub const BUFFER_SIZE: usize = 1 << 20;

#[derive(Serialize, Deserialize, Debug)]
pub struct BinaryDataHeader {
    pub name: String,
    pub size: usize,
    pub hash: u128,
}

pub async fn send_binary_data<T: Sink<Message> + Unpin>(
    wsout: &mut T,
    name: &str,
    data: &[u8],
) -> Result<(), String>
where
    <T as Sink<Message>>::Error: Display,
{
    let header = BinaryDataHeader {
        name: name.to_string(),
        size: data.len(),
        hash: hash128(data),
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
    let header = match serde_json::from_str::<BinaryDataHeader>(&header) {
        Ok(x) => x,
        Err(x) => return Err(format!("Received invalid binary header: {}", x)),
    };
    let mut buffer = Vec::new();
    loop {
        if buffer.len() >= header.size {
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
    if hash128(&buffer) != header.hash {
        return Err(format!("Received corrupted binary data"));
    }
    Ok((header.name, buffer))
}
