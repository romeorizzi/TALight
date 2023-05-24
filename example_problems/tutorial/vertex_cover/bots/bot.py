#!/usr/bin/env python3

from sys import stderr, exit, argv
import argparse
import sys
import random
import math
import networkx as nx

from datetime import datetime
from bot_lib import Bot

parser = argparse.ArgumentParser(description="I am a bot for the TALight problem `Vertex Cover`. In a never ending loop (until I get the '# WE HAVE FINISHED' line), I read an input instances from stdin and I write my answer for it on stdout.")
parser.add_argument('--minimum', action='store_true', help="Use this option to calculate a minimum vertex cover for the graph.")
parser.add_argument('--approx', action='store_true', help="Use this option to calculate a 2-approximated vertex cover for the graph.")
args = parser.parse_args()

print(f"""# I am a bot for the TALight problem `Vertex Cover`. Call me like this:
#     {argv[0]} -h
# if you want to know more about me (how to call me, my arguments and what I am supposed to do for you).
# My parameters for the current call are set as follows:
#   {args.minimum=}
#   {args.approx=}""")

# BOT = Bot(report_inputs=True,reprint_outputs=True)
BOT = Bot(report_inputs=False,reprint_outputs=False)

'''
 Metodi per il branch and bound
'''
def find_maxdeg(graph, vertices=None):
  if vertices == None:
    deg_list = list(graph.degree())
  else:
    deg_list = list(graph.degree(vertices))

  deg_list.sort(key=lambda tup: tup[1], reverse=True)

  v = deg_list[0]

  return v

def lowerbound(graph):
  lb=graph.number_of_edges() / find_maxdeg(graph)[1]
  lb=math.ceil(lb)

  return lb

'''
solutore vero e proprio: uso un algoritmo Branch and Bound
Liberamente tratto da https://github.com/arjunchint/Minimum-Vertex-Cover/blob/master/Code/BnB.py
'''
def calculate_minimum_vc(graph):
  OptVC = []
  CurVC = []
  Frontier = []
  neighbor = []

  UpperBound = graph.number_of_nodes()

  CurG = graph.copy()
  v = find_maxdeg(CurG)

  Frontier.append((v[0], 0, (-1, -1)))  # tuples of node,state,(parent vertex,parent vertex state)
  Frontier.append((v[0], 1, (-1, -1)))

  while Frontier!=[]:
    (vi,state,parent)=Frontier.pop()

    backtrack = False

    if state == 0:
      neighbor = CurG.neighbors(vi)
      for node in list(neighbor):
        CurVC.append((node, 1))
        CurG.remove_node(node)

    elif state == 1:
      CurG.remove_node(vi)

    else:
      pass

    CurVC.append((vi, state))
    CurVC_size = len(CurVC)

    if CurG.number_of_edges() == 0: # Ho la soluzione
      if CurVC_size < UpperBound:
        OptVC = CurVC.copy()
        UpperBound = CurVC_size

      backtrack = True

    else:
      CurLB = lowerbound(CurG) + CurVC_size

      if CurLB < UpperBound:
        vj = find_maxdeg(CurG)
        Frontier.append((vj[0], 0, (vi, state)))
        Frontier.append((vj[0], 1, (vi, state)))

      else:
        backtrack=True

    if backtrack==True:
      if Frontier != []:
        nextnode_parent = Frontier[-1][2]

        if nextnode_parent in CurVC:
          id = CurVC.index(nextnode_parent) + 1

          while id < len(CurVC):
            mynode, mystate = CurVC.pop()
            CurG.add_node(mynode) #undo the deletion from CurG

            curVC_nodes = list(map(lambda t:t[0], CurVC))
            for nd in graph.neighbors(mynode):
              if (nd in CurG.nodes()) and (nd not in curVC_nodes):
                CurG.add_edge(nd, mynode)

        elif nextnode_parent == (-1, -1):
          # backtrack to the root node
          CurVC.clear()
          CurG = graph.copy()
        else:
          print('error in backtracking step')

  res = []

  for n in OptVC:
    res.append(n[0])

  res.sort()
  size = len(res)

  # return OptVC
  return size, ' '.join(map(str,res))

