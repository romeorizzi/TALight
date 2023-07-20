#!/usr/bin/env -S cargo-eval -r

//! ```cargo
//! [dependencies]
//! tal-utils = { git = "https://github.com/Guilucand/tal-utils-rs.git" }
//! roaring = { version = "0.10.1" }
//! rand = { version = "0.8", features = ["small_rng"] }
//! ```

use rand::prelude::*;
use rand::rngs::SmallRng;
use std::io::BufRead;
use std::{
    cmp::{max, min},
    io::stdin,
};
use tal_utils::{gen_data, run_tc, tc, Verdict};

const TIME_LIMIT: f64 = 5.0;

fn fetch_env(name: &str) -> tc::Result<String> {
    std::env::var(name)
        .map_err(|e| format!("Cannot get environment variable {}: {}", name, e).into())
}

#[derive(Clone)]
struct Limits {
    n: u32,
    strict_n: bool,
    multiple_k: bool,
    exact_k: Option<u32>,
    oracle_state: OracleState,
    extra_amount: u32,
}

#[derive(Clone)]
struct Instance {
    n: u32,
    k: u32,
    oracle_state: OracleState,
    extra_amount: u32,
}

fn init(subtask: Option<&str>) -> tc::Result<Vec<Limits>> {
    if let Some(subtask) = subtask {
        #[rustfmt::skip]
        let data = [
            ("small0", 5, Limits { n: 15, strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Known { liar: false }, extra_amount: 1 }),
            ("small1", 10, Limits { n: 15, strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Known { liar: false }, extra_amount: 0 }),
            ("small2", 5, Limits { n: 15, strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Unknown, extra_amount: 0 }),
            ("small3", 10, Limits { n: 15, strict_n: false, multiple_k: true, exact_k: None, oracle_state: OracleState::Unknown, extra_amount: 0 }),

            ("medium0", 5, Limits { n: 100, strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Known { liar: false }, extra_amount: 1 }),
            ("medium1", 10, Limits { n: 100, strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Known { liar: false }, extra_amount: 0 }),
            ("medium2", 5, Limits { n: 100, strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Unknown, extra_amount: 0 }),
            ("medium3", 10, Limits { n: 100, strict_n: false, multiple_k: true, exact_k: None, oracle_state: OracleState::Unknown, extra_amount: 0 }),

            ("big0", 6, Limits { n: 10_u32.pow(9), strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Known { liar: false }, extra_amount: 1 }),
            ("big1", 6, Limits { n: 10_u32.pow(9), strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Known { liar: false }, extra_amount: 0 }),
            ("big2", 6, Limits { n: 10_u32.pow(9), strict_n: false, multiple_k: false, exact_k: None, oracle_state: OracleState::Unknown, extra_amount: 0 }),
            ("big3", 6, Limits { n: 10_u32.pow(9), strict_n: false, multiple_k: true, exact_k: None, oracle_state: OracleState::Unknown, extra_amount: 0 }),
        ];
        Ok(gen_data(subtask, &data))
    } else {
        let t = fetch_env("TAL_t")?.parse::<u32>()?;
        let n = fetch_env("TAL_n")?.parse::<u32>()?;
        let k = fetch_env("TAL_k")?.parse::<u32>()?;
        let extra = fetch_env("TAL_extra")?.parse::<u32>()?;
        let bugiardi = fetch_env("TAL_bugiardi")?.parse::<u32>()?;

        Ok((0..t)
            .map(|_| Limits {
                n,
                strict_n: true,
                multiple_k: false,
                exact_k: Some(k),
                oracle_state: match bugiardi {
                    0 => OracleState::Known { liar: false },
                    1 => OracleState::Known { liar: true },
                    2 => OracleState::Unknown,
                    _ => unreachable!(),
                },
                extra_amount: extra,
            })
            .collect())
    }
}

fn gen(limits: Limits) -> tc::Result<Instance> {
    let mut rng = SmallRng::from_entropy();
    let n = if limits.strict_n {
        limits.n
    } else {
        limits.n - rng.gen_range(0..=max(6, limits.n / 4))
    };
    let k = if let Some(k) = limits.exact_k {
        k
    } else {
        if limits.multiple_k {
            rng.gen_range(2..=n.ilog2()) as u32
        } else {
            1
        }
    };
    let b = if limits.oracle_state == (OracleState::Known { liar: false }) {
        0
    } else {
        1
    };
    println!("{} {} {}", n, k, b);
    Ok(Instance {
        n,
        k,
        oracle_state: limits.oracle_state,
        extra_amount: limits.extra_amount,
    })
}

#[derive(Copy, Clone, Debug, Eq, PartialEq)]
enum OracleState {
    Unknown,
    Undecided { query: u32, greater: bool },
    Known { liar: bool },
}

