# Rust Turing Arena Light

This is a Rust implementation of the Turing Arena Light specification.
It consists of two programs, the `rtal` client, and the `rtald` server.

## Building

In order to build this project, you will first need a working installation of the Rust compiler and Cargo.
If you don't already have win, visit [rustup.rs](https://rustup.rs/).

### Debug build

To build this project in debug mode issue the command:
```
cargo build
```
You'll then find the built binaries in `target/debug/`.

### Release build

To build this project in debug mode issue the command:
```
cargo build --release
```
You'll then find the built binaries in `target/release/`.

## Usage examples

Both `rtal` and `rtald` have detailed `--help` sections, here we just provide a sample invocation of both the server and the client to showcase a minimal usage example (we assume a POSIX-like shell).

When starting the server, it is a good idea to also turn on logging, by setting the environment variable `RUST_LOG=info`.
Thus, if for example the problems are located in the `../problems/` directory, we can start the server as follows:
```
RUST_LOG=info ./rtald -d ../problems/
```

To list the problems available through the client, and thus check that both the client and the server are working, we can use the following command:
```
./rtal list -v
```
