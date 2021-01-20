# Rust Turing Arena Light

This is a Rust implementation of the Turing Arena Light specification.
It consists of two programs, the `rtal` client, and the `rtald` server.

## Building

In order to build this project, you will first need a working installation of the Rust compiler and Cargo.
If you don't already have these, the official service [rustup.rs](https://rustup.rs/) from the rust community will guide you with updated instructions through the few simple steps needed to set these up. The service assumes you have a terminal at your disposal (which, in case you are on a Windows platform, can be the CMD). The terminal il also a main companion and your close friend in enjoying the TAlight services.

Once rust is set up, you have two options for the kinds of builds you intend to obtain. We actually suggest you to make them both. One is more efficient, the other provides more information when you use it.

### Debug build

To build this project in debug mode issue the command:
```bash
cargo build
```
You'll then find the built binaries in `target/debug/`.

### Release build

To build this project in debug mode issue the command:
```bash
cargo build --release
```
You'll then find the built binaries in `target/release/`.

## Usage examples

Both `rtal` and `rtald` have detailed `--help` sections, here we just provide a sample invocation of both the server and the client to showcase a minimal usage example (we assume a POSIX-like shell).

When starting the server, it is a good idea to also turn on logging, by setting the environment variable `RUST_LOG=info`.
Thus, if for example you have just compiled the binaries and are sitting in the `rtal` directory of the project while the problems are located in the `../problems/` directory, then you can start the server as follows:
```bash
RUST_LOG=info ./target/debug/rtald -d ../problems/
```
That terminal will now be the place where the server `rtald` updates you on about the requests of service it receives and what is going on with them.

Open another terminal (I prefer vertically splitting my terminator so that I quickly perceive what is going on while experimenting) to send requests with your client `rtal`.
To list the problems available, and thus check that both the client and the server are working, try the following command:
```bash
./target/debug/rtal list
```
In the list of available problems at least the example problem `sum` should appear. 

Two examples on how to invocate the help sections

```bash
./target/debug/rtal --help
```

```bash
./target/debug/rtal list --help
```

To explore the services available for the example problem `sum` try issuing
```bash
target/debug/rtal list sum -v
```
to get something like
```bash
- sum
  * observe
    # lang [it] { ^(en|it)$ }
  * solve
    # subtask [small] { ^(small|big)$ }
    # lang [it] { ^(en|it)$ }
```
From this you understand that two services (`observe` and `solve`) are up for this problem on your local machine. If you want to talk with another service use the `-s` option that was mentioned when you run `rtal --help`. (And consider placing the directories of these binaries in your path environment variable. We assume this to be the case to shorten the commands to the essential.)
Combining the problem specific information you got above by issuing `rtal list sum -v` with the TAlight core instructions you get with `rtal connect --help` you could decide to try the following service:

```bash
rtal connect -a subtask=small sum solve
```

Problem `sum` also exemplifies how to interact with a service through a browser rather than through the terminal.
In this way and by resorting on HTML/CCS/JavaScript technology, nice applets running on the problem solver site can be designed for more user friendly interactions.
Just look in the `applets` directory of the project and run

```bash
~/TAlight/applets$ google-chrome sum-protoapplet.html
```
In this file, it is easy to spot out and substitute the hardcoded problem-specific parts and get an analogous page for a first browser mediated interaction also for other problems. One can start from here in order to develop ad-hoc applets specific to other problems.