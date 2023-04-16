use std::io;
use rand::Rng;
use std::{env, time::Duration}; 
use manager::*;

//############## TESTCASES' PARAMETERS ############################
const TL: Duration = Duration::from_secs(1);   // the time limit for each testcase
const MAPPER: [&str; 5] = [
    "tiny",
    "small",
    "medium",
    "big",
    "huge",
];
type RangeN = (u64, u64);
const DATA: Pippo<RangeN> = &[
    (5, (0, 5)),
    (5, (5, 10)),
    (10, (16, 26)),
    (50, (10_u64.pow(5), 1+10_u64.pow(6) ) ),
    (30, (10_u64.pow(17), 1+10_u64.pow(18) ) )
];
// that is, 5 instances of size "tiny", i.e., with 0 <= n <= 4, ... 
//#################################################################

type Mat2x2 = [[u64; 2]; 2];

fn mat_mult(a: &Mat2x2, b: &Mat2x2, modulus: u64) -> Mat2x2 {
    let mut out: Mat2x2 = [[0, 0], [0, 0]]; 
    for i in 0..2 {
        for j in 0..2 {
            for k in 0..2 {
                out[i][j] = (out[i][j] + a[i][k] * b[k][j]) % modulus;
            }
        }
    }
    out
}

fn fast_mat_pow(mat: &Mat2x2, n: u64, modulus: u64) -> Mat2x2 {
    if n == 0 { return [[1, 0], [0, 1]]; }
    if n % 2 == 0 {
        let tmp = fast_mat_pow(mat, n/2, modulus);
        return mat_mult(&tmp, &tmp, modulus)
    }
    else {
        return mat_mult(&fast_mat_pow(mat,n-1, modulus), mat, modulus);
    }
}
    

fn num_piastrellature(n: u64) -> u64 {
  assert!(n >= 0);
  if n <= 1 { return 1; }
  let M_to_power_of_N = fast_mat_pow(&[ [1, 1], [1, 0] ], n, 10_u64.pow(9) + 7);
  return M_to_power_of_N[0][0];
}

fn gen_tc(range: &RangeN) -> u64 {
    let mut rng = rand::thread_rng();
    let n = rng.gen_range(range.0..range.1);
    println!("{n}");
    n
}

fn check_tc(n: u64) -> Result<Option<String>,&'static str> {
    let mut input_line = String::new();
    io::stdin()
        .read_line(&mut input_line)
        .expect("Failed to read line");
    let risp: u64 = input_line.trim().parse().expect("Input not an integer");
    let corr_answ = num_piastrellature(n);
    if risp != corr_answ {
        return Ok(Some(format!("On input:\n{n}\nyou answered:\n{risp}\nwhile the correct answer was:\n{corr_answ}")));
    }
    Ok(None)
}

fn main() {
    let size = env::var("TAL_size").expect("expected environment variable TAL_size");
    let size = MAPPER.iter()
        .position(|v|*v == size)
        .expect("not found in MAPPER");
    let tc = TC::new(&DATA[..=size], TL);
    tc.run(gen_tc, check_tc);
}