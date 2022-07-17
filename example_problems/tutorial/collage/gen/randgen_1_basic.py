#!/usr/bin/env python3
import os
from sys import argv, exit
from pathlib import Path
import collage_lib as cl


def main(seq_len, num_col, mod, seed, file_full_extension):
    # Automatic cast:
    seq_len = int(seq_len)
    num_col = int(num_col)
    mod = int(mod)
    seed = int(seed)
    # Generate collage instance
    instance = cl.instances_generator(1, 1, seq_len, num_col, mod, seed)[0]
    # Generate selected output
    print(cl.instance_to_str(instance, cl.file_extension_to_format_name(file_full_extension)))

if __name__ == "__main__":
    from sys import argv
    #assert len(argv) == 5, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4], argv[5])
    exit(0)
