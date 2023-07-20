#!/usr/bin/env -S cargo-eval -r

//! ```cargo
//! [dependencies]
//! tal-utils = { git = "https://github.com/dariost/tal-utils-rs.git" }
//! roaring = { version = "0.10.1" }
//! rand = { version = "0.8", features = ["small_rng"] }
//! ```

use std::{
    cmp::Ordering,
    io::{stdin, stdout, Write},
};
use tal_utils::Parser;

#[derive(Copy, Clone, Debug)]
enum OracleState {
    Unknown,
    Liar,
    Truthful,
}

fn query(x: u64, state: OracleState) -> Ordering {
    println!("?{}", x);
    stdout().flush().unwrap();
    let r: char = stdin().lock().get().unwrap();
    match r {
        '<' => {
            if let OracleState::Liar = state {
                Ordering::Greater
            } else {
                Ordering::Less
            }
        }
        '=' => Ordering::Equal,
        '>' => {
            if let OracleState::Liar = state {
                Ordering::Less
            } else {
                Ordering::Greater
            }
        }
        _ => panic!("Invalid response"),
    }
}

fn main() {
    let t: u64 = stdin().lock().get().unwrap();

    'next: for tc in 0..t {
        let n: u64 = stdin().lock().get().unwrap();
        let k = stdin().lock().get().unwrap();
        let b: u64 = stdin().lock().get().unwrap();

        eprintln!("Testcase {tc}: n={n}, k={k}, b={b}");

        let mut states = vec![
            if b == 0 {
                OracleState::Truthful
            } else {
                OracleState::Unknown
            };
            k
        ];

        let mut low = 1;
        let mut high = n;
        let mut oracle = 0;

        if b == 1 {
            for state in states.iter_mut() {
                match query(low, OracleState::Unknown) {
                    Ordering::Less => {
                        *state = OracleState::Liar;
                    }
                    Ordering::Equal => {
                        println!("!{}", low);
                        stdout().flush().unwrap();
                        continue 'next;
                    }
                    Ordering::Greater => {
                        *state = OracleState::Truthful;
                    }
                }
                low += 1;
            }
        }

        while low != high {
            let mid = (low + high) / 2;
            match query(mid, states[oracle]) {
                Ordering::Less => {
                    high = mid - 1;
                }
                Ordering::Equal => {
                    println!("!{}", low);
                    stdout().flush().unwrap();
                    continue 'next;
                }
                Ordering::Greater => {
                    low = mid + 1;
                }
            }
            oracle = (oracle + 1) % k;
        }

        println!("!{}", low);
        stdout().flush().unwrap();
    }
}
