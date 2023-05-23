#!/usr/bin/python3
import argparse
import networkx as nx
from networkx.algorithms.matching import max_weight_matching
import random
random.seed(777, version=2)
MINW = 0
MAXW = 10000

m = 20
n = 20

G = nx.Graph()
G.add_nodes_from([(i,j) for i in range(m) for j in range(n)])
G.add_edges_from([((i, j), (i, j + 1), {'weight': random.randint(MINW, MAXW)}) for i in range(m) for j in range(n - 1)]) # randomly weighted horizontal edges
G.add_edges_from([((i, j), (i + 1, j), {'weight': random.randint(MINW, MAXW)}) for i in range(m - 1) for j in range(n)]) # randomly weighted vertical edges
M = max_weight_matching(G, maxcardinality=False, weight='weight')

grid = [ ["X" for j in range(n) ] for i in range(m) ]

for u,v in M:
  if u[0] + u[1] > v[0] + v[1]:
    tmp = u
    u = v
    v = tmp
  if u[0] == v[0]: # horizontal edge
    grid[u[0]][u[1]] = 'W'
    grid[v[0]][v[1]] = 'E'
  else: # vertical edge
    grid[u[0]][u[1]] = 'N'
    grid[v[0]][v[1]] = 'S'

print(m,n)
if m * n % 2 == 0:
   for i in range(m):
      for j in range(n):
         print(grid[i][j],end="")
      print()

print()
