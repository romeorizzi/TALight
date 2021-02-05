#![allow(dead_code)]

mod problem;

use clap::Clap;
use std::fs::{canonicalize, metadata, read_to_string};
use std::io::Write;
use std::path::PathBuf;
use std::process::exit;
use termcolor::{Color, ColorChoice, ColorSpec, StandardStream, WriteColor};

#[cfg(target_family = "unix")]
use std::os::unix::fs::MetadataExt;

#[derive(Clap)]
struct CliArgs {
    #[clap(about = "Problem directory", default_value = ".")]
    directory: PathBuf,
}

fn ignore_result<T, E>(_: Result<T, E>) {}

macro_rules! cwriteln {
    ($stream:expr, $color:expr, $($arg:tt)+) => {
        {
            ignore_result($stream.set_color(ColorSpec::new().set_bold(true).set_fg(Some($color))));
            ignore_result(writeln!(&mut $stream, $($arg)+));
            ignore_result($stream.set_color(ColorSpec::new().set_bold(false).set_fg(None)));
        }
    }
}

macro_rules! error {
    ($stream:expr, $($arg:tt)+) => {
        {
            cwriteln!($stream, Color::Red, $($arg)+);
        }
    }
}

macro_rules! fail {
    ($stream:expr, $($arg:tt)+) => {
        {
            error!($stream, $($arg)+);
            exit(1);
        }
    }
}

macro_rules! warn {
    ($stream:expr, $($arg:tt)+) => {
        {
            cwriteln!($stream, Color::Yellow, $($arg)+);
        }
    }
}

fn main() {
    let mut stdout = StandardStream::stdout(ColorChoice::Auto);
    let opts = CliArgs::parse();
    let mut dir = match canonicalize(opts.directory) {
        Ok(x) => x,
        Err(x) => fail!(stdout, "Cannot canonicalize directory: {}", x),
    };
    dir.push(problem::META);
    let meta_str = match read_to_string(&dir) {
        Ok(x) => x,
        Err(x) => fail!(stdout, "Cannot read meta.yaml: {}", x),
    };
    dir.pop();
    let meta = match serde_yaml::from_str::<problem::Meta>(&meta_str) {
        Ok(x) => x,
        Err(x) => fail!(stdout, "Cannot parse meta.yaml: {}", x),
    };
    dir.push(meta.public_folder);
    match metadata(&dir) {
        Ok(x) if !x.is_dir() => error!(stdout, "public_folder is not a directory"),
        Err(x) => error!(stdout, "public_folder missing: {}", x),
        Ok(_) => {}
    };
    dir.pop();
    for (name, service) in meta.services.iter() {
        if service.evaluator.len() > 0 {
            let mut eval = dir.clone();
            eval.push(&service.evaluator[0]);
            #[cfg(not(target_family = "unix"))]
            match metadata(&eval) {
                Err(x) => error!(stdout, "Service \"{}\" evaluator missing: {}", name, x),
                Ok(x) if !x.is_file() => error!(stdout, "Evaluator of service \"{}\" is not a file", name),
                Ok(_) => {}
            };
            #[cfg(target_family = "unix")]
            match metadata(&eval) {
                Err(x) => error!(stdout, "Service \"{}\" evaluator missing: {}", name, x),
                Ok(x) if !x.is_file() => error!(stdout, "Evaluator of service \"{}\" is not a file", name),
                Ok(x) if x.mode() & 0o111 != 0o111 => error!(stdout, "Evaluator of service \"{}\" is not executable", name),
                Ok(x) if x.mode() & 0o444 != 0o444 => warn!(stdout, "Evaluator of service \"{}\" is not readable", name),
                Ok(_) => {}
            };
        } else {
            error!(stdout, "Evaluator of service \"{}\" is empty", name);
        }
        if let Some(args) = &service.args {
            for (argname, arg) in args.iter() {
                if !arg.regex.is_match(&arg.default) {
                    error!(stdout, "Default argument for \"{}\" for service \"{}\" does not match its regex", argname, name);
                }
            }
        }
    }
}