fn check(inst: Instance) -> tc::Result<Verdict> {
    let mut rng = SmallRng::from_entropy();
    let mut stdin = stdin().lock();

    let mut space = roaring::RoaringBitmap::new();
    space.insert_range(0..inst.n);

    let mut orc = 0;
    let mut queries = 0;
    let sol;

    let mut orc_state = vec![inst.oracle_state; inst.k as usize];

    let best_query_count = if inst.oracle_state == OracleState::Unknown {
        let n = inst.n - inst.k;
        n.ilog2() + inst.k
    } else {
        inst.n.ilog2()
    };

    loop {
        let mut line = String::new();
        stdin.read_line(&mut line)?;
        let line = line.trim();
        let state = line
            .chars()
            .nth(0)
            .ok_or("Invalid output, expected !<number> or ?<number>")?;

        let value = line[1..].trim().parse::<u32>()? - 1;

        match state {
            '!' => {
                sol = value;
                break;
            }
            '?' => {
                queries += 1;

                if queries >= best_query_count * 10 {
                    return Ok(Verdict {
                        ok: false,
                        msg: Some(format!(
                            "Too many queries, expected at most {}, evaluator terminated your program at {} queries",
                            best_query_count, queries,
                        ))
                    });
                }

                // eprintln!("Range was: {:?}", space);

                // Only one number left
                if space.range_cardinality(0..inst.n) == 1 {
                    println!("=");
                    continue;
                }

                orc_state[orc] = match orc_state[orc] {
                    OracleState::Unknown => {
                        let greater = rng.gen_bool(0.5);

                        println!("{}", if greater { ">" } else { "<" });

                        // let left_count = space.range_cardinality(0..value);
                        // let right_count = space.range_cardinality((value + 1)..inst.n);

                        space.remove(value);

                        OracleState::Undecided {
                            query: value,
                            greater: greater,
                        }
                    }
                    OracleState::Undecided { query, greater } => {
                        if query == value {
                            println!("{}", if greater { ">" } else { "<" });
                            OracleState::Undecided { query, greater }
                        } else {
                            let inside_range =
                                space.range_cardinality((min(query, value) + 1)..max(query, value));
                            let outside_left = space.range_cardinality(0..min(query, value));
                            let outside_right =
                                space.range_cardinality((max(query, value) + 1)..inst.n);
                            // TODO: Check if this is the correct optimal condition
                            if inside_range > 2 * max(outside_left, outside_right) {
                                // Collapse the oracle
                                space.remove_range(0..(min(query, value) + 1));
                                space.remove_range(max(query, value)..inst.n);
                                println!("{}", if !greater { ">" } else { "<" });
                                OracleState::Known {
                                    // If the current value is the min of the range and we returned '>' the oracle is a liar
                                    liar: (value < query) ^ !greater,
                                }
                            } else {
                                space.remove_range(min(query, value)..(max(query, value) + 1));
                                // Keep consistency with the previous answer
                                println!("{}", if greater { ">" } else { "<" });
                                if outside_left == 0 {
                                    OracleState::Known { liar: !greater }
                                } else if outside_right == 0 {
                                    OracleState::Known { liar: greater }
                                } else {
                                    OracleState::Undecided { query, greater }
                                }
                            }
                        }
                    }
                    OracleState::Known { liar } => {
                        let left_range = space.range_cardinality(0..value);
                        let right_range = space.range_cardinality((value + 1)..inst.n);

                        let greater = left_range < right_range;

                        if greater {
                            space.remove_range(0..value + 1);
                        } else {
                            space.remove_range(value..inst.n);
                        }

                        println!("{}", if greater ^ liar { ">" } else { "<" });

                        OracleState::Known { liar }
                    }
                };

                // eprintln!("Range is: {:?} orc: {:?}", space, orc_state);
            }
            _ => {
                Err("Invalid output, expected !<number> or ?<number>")?;
            }
        }

        orc = (orc + 1) % (inst.k as usize);
    }

    let answers_left = space.range_cardinality(0..inst.n);
    let correct = answers_left == 1 && space.iter().next() == Some(sol);

    if !correct {
        let contained = space.contains(sol);

        return Ok(Verdict {
            ok: false,
            msg: Some(format!(
                "Wrong answer, with the queries performed, there are still {} feasible answers. Your solution {} {} in the set of valid answers",
                answers_left,
                sol,
                if contained { "is" } else { "is not" }
            ))
        });
    }

    if queries > best_query_count + inst.extra_amount {
        return Ok(Verdict {
            ok: false,
            msg: Some(format!(
                "The answer is correct, but with too many queries: expected at most {} with parameters [n: {} k: {}] but your solution used {} queries",
                best_query_count + inst.extra_amount,
                inst.n,
                inst.k,
                queries
            ))
        });
    }

    Ok(Verdict {
        ok: correct,
        msg: None,
    })
}

fn main() -> tc::Result<()> {
    let graded = match fetch_env("TAL_META_SERVICE").as_deref() {
        Ok("solve") => true,
        Ok("umano") => false,
        _ => panic!("Invalid service!"),
    };

    run_tc(
        if graded { TIME_LIMIT } else { 3600.0 },
        init,
        gen,
        check,
        graded,
    )
}
