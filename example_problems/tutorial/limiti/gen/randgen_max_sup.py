#!/usr/bin/env python3
from sys import argv, exit

import limiti_lib as ll

def main(gen_seed):
    # Automatic cast:
    gen_seed = int(gen_seed)

    # Generate lcs instance
    _,instance,_,_=ll.instance_randgen_1(gen_seed)

    # Generate selected output
    print(instance+'\n'+str(gen_seed))

if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 3, 'Miss arguments'
    main(argv[1])
    exit(0)
