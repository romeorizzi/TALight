#!/usr/bin/env python3
import os
from sys import argv, exit
from pathlib import Path
import triangle_lib as tl


def main(n, m, MIN_VAL, MAX_VAL, MIN_VAL_BIG, MAX_VAL_BIG, seed, big_seed, path, usage, file_full_extension):
    # Automatic cast:
    n = int(n)
    m = int(m)
    MIN_VAL = int(MIN_VAL)
    MAX_VAL = int(MAX_VAL)
    MIN_VAL_BIG = int(MIN_VAL_BIG)
    MAX_VAL_BIG = int(MAX_VAL_BIG)
    seed = int(seed)
    big_seed = int(big_seed)
    # Generate triangle instance
    instance = tl.instances_generator(1, 1, MIN_VAL, MAX_VAL, n, n, m, m, MIN_VAL_BIG, MAX_VAL_BIG, seed, big_seed, path, "double")[0]
    # Generate selected output
    print(tl.instance_to_str(instance, tl.file_extension_to_format_name(file_full_extension)))

if __name__ == "__main__":
    from sys import argv
    #assert len(argv) == 11, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11])
    exit(0)


