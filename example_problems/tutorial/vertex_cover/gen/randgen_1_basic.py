#!/usr/bin/env python3
import os
from sys import argv, exit
from pathlib import Path
import vertex_cover_lib as vcl

EXACT_LIMIT = 80

def main(num_vertices, num_edges, seed, weighted, file_full_extension):
    # Automatic cast:
    num_vertices = int(num_vertices)
    num_edges = int(num_edges)
    seed = int(seed)
    weighted = int(weighted)
    # Generate graph instance
    instance = vcl.instances_generator(1, 1, num_vertices, num_edges, seed, weighted)[0]

    if num_vertices <= EXACT_LIMIT:
      size, sol = vcl.calculate_minimum_vc(instance['graph'])
      instance['exact_sol'] = True
      instance['risp'] = sol
    else:
      size, sol, max_matching = vcl.calculate_approx_vc(instance['graph'])
      instance['exact_sol'] = False
      instance['risp'] = max_matching

    # Generate selected output
    print(vcl.instance_to_str(instance, vcl.file_extension_to_format_name(file_full_extension)))
    

if __name__ == "__main__":
    from sys import argv
    #assert len(argv) == 5, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4], argv[5])
    exit(0)
