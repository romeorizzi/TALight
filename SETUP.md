LINUX UBUNTU:

sudo apt install rustc cargo
sudo apt install libssl-dev pkg-config

# Compila in modalità debug:

rtdl> cargo build

# Compila in modalità relase:

rtdl> cargo build --release

~/TAlight/rtal/target/debug>export RUST_LOG=info
~/TAlight/rtal/target/debug>./rtald -d ~/TAlight/problems/

MAC: apt=?

sudo apt install rustc cargo

# Compila in modalità debug:

rtdl> cargo build

# Compila in modalità relase:

rtdl> cargo build --release

~/TAlight/rtal/target/debug>export RUST_LOG=info
~/TAlight/rtal/target/debug>./rtald -d ~/TAlight/problems/


WINDOWS:

1. installarsi cargo e il compilatore di rust
2. Generare i binari
# Compila in modalità debug:

rtdl> cargo build

# Compila in modalità relase:

rtdl> cargo build --release

INVOCAZIONE:

~/TAlight/rtal/target/debug>set RUST_LOG=info
~/TAlight/rtal/target/debug>rtald.exe -d ~/TAlight/problems/

