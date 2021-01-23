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
That terminal will now be the place where the server `rtald` updates you about the requests of service it receives and what is going on with them.

Open another terminal (I prefer vertically splitting my terminator so that I quickly perceive what is going on while experimenting) to send requests with your client `rtal`.
To list the problems available, and thus check that both the client and the server are working, try the following command:
```bash
./target/debug/rtal list
```
In the list of available problems at least the example problem `sum` should appear.


## SETUP OF THE PATH ENVIRONMENT VARIABLE

Having to remember and digit the whole path `~/TAlight/target/debug/rtal list` in order to access the `TAlight` services will soon appear too lengthly.
To avoid this, we suggest a convenint way to make them directly accessible. 

From the terminal,
lounch the following commands
```bash
mkdir ~/.bin
cd ~/.bin
ln -s ~/TAlight/rtal/target/debug/rtald ~/.bin/
ln -s ~/TAlight/rtal/target/debug/rtal ~/.bin/
```

Then, add the following line at the end of your `~/.bashrc` file.

```bash
export PATH="$PATH:$HOME/.bin"
```

Remember that this update will be effective only for terminals you open after having modifyied the `~/.bashrc` file.
If you want older terminals to get the update then you can issue from them the command
```bash
source .bashrc
```

## Getting some help with `rtal` and `rtald`

Two examples on how to invocate the help sections

```bash
rtal --help
```

```bash
rtal list --help
```

## Exploring the services available for a problem

To explore the services available for the example problem `sum` try issuing
```bash
rtal list sum -v
```
to get something like
```bash
- sum
  * sum_and_difference
    # numbers [onedigit] { ^(onedigit|twodigits|big)$ }
    # lang [it] { ^(en|it)$ }
  * sum
    # obj [any] { ^(any|max_product)$ }
    # numbers [twodigits] { ^(onedigit|twodigits|big)$ }
    # lang [it] { ^(en|it)$ }
  * sum_and_product
    # lang [it] { ^(en|it)$ }
    # numbers [onedigit] { ^(onedigit|twodigits|big)$ }
```
From this you understand that three services (`sum`, `sum_and_difference`, and `sum_and_product`) are up for this problem on your local machine. If you want to talk with another server made available online use the `-s` option that is mentioned when you run `rtal --help`.
Combining the problem specific information you got above by issuing `rtal list sum -v` with the TAlight core instructions you get with `rtal connect --help` you could decide to try the following service:

```bash
rtal connect -a numbers=big sum sum_and_product
```

```bash
rtal connect -a numbers=big sum sum -- sum_mysolution.py
```

In the first case you will enjoy a direct interaction with the server through the terminal (this can be enough or anyhow play helpful to find out about the service and the protocol of the interaction).
In the second case you connect your local solution program or bot `sum_mysolution.py` to the server to check out how your method you have therein encoded performs.
Clearly the file `sum_mysolution.py` must have the correct permissions in order to be executed on your local system. In other words the file must be an excutable, but otherwise any programming language could have been used to produced it. 
If you want to observe the interaction between your bot and the server you can issue:

```bash
rtal connect -e -a numbers=small sum sum -- sum_mysolution.py
```

Problem `sum` also exemplifies how to interact with a service through a browser rather than through the terminal.
In this way and by resorting on HTML/CCS/JavaScript technology, nice applets running on the problem solver site can be designed for more user friendly interactions.
Just look in the `applets` directory of the project and run

```bash
~/TAlight/applets$ google-chrome sum-protoapplet.html
```
In this file, it is easy to spot out and substitute the hardcoded problem-specific parts and get an analogous page for a first browser mediated interaction also for other problems. One can start from here in order to develop ad-hoc applets specific to other problems and offer fun active learnig opportunities also to kids that do not yet know how to code.
