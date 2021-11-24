#!/usr/bin/env python3
from sys import argv, stderr, exit

import model_ANN_lib as annl



def main(n_nodes, gen_seed, format):
    # Automatic cast
    gen_seed = int(gen_seed)

    # Generate instance
    instance = annl.gen_instance(n_nodes, gen_seed) # instance here is a list of lists [tot_num_layers, [tot_num_nodes_for_each_layer], [weigths_1], ... ,[weigths_n]]

    # Generate selected output
    print(annl.instance_to_str(instance, format))


if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 4, 'Miss arguments'
    main(argv[1], argv[2], argv[3])
    exit(0)