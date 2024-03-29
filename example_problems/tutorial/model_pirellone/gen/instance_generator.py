#!/usr/bin/env python3
from sys import argv, stderr, exit

import pirellone_lib as pl


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


def main(n, m, solvable, gen_seed, format):
    # Automatic cast:
    n = int(n)
    m = int(m)
    solvable = str2bool(solvable)
    gen_seed = int(gen_seed)

    # Generate pirellone instance
    pirellone = pl.gen_instance(m, n, gen_seed)

    # Generate selected output
    print(pl.instance_to_str(pirellone, pl.file_extension_to_format_name(format)))


if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 6, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4], argv[5])
    exit(0)