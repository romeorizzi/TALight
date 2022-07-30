#!/usr/bin/env python3
import os
from sys import argv, exit
from pathlib import Path
import vertex_cover_lib as vcl


def main(num_vertices, seed, file_full_extension):
    # Automatic cast:
    num_vertices = int(num_vertices)
    seed = int(seed)
    # Generate collage instance
    instance = vcl.instances_generator(1, 1, num_vertices, seed)[0]
    # Generate selected output
    print(vcl.instance_to_str(instance, vcl.file_extension_to_format_name(file_full_extension)))

if __name__ == "__main__":
    from sys import argv
    #assert len(argv) == 5, 'Miss arguments'
    main(argv[1], argv[2], argv[3])
    exit(0)
