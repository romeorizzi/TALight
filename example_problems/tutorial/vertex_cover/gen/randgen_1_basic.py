#!/usr/bin/env python3
import os
from sys import argv, exit
from pathlib import Path
import vertex_cover_lib as vcl

EXACT_LIMIT = 80

def main(num_vertices, num_edges, seed, weighted, approx, file_full_extension):
    # Automatic cast:
    num_vertices = int(num_vertices)
    num_edges = int(num_edges)
    seed = int(seed)
    weighted = int(weighted)
    approx = int(approx)
    # Generate graph instance
    instance = vcl.instances_generator(1, 1, num_vertices, num_edges, seed, weighted)[0]

    #if num_vertices <= EXACT_LIMIT:
    if not approx:
      if not weighted:
        size, sol = vcl.calculate_minimum_vc(instance['graph'])
      else:
        sol, size, weight = vcl.calculate_minimum_weight_vc(instance['graph'])
        instance['risp_weight'] = weight
    
      instance['exact_sol'] = True
      instance['risp'] = sol

    else:
      if not weighted:
        size, sol, max_matching = vcl.calculate_approx_vc(instance['graph'])
        instance['exact_sol'] = False
        instance['risp'] = f'{sol}\n{max_matching}'
        #instance['risp'] = max_matching
      else:
        sol, size, weight = vcl.calculate_weighted_approx_vc(instance['graph'])
        instance['exact_sol'] = False
        instance['risp'] = sol
        instance['risp_weight'] = weight

    # Generate selected output
    print(vcl.instance_to_str(instance, vcl.file_extension_to_format_name(file_full_extension)))
    

if __name__ == "__main__":
    from sys import argv
    #assert len(argv) == 5, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6])
    exit(0)
