#!/usr/bin/env python3
from sys import argv, exit

import model_lcs_lib as ll


def main(n, m, alphabet, gen_seed, format):
    # Automatic cast:
    n = int(n)
    m = int(m)
    alphabet = alphabet
    gen_seed = int(gen_seed)

    # Generate lcs instance

    instance = ll.gen_instance(m, n, alphabet, gen_seed)

    # Generate selected output
    print(ll.instance_to_str(instance, format))


if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 6, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4], argv[5])
    exit(0)