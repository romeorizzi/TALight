# Rust Turing Arena Light

This is a Rust implementation of the Turing Arena Light specification.
It offers two main programs plus other utilities mainly meant for the problem maker:

1. `rtal` (the rust implementation of the TA-light client)

2. `rtald` (the rust implementation of the TA-light daemon)

3. `rtalc` (the rust implementation of a checker of the consistency of the `meta.yaml` file listing the services of a problem)

This document explains how to build up all these `TALight` commands for your architecture.
Do not scare because:

1. the process is simple and you will be followed step as step;

2. you will not need to use nor know anything about Rust.


## Building the needed binaries

In order to build this project, you will first need a working installation of the Rust compiler and Cargo.
If you don't already have these, the official service [rustup.rs](https://rustup.rs/) from the rust community will guide you with updated instructions through the few simple steps needed to set these up. The service assumes you have a terminal at your disposal (which, in case you are on a Windows platform, can be the CMD). The terminal il also a main companion and your close friend in enjoying the TALight services.

Once Rust is set up, you have two options for the kinds of builds you intend to obtain.
The `Relase build` is by far more efficient in term of performances.
The `Debug build` provides you with more detailed information when you use it. For what it costs, we actually suggest you to make them both.
However, using the debug version (binaries placed in the `~/TALight/rtal/target/debug` folder) rather than the release version (binaries placed in the `~/TALight/rtal/relase/debug` folder) is the best choice and practice, you can switch to the other in those few situations when in need for more performances. 

### Debug build

To build this project in debug mode, first move to the directory `rtal` of this repo as downloaded on your local machine, and then issue the command:
```bash
cargo build
```
You'll then find the built binaries in `target/debug/`.

### Release build

To build this project in release mode, first move to the directory `rtal` of this repo as downloaded on your local machine, and then issue the command:
```bash
cargo build --release
```
You'll then find the built binaries in `target/release/`.

