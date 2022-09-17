#!/usr/bin/env python3

from sys import stderr, exit, argv
import argparse
import sys
import random
import math
import networkx as nx

from datetime import datetime
from bot_lib import Bot

'''
print(f"""# I am a bot for the TALight problem `Vertex Cover`. Call me like this:
#     {argv[0]} -h
# if you want to know more about me (how to call me, my arguments and what I am supposed to do for you).
# My parameters for the current call are set as follows:
#   {args.minimum=}
#   {args.approx=}""")
'''

print(f"""# I am a bot for the TALight problem `Vertex Cover`. Call me like this:
#     {argv[0]} -h
# if you want to know more about me (how to call me, my arguments and what I am supposed to do for you).""")

# BOT = Bot(report_inputs=True,reprint_outputs=True)
BOT = Bot(report_inputs=False,reprint_outputs=False)

def calculate_bounds(graph):
  CurG = graph.copy()
  deg_list = list(CurG.degree())
  deg_list.sort(key=lambda tup: tup[1], reverse=True)

  i = 0
  sum_deg = 0
  S = [] # Lower bound
  VminS = []

  while sum_deg < CurG.number_of_edges() and i <= len(deg_list):
    sum_deg += deg_list[i][1]
    S.append(deg_list[i][0])
    i += 1 
 
  for v in list(CurG.nodes())[:]:
    if v not in S:
      VminS.append(v)
    else:
      CurG.remove_node(v)

  S_1 = S.copy() # Upper bound

  for v in list(CurG.nodes())[:]:
    if CurG.degree(v) > 0:
      S_1.append(v)
      CurG.remove_node(v)

  return len(S), S, len(S_1), S_1

while True:
  vertices,num_edges,weighted = map(int, BOT.input().split())
  #if weighted:
  #  weights = [int(i) for i in BOT.input().split()]
  graph = BOT.input()
  graph = graph.replace(', ',',').split()
  edges = [eval(t) for t in graph]

  G = nx.Graph()
  G.add_nodes_from([int(v) for v in range(vertices)])
  G.add_edges_from(edges)

  '''
  if weighted:
    i = 0
    for v in G.nodes():
      G.add_node(v, weight=weights[i])
      i += 1
  '''

  lb, S, ub, S_1 = calculate_bounds(G)

  BOT.print(lb)
  BOT.print(' '.join(map(str,S)))
  BOT.print(ub)
  BOT.print(' '.join(map(str,S_1)))

