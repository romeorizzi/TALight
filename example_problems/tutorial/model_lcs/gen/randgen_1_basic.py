#!/usr/bin/env python3
from sys import argv, exit

import model_lcs_lib as ll


def main(m, n, alphabet, gen_seed, file_full_extension):
    # Automatic cast:
    m = int(m)
    n = int(n)
    alphabet = alphabet
    gen_seed = int(gen_seed)

    # Generate lcs instance
    instance = ll.instance_randgen_1(m, n, alphabet, gen_seed)

    # Generate selected output
    print(ll.instance_to_str(instance, ll.file_extension_to_format_name(file_full_extension)))


if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 6, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4], argv[5])
    exit(0)