def calculate_approx_vc(graph, mode='random'):
  curG = graph.copy()

  visited = []
  c = []
  max_matching = []
  #vertices_list = [i for i in range(graph.number_of_nodes())]
  vertices_list = [i for i in list(graph.nodes())]

  while curG.number_of_edges() != 0:
    if mode == 'greedy':
      v = find_maxdeg(curG, vertices_list)[0]
      neighbour = curG.neighbors(v)
      vertices_list.remove(v)

      v1 = find_maxdeg(curG,neighbour)[0]
      vertices_list.remove(v1)

      arco = (v,v1)
      arco = tuple(sorted(arco))

    ## Prendo un arco casualmente
    elif mode == 'random':
      random.seed(datetime.now())

      edges = list(curG.edges())
      i = random.randint(0, curG.number_of_edges() - 1)

      arco = edges[i]
      arco = tuple(sorted(arco))

      v = arco[0]
      v1 = arco[1]

    visited.append(arco)
    curG.remove_edge(v,v1)

    c.append(v)
    c.append(v1)

    max_matching.append((v,v1))

    for e in list(curG.edges())[:]:
      if v in e and e not in visited:
        curG.remove_edge(e[0],e[1])
        visited.append(e)
      if v1 in e and e not in visited:
        curG.remove_edge(e[0],e[1])
        visited.append(e)

  size = len(c)

  return size, ' '.join(map(str,c))

'''
Calcolo il vertex cover esatto su un grafo pesato. Non essendoci
algoritmi "buoni" ed essendo estremamente complicato definire un
lower bound per adattare l'algoritmo branch and bound per grafi
non pesati, ricorro alle riduzioni tra problemi: calcolo la 
massima clique sul grafo complementare, la quale sarà anche un
massimo independet set per il grafo principale. Gli archi che non
fanno parte del massimo independent set saranno il mio vertex
cover di peso minimo
'''
def calculate_minimum_weight_vc(graph):
  weights = []
  vc = []

  for n,w in nx.get_node_attributes(graph, 'weight').items():
    weights.append(w)

  G_1 = nx.complement(graph)

  # Per qualche motivo facendo il grafo complementare perdo
  # i pesi sui nodi e devo rimettercel a mano...
  i = 0
  for v in G_1.nodes():
    G_1.add_node(v, weight=weights[i])
    i += 1

  # max_weight_clique() utilizza anch'esso un algoritmo
  # di branch and bound per trovare la clique di peso 
  # massimo
  clique, w_clique = nx.max_weight_clique(G_1)

  for v in graph.nodes():
    if v not in clique:
      vc.append(v)

  size_vc = len(vc)
  weight_vc = sum(weights) - w_clique

  return ' '.join(map(str, vc)), size_vc, weight_vc

'''
Calcolo una 2-approssimazione per il grafo pesato
'''
def calculate_weighted_approx_vc(graph):
  appr_sol = nx.approximation.min_weighted_vertex_cover(graph, weight='weight')
  size_sol = len(appr_sol)

  weight_sol = 0

  for n,w in nx.get_node_attributes(graph, 'weight').items():
    if n in appr_sol:
      weight_sol += w

  return ' '.join(map(str, appr_sol)), size_sol, weight_sol


while True:
  vertices,num_edges,weighted = map(int, BOT.input().split())
  if weighted:
    weights = [int(i) for i in BOT.input().split()]
  graph = BOT.input()
  graph = graph.replace(', ',',').split()
  edges = [eval(t) for t in graph]

  G = nx.Graph()
  G.add_nodes_from([int(v) for v in range(vertices)])
  G.add_edges_from(edges)

  if weighted:
    i = 0
    for v in sorted(G.nodes()):
      G.add_node(v, weight=weights[i])
      i += 1
  
  if args.minimum:
    if not weighted:
      size,answer = calculate_minimum_vc(G)
      weight = 0
    else:
      answer,size,weight = calculate_minimum_weight_vc(G)
  elif args.approx:
    if not weighted:
      size,answer = calculate_approx_vc(G)
      weight = 0
    else:
      answer,size,weight = calculate_weighted_approx_vc(G)
  else:
    size,answer = calculate_minimum_vc(G)
 
  BOT.print(size)
  BOT.print(answer)
  if weighted:
    BOT.print(weight) 
