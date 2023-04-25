#!/usr/bin/env python3
from sys import stderr

from matita_lib import Matita_Graph

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        G = Matita_Graph()
        G.load_from_stdin(input_node_names_start_from = 1)
        #G.display(node_names_starting_from = 1, out = stderr)
        G.solve_matita()
