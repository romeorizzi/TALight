#!/usr/bin/env python3
from sys import argv, stderr, exit

import asteroid_lib as al



def main(n, m, gen_seed, format):
    # Automatic cast:
    n = int(n)
    m = int(m)
    gen_seed = int(gen_seed)

    # Generate instance
    (instance, seed) = al.gen_instance(m, n, gen_seed)

    # Generate selected output
    print(al.instance_to_str(instance, format))


if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 5, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4])
    exit(0)