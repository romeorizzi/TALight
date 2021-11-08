#!/usr/bin/env python3
from sys import stderr, exit
import networkx as nx
from networkx.algorithms.matching import max_weight_matching
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem = "tiling_mxn-boards_with_1x2-boards"
service = "is_tilable"
args_list = [('m',int), # Grid dimension
    ('n',int),
    ('h',int), # Tile dimension
    ('k',int),
    ('hint_type',str),
    ('num_piece',int),
    ('seed_of_the_tiling',int),

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
m = ENV['m']
n = ENV['n']
h = ENV['h']
k = ENV['k']
hint_type = ENV['hint_type'] # Ignored for now
num_piece = ENV['num_piece'] # Num pieces to show
seed_of_the_tiling = ENV['seed_of_the_tiling']
lang = ENV['lang']

def main():
    assert ENV['h'] == 1
    assert ENV['k'] == 2

    random.seed(seed_of_the_tiling, version=2)

    G = nx.Graph()
    G.add_nodes_from([(i,j) for i in range(m) for j in range(n)])
    
    # Random weighted
    G.add_edges_from([((i, j), (i, j + 1), {'weight': random.randint(MINW, MAXW)}) for i in range(m) for j in range(n - 1)])
    G.add_edges_from([((i, j), (i + 1, j), {'weight': random.randint(MINW, MAXW)}) for i in range(m - 1) for j in range(n)])

    M = max_weight_matching(G, maxcardinality=False, weight='weight')

    grid = [ ["X" for j in range(n) ] for i in range(m) ]

    shown = 0

    for u,v in M:
        if u[0] + u[1] > v[0] + v[1]:
            tmp = u
            u = v
            v = tmp     

        if u[0] == v[0]: # horizontal edge
            if (shown < num_piece):
                grid[u[0]][u[1]] = 'W'
                grid[v[0]][v[1]] = 'E'
            else:
                grid[u[0]][u[1]] = 'X'
                grid[v[0]][v[1]] = 'X'
        else: # vertical edge
            if (shown < num_pieces):
                grid[u[0]][u[1]] = 'N'
                grid[v[0]][v[1]] = 'S'
            else:
                grid[u[0]][u[1]] = 'X'
                grid[v[0]][v[1]] = 'X'

        shown = shown + 1

    print(m,n)
    if m * n % 2 == 0:
       for i in range(m):
          for j in range(n):
             print(grid[i][j],end="")
          print()    

if __name__ == "__main__":
    main()
