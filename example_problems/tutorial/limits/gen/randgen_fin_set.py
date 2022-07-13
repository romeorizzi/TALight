#!/usr/bin/env python3
from sys import argv, exit

import limiti_lib as ll

def main(set_cardinality, gen_seed):
    # Automatic cast:
    set_cardinality = int(set_cardinality)
    gen_seed = int(gen_seed)

    # Generate lcs instance
    instance = ll.instance_randgen(set_cardinality, gen_seed)

    # Generate selected output
    print(', '.join(instance))


if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 4, 'Miss arguments'
    main(argv[1], argv[2])
    exit(0)
