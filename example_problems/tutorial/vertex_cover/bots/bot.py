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
parser.add_argument('--minimum', action='store_true', help="Use this option to select the recursive solution method.")
parser.add_argument('--approx', action='store_true', help="Use this option to select the dynamic programming solution method.")
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
  vertices_list = [i for i in range(graph.number_of_nodes())]

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

    for e in list(curG.edges())[:]:
      if v in e and e not in visited:
        curG.remove_edge(e[0],e[1])
        visited.append(e)
      if v1 in e and e not in visited:
        curG.remove_edge(e[0],e[1])
        visited.append(e)

  size = len(c)

  return size, ' '.join(map(str,c))

while True:
  #num_vertices = int(BOT.input())
  graph = BOT.input()
  graph = graph.replace(', ',',').split()
  edges = [eval(t) for t in graph]

  G = nx.Graph()
  G.add_edges_from(edges)
  
  if args.minimum:
    size,answer = calculate_minimum_vc(G)
  elif args.approx:
    size,answer = calculate_approx_vc(G)
  else:
    size,answer = calculate_minimum_vc(G)
  
  BOT.print(size)
  BOT.print(answer)
