#!/usr/bin/env python3

from sys import stderr, exit, argv
import argparse
import sys
import random
import math
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

THRESHOLD = 80

# BOT = Bot(report_inputs=True,reprint_outputs=True)
BOT = Bot(report_inputs=False,reprint_outputs=False)

'''
 Metodi per il branch and bound
'''
def get_edges(graph):
  edges_list = []

  edges_list_str = graph[0].replace('}{',' ').replace('{','').replace('}','').split(' ')
  
  for e in edges_list_str:
    n = e.replace(',', ' ').split(' ')
    edges_list.append((int(n[0]),int(n[1])))

  return edges_list

def find_maxdeg(vertices, edges_list):
  deg_list = []

  for vi in vertices:
    deg = 0

    for edge in edges_list:
      if vi in edge:
        deg += 1

    deg_list.append((vi,deg))

  deg_list.sort(key=lambda tup: tup[1], reverse=True)
  v = deg_list[0]

  return v

def lowerbound(vertices, edges):
  #num_edges, _ = get_edges(graph)

  lb = math.ceil(len(edges) / find_maxdeg(vertices, edges)[1])

  return lb

def neighbours(v, edges):
  neighbour = []

  for e in edges:
    if v in e:
      if v == e[0]:
        neighbour.append(e[1])
      else:
        neighbour.append(e[0])

  return neighbour

def remove_node(node, list_edges, vertices_list):
  for e in list_edges[:]:
    if node in e:
      list_edges.remove(e)

  vertices_list.remove(node)

  return vertices_list, list_edges

def calculate_minimum_vc(num_vertices, graph):
  optVC = []
  curVC = []
  frontier = []
  neighbour = []

  G = get_edges(graph)
  curG = G.copy()
  vertices_list = [i for i in range(num_vertices)]

  upperbound = num_vertices
  v = find_maxdeg(vertices_list, curG)

  frontier.append((v[0], 0, (-1, -1)))
  frontier.append((v[0], 1, (-1, -1)))

  while frontier != [] :
    (vi, state, parent) = frontier.pop()
    backtrack = False

    if state == 0:
      neighbour = neighbours(vi, curG)

      for node in neighbour:
        curVC.append((node, 1))
        vertices_list, curG = remove_node(node, curG, vertices_list)

      
    elif state == 1: 
      vertices_list, curG = remove_node(vi, curG, vertices_list)

    else:
      pass

    curVC.append((vi, state)) 

    if len(curG) == 0: # Ho la soluzione
      if len(curVC) < upperbound:
        optVC = curVC.copy()
        upperbound = len(curVC)

      backtrack = True

    else:
      curLB = lowerbound(vertices_list, curG) + len(curVC)

      if(curLB < upperbound):
        vj = find_maxdeg(vertices_list, curG)
        frontier.append((vj[0], 0, (vi, state)))
        frontier.append((vj[0], 1, (vi, state)))
      else:
        backtrack = True

    if backtrack == True:
      if frontier != []:
        nextnode_parent = frontier[-1][2]

        if nextnode_parent in curVC:
          id = curVC.index(nextnode_parent) + 1

          while id < len(curVC):
            mynode, mystate = curVC.pop()
            
            ## Per qualche motivo mette dei doppioni, da qui l'if...
            if mynode not in vertices_list:
              vertices_list.append(mynode)

            curVC_nodes = list(map(lambda t:t[0], curVC))
            neighbourG = neighbours(mynode, G)

            for ng in neighbourG:
              if (ng in vertices_list) and (ng not in curVC_nodes):
                curG.append((mynode,ng))

        elif nextnode_parent == (-1, -1):
          curVC.clear()
          curVC = G.copy()
           
  res = []
  for n in optVC:
    res.append(n[0])

  res.sort()
  size = len(res)
 
  # return optVC
  return size, ' '.join(map(str,res))

def calculate_approx_vc(num_vertices, graph):
  G = get_edges(graph)
  curG = G.copy()
  curG.sort(key=lambda tup: tup[0])
  vertices_list = [i for i in range(num_vertices)]

  visited = []
  c = []

  while curG != []:
    v = find_maxdeg(vertices_list, curG)[0]
    neighbour = neighbours(v, curG)
    vertices_list.remove(v)
    
    v1 = find_maxdeg(neighbour, curG)[0]
    vertices_list.remove(v1)

    if v > v1:
      arco = (v1,v)
    else:
      arco = (v,v1)

    visited.append(arco)
    curG.remove(arco)

    c.append(v)
    c.append(v1)

    for e in curG[:]:
      if v in e and e not in visited:
        curG.remove(e)
        visited.append(e)
      if v1 in e and e not in visited:
        curG.remove(e)
        visited.append(e)

  size = len(c)

  return size, ' '.join(map(str,c))


while True:
  num_vertices = int(BOT.input())
  graph = BOT.input().split()

  if num_vertices < THRESHOLD:
    if args.minimum:
      size,answer = calculate_minimum_vc(num_vertices, graph)
    elif args.approx:
      size,answer = calculate_approx_vc(num_vertices, graph)
    else:
      size,answer = calculate_minimum_vc(num_vertices, graph)
  else:
    size,answer = calculate_approx_vc(num_vertices, graph)
  
  BOT.print(answer)
