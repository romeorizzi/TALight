mod solution;
use std::io::Write;

macro_rules! readln {
    ($($var:expr),*) => {{
        let mut buf = String::new();
        std::io::stdin().read_line(&mut buf).unwrap();
        let parts: Vec<&str> = buf.trim().split(" ").collect();
        let mut i: usize = 0;
        $(
            assert!(i < parts.len(), "input format incorrect: too few values on this line"); 
            $var = parts[i].parse().unwrap();
            i += 1;
        )*
        assert!(i == parts.len(), "input format incorrect: too many values on the line")
    }};
}

const H: i64 = 0;
const V: i64 = 1;

fn main() {
    // checkpoint
    println!("{}", 0);
    // read m, n
    let n: i64;
    let m: i64;
    std::io::stdout().flush().unwrap();
    readln!(m, n);
    // call res = is_tilable(m, n)
    let res: i64;
    res = solution::is_tilable(m, n);
    // write res
    println!("{}", res);
    // if res {...}
    if res != 0 {
        // read choice
        let choice: i64;
        std::io::stdout().flush().unwrap();
        readln!(choice);
        // if choice {...}
        if choice != 0 {
            // read m1, n1
            let m1: i64;
            let n1: i64;
            std::io::stdout().flush().unwrap();
            readln!(m1, n1);
            // call compose_tiling(m1, n1) callbacks {...}
            solution::compose_tiling(m1, n1, |row: i64, col: i64, dir: i64| {
                // callback place_tile
                println!("{} {}", 1, 0);
                // write row, col, dir
                println!("{} {} {}", row, col, dir);
            });
            // no more callbacks
            println!("{} {}", 0, 0);
        }
    }
    // exit
    std::process::exit(0);
}
