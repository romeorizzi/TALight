#!/usr/bin/env python3
import os
import sys
import random
import math
import networkx as nx
import matplotlib.pyplot as plt

from random import randint
from datetime import datetime
from termcolor import colored
from contextlib import redirect_stdout
from networkx.algorithms import approximation

AVAILABLE_FORMATS = {'instance':{'simple':'simple.txt', 'with_info':'with_info.txt', 'vc_dat':'.dat'},'solution':{'exact_sol': 'exact_sol.txt', 'approx_sol':'approx_sol.txt'}}
DEFAULT_INSTANCE_FORMAT='with_info'
DEFAULT_SOLUTION_FORMAT='exact_sol'

def format_name_to_file_extension(format_name, format_gender):
    assert format_gender in AVAILABLE_FORMATS, f'No format has been adopted for objects of the gender `{format_gender}`.'
    assert format_name in AVAILABLE_FORMATS[format_gender], f'Format_name `{format_name}` unsupported for objects of gender {format_gender}.'
    return AVAILABLE_FORMATS[format_gender][format_name]

def file_extension_to_format_name(file_extension):
    for format_gender in AVAILABLE_FORMATS:
        for format_name in AVAILABLE_FORMATS[format_gender]:
            if AVAILABLE_FORMATS[format_gender][format_name] == file_extension:
                return format_name
    assert False, f'No adopted format is associated to the file_extension `{file_extension}`.'

def format_name_expand(format_name, format_gender):
    long_format_name = format_name_to_file_extension(format_name, format_gender)
    format_list = long_format_name.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = None
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    return format_primary, format_secondary


'''  
  GENERATORE DI ISTANZE 
'''
def instance_to_str(instance, format_name=DEFAULT_INSTANCE_FORMAT):
    """This function returns the string representation of the given <instance> provided in format <instance_format_name>"""
    format_primary, format_secondary = format_name_expand(format_name, 'instance')
    if format_primary == 'dat':
        return instance_to_dat_str(instance, format_name)
    if format_primary == 'txt':
        return instance_to_txt_str(instance, format_name)

def instance_to_txt_str(instance, format_name="with_info"):
    """Of the given <instance>, this function returns the .txt string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    output= f''

    if format_name == "with_info":
      num_vertices = instance['num_vertices']
      num_edges = instance['graph'].number_of_edges()
      if 'weighted' not in instance:
        instance['weighted'] = 0
      weighted = int(instance['weighted'])
      output += f'{num_vertices} {num_edges} {weighted}\n'

    if instance['weighted']:
      for n,w in sorted(nx.get_node_attributes(instance['graph'], 'weight').items()):
        output += f'{w} '
      output += '\n'
    elif not instance['weighted'] and format_name == "simple":
      output += '\n'
      
    graph = instance['graph'].edges()

    output += f'{"".join(map(str, graph))}\n'

    if 'risp' in instance:
      if 'exact_sol' in instance:
        if instance['exact_sol'] == 1:
          output += '1\n'
        else:
          output += '0\n'

      output += f'{instance["risp"]}\n'
      
      if 'risp_weight' in instance:
        output += f'{instance["risp_weight"]}\n'

    #output += '\n'

    return output

def get_instance_from_str(instance_as_str, instance_format_name=DEFAULT_INSTANCE_FORMAT):
    """This function returns the instance it gets from its string representation as provided in format <instance_format_name>."""
    format_primary, format_secondary = format_name_expand(instance_format_name, 'instance')
    if format_primary == 'dat':
       return get_instance_from_dat(instance_as_str, instance_format_name)
    if format_primary == 'txt':
      return get_instance_from_txt(instance_as_str, instance_format_name)

def get_instance_from_txt(instance_as_str, format_name):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
    instance = {}

    str_to_arr = instance_as_str.split('\n')

    if str_to_arr[0] == '':
      instance['weighted'] = 0
    else:
      instance['weighted'] = 1

    G = nx.Graph()

    if format_name != "with_info":
      if instance['weighted']:
        weights = str_to_arr[0].split()
        G.add_nodes_from([i for i in range(len(weights))])
        edges = str_to_arr[1].replace(', ', ',').replace(')(',') (').split()
      else:
        edges = str_to_arr[1].replace(', ', ',').replace(')(',') (').split()

      edges = [eval (t) for t in edges]
      G.add_edges_from(edges)

      i = 0
      for v in sorted(G.nodes()):
        if instance['weighted']:
          G.add_node(v, weight=weights[v])
        else:
          G.add_node(v, weight=1)
        i += 1

      instance['graph'] = G
      instance['num_vertices'] = len([v for v in list(G.nodes())])

      instance['exact_sol'] = int(str_to_arr[2])
      instance['sol'] = str_to_arr[3]
      
      if instance['weighted']:
        instance['sol_weight'] = str_to_arr[4]

    else:
      v_e_w_split = str_to_arr[0].split(' ')
      instance['num_vertices'] = int(v_e_w_split[0])
      instance['num_edges'] = int(v_e_w_split[1])
      instance['weighted'] = int(v_e_w_split[2])
      
      if instance['weighted']:
        weights = [int(w) for w in str_to_arr[1].split()]
        edges = str_to_arr[2].replace(', ', ',').replace(')(',') (').split()
      else:
        edges = str_to_arr[1].replace(', ', ',').replace(')(',') (').split()
      edges = [eval (t) for t in edges]

      G.add_edges_from(edges)
      G.add_nodes_from([int(n) for n in range(instance['num_vertices'])])

      i = 0
      for v in sorted(G.nodes()):
        if instance['weighted']:
          G.add_node(v, weight=weights[i])
        else:
          G.add_node(v, weight=1)
        i = i+1

      instance['graph'] = G

      if instance['weighted']:
        instance['exact_sol'] = int(str_to_arr[3])
        instance['sol'] = str_to_arr[4]
        instance['sol_weight'] = str_to_arr[5]
      else:
        instance['exact_sol'] = int(str_to_arr[2])
        if instance['exact_sol']:
          instance['sol'] = str_to_arr[3]
        else:
          instance['sol'] = f'{str_to_arr[3]}\n{str_to_arr[4]}'
    
    return instance

'''
Aggiorna la soluzione approssimata nel caso in cui l'utente ne abbia trovata
una migliore rispetto a quella memorizzata nell'istanza
'''
def update_instance_txt(path, file, new_data, weighted=0):
  for format_gender in AVAILABLE_FORMATS['instance']:
    format_name = AVAILABLE_FORMATS['instance'][format_gender]
    if format_name.split('.')[1] == 'txt':
      instance_filename = f'{file}.{format_name}'
      full_path = os.path.join(path, instance_filename)

      lines = open(full_path, 'r').readlines()

      if weighted:
        #lines[-2] = f'{new_data}\n'
        lines[-3] = f'{new_data}\n'
      else:
        lines[-3:-1] = f'{new_data}\n'

      open(full_path, 'w').writelines(lines)

'''
DAT
'''
def instance_to_dat_str(instance,format_name='vc_dat'):
  """Of the given <instance>, this function returns the .dat string in format <format_name>"""
  assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
  graph = instance['graph']
  num_vertices = instance['num_vertices']
  num_edges = instance['num_edges']
  weighted = instance['weighted']

  output = f"param num_vertices := {num_vertices};            # Number of vertices in the graph\n"
  output += f"param num_edges := {num_edges};                 # Number of edges in the graph\n"
  output += f"param weighted := {weighted};                   # Weighted graph or not\n"
  output += "param: EDGES OF THE GRAPH "
  output += f":= {list(graph.edges())};\n"

  if weighted == 1:
    weights = []

    for n,w in nx.get_node_attributes(graph, 'weight').items():
      weights.append(w)

    output += f'param weights := {weights}'

  if 'risp' in instance:
      if 'exact_sol' in instance:
        if instance['exact_sol'] == 1:
          output += f'param exact_sol := 1\n'
        else:
          output += f'param exact_sol := 0\n'

      output += f'param sol := {instance["risp"]}\n'
  #output += f":= {''.join(map(str, graph.edges()))} "
  output += "end;"
    
  return output

def get_instance_from_dat(instance_as_str, format_name):
  """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
  assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
  split_instance = instance_as_str.split(";")
  instance = {}

  instance['num_vertices'] = int(get_param(split_instance[0])) # assign num_vertices
  instance['num_edges'] = int(get_param(split_instance[1])) # assign num_edges
  instance['weighted'] = int(get_param(split_instance[2])) # assign num_edges

  if not instance['weighted']:
    edges = list(ast.literal_eval(get_param(split_instance[3]).replace("] [","],[").replace(", ",",").replace(')(',') ('))) # DA VERIFICARE!
  else:
    weights = list(ast.literal_eval(get_param(split_instance[3]).replace("] [","],["))) # DA VERIFICARE!
    edges = list(ast.literal_eval(get_param(split_instance[4]).replace("] [","],[").replace(", ",",").replace(')(',') ('))) # DA VERIFICARE!

  G = nx.Graph()
  G.add_nodes_from([c for v in range(instance['num_vertices'])])

  if instance['weighted']:
    i = 0
    for v in G.nodes():
      G.add_node(v, weight=weights[i])
      i = i+1

  G.add_edges_from(edges)
  instance['graph'] = G

  return instance


'''
GENERATORE GRAFI
'''
def instances_generator(num_instances, scaling_factor: float, num_vertices: int, num_edges: int, seed = "random_seed", weighted = 0):
  instances = []

  for _ in range(num_instances):
    instance = {}
    if seed == "random_seed":
      seed = random.randint(100000,999999)

    instance['num_vertices'] = num_vertices
    instance['num_edges'] = num_edges
    instance['graph'] = random_graph(num_vertices, num_edges, seed, weighted)
    instance['seed'] = seed
    instance['weighted'] = weighted

    num_vertices = math.ceil(scaling_factor * num_vertices)
    num_edges = math.ceil(scaling_factor * num_edges)

    instance['measured_time'] = None
    instance['answer_correct'] = None

    instances.append(instance)

  return instances

def random_graph(num_vertices, num_edges, seed, weighted):
  random.seed(seed)

  G = nx.gnm_random_graph(num_vertices, num_edges, seed)

  # Aggiungo un peso ai nodi (1 se non viene specificato nulla
  for n in G.nodes():
    if weighted == 1:
      G.add_node(n, weight=random.randint(1,10))
    else:
      G.add_node(n, weight=1)

  # L'idea era di controllare se ci sono nodi non connessi e,
  # nel caso, rigenerare il grafo. Il problema è però il seed,
  # che va cambiato e quindi rende non replicabile il grafo...
  #while nx.number_of_isolates(G) != 0:
  #  G = nx.gnm_random_graph(num_vertices, num_edges, seed)
    
  return G

'''
Stampa l'istanza del grafo per le eval
'''
def print_graph(num_vertices, num_edges, graph, weighted=0, instance_format=DEFAULT_INSTANCE_FORMAT):
  print(f'{num_vertices} {num_edges} {weighted}')

  if weighted:
    weights = []

    for n,w in nx.get_node_attributes(graph, 'weight').items():
      weights.append(w)

    print(f'{" ".join(map(str,weights))}')

  edges = list(graph.edges())
  print(f'{" ".join(map(str,edges))}')


'''
SOLUTORI
'''
def solutions(sol_type,instance,instance_format=DEFAULT_INSTANCE_FORMAT):
  sols = {}

  VMAX = 80

  if sol_type == 'minimum':
    if 'exact_sol' in instance:
      if instance['exact_sol'] == 0:
        sols['calculate_minimum_vc'] = 'Instance too big! Please, use approximation.'
        return sols

    else:
      if instance['num_vertices'] <= VMAX:
        if not instance['weighted']:
          size, vc = calculate_minimum_vc(instance['graph'])
          sols['calculate_minimum_vc'] = f"{vc}"
          sols['vertex_cover_size'] = f"{size}"
        else:
          vc, size, weight = calculate_minimum_weight_vc(instance['graph'])
          sols['calculate_minimum_weight_vc'] = f"{vc}"
          sols['calculate_minimum_weight_vc_size'] = f"{size}"
          sols['calculate_minimum_weight_vc_weight'] = f"{weight}"
      else:
        sols['calculate_minimum_vc'] = 'Instance too big! Please, use approximation.'

  elif sol_type == 'approx':
    if not instance['weighted']:
      size, vc, max_matching = calculate_approx_vc(instance['graph'])
      sols['calculate_approx_vc'] = f"{vc}"
      sols['calculate_2-approx_vc_matching'] = f"{max_matching}"
    else:
      vc, size, weight = calculate_weighted_approx_vc(instance['graph'])
      sols['calculate_weighted_approx_vc'] = f"{vc}"
      sols['calculate_weighted_approx_vc_size'] = f"{size}"
      sols['calculate_weighted_approx_vc_weight'] = f"{weight}"

  elif sol_type == 'both':
    # Caso di istanza da catalogo
    if 'exact_sol' in instance:
      if instance['exact_sol'] == 1:
        size_min, vc_min = calculate_minimum_vc(instance['graph'])
        sols['calculate_minimum_vc'] = f"{vc_min}"
        sols['calculate_minimum_vc_size'] = f"{size_min}"

      size_appr, vc_appr, max_matching = calculate_approx_vc(instance['graph'], 'greedy')
      sols['calculate_2-approx_vc'] = f"{vc_appr}"
      sols['calculate_2-approx_vc_matching'] = f"{max_matching}"

    # Istanza random
    else:
      if int(instance['num_vertices']) <= VMAX:
        if not instance['weighted']:
          size_min, vc_min = calculate_minimum_vc(instance['graph'])
          sols['calculate_minimum_vc'] = f"{vc_min}"
          sols['vertex_cover_size'] = f"{size_min}"
        else:
          vc, size, weight = calculate_minimum_weight_vc(instance['graph'])
          sols['calculate_minimum_weight_vc'] = f"{vc}"
          sols['calculate_weighted_vc_size'] = f"{size}"
          sols['calculate_weighted_vc_weight'] = f"{weight}"
      else:
        sols['calculate_minimum_vc'] = 'Instance too big! Please, use approximation.'

      if not instance['weighted']:
        size_appr, vc_appr, max_matching = calculate_approx_vc(instance['graph'], 'greedy')
        sols['calculate_2-approx_vc'] = f"{vc_appr}"
        sols['calculate_2-approx_vc_matching'] = f"{max_matching}"
      else:
        vc_appr, size_appr, weight_appr = calculate_weighted_approx_vc(instance['graph'])
        sols['calculate_weighted_approx_vc'] = f"{vc_appr}"
        sols['calculate_weighted_approx_vc_size'] = f"{size_appr}"
        sols['calculate_weighted_approx_vc_weight'] = f"{weight_appr}"

  return sols

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
Calcolo una 2-approssimazione del VC. La scelta dell'arco è greedy,
Quindi in teoria dovrei avere sempre la miglior approssimazione
possibile...
'''
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
    curG.remove_node(v)
    curG.remove_node(v1)

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
  c.sort()

  return size, ' '.join(map(str,c)), ' '.join(map(str, max_matching))

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

  
## Verifico se un vertex cover fornito in input è un vc valido per il grafo
def verify_vc(vertices, graph, ret_edges=0):
  edges_list = list(graph.edges())
  vertices = list(map(int, vertices))

  # Scorro una copia della lista
  for e in edges_list[:]:
    for v in vertices:
      if v in e:
        edges_list.remove(e)
        break

  if(len(edges_list) > 0):
    if not ret_edges:
      return 0
    else:
      return 0, edges_list
  else:
    if not ret_edges:
      return 1
    else:
      return 1, edges_list

## Verifico se il vc approssimato fornito dall'utente è tale
def verify_approx_vc(matching, graph, ret_edges=0):
  curG = graph.copy()
  #max_matching = [eval(t) for t in matching]
  max_matching = matching
  
  visited = []
  
  for e in max_matching:
    e = tuple(sorted(e))
    if e not in visited:
      curG.remove_edge(e[0],e[1])
    else: 
      if ret_edges == 1:
        return 0, 1, e
      else:
        return 0

    for v in e:
      for e1 in list(curG.edges())[:]:
        if v in e1 and e1 not in visited:
          curG.remove_edge(e1[0],e1[1])
          visited.append(e1)

  if curG.number_of_edges() != 0:
    if ret_edges == 1:
      return 0, 2, curG.edges()
    else:
      return 0

  for e in max_matching:
    for v in e:
      if v in visited:
        if ret_edges == 1:
          return 0, 3, v
        else:
          return 0

  if ret_edges == 1:
    return 1, 0, []
  else:
    return 1

'''
VARIE: PLOT
'''
def plot_graph(graph, weighted=0):
  pos = nx.spring_layout(graph, seed=3113794652)
  #nx.draw_networkx(graph,pos,node_size=500,width=2,with_labels=True)
  if not weighted:
    nx.draw_networkx(graph,pos,node_color='#00b4d9',node_size=500,width=2,with_labels=True)
  else:
    labels = nx.get_node_attributes(graph, 'weight')
    nx.draw_networkx(graph,pos,node_color='#00b4d9',node_size=500,width=2,with_labels=True)
    for v in graph.nodes():
      x,y=pos[v]
      plt.text(x,y+0.15,s=labels[v], bbox=dict(facecolor='white', alpha=0.5),horizontalalignment='center')
  ax = plt.gca()
  ax.set_title('Graph')
  ax.margins(0.20)
  plt.axis("off")

  plt.show()
 
def plot_mvc(graph, vertices, edges, weighted=0, approx=0):
  pos = nx.spring_layout(graph, seed=3113794652)
  vertices = [int(i) for i in vertices.split()]
  v_color_map = []
  e_color_map = []

  for node in graph.nodes():
    if node in vertices:
      v_color_map.append('red')
    else:
      v_color_map.append('#00b4d9')

  for e in graph.edges():
    if e in edges:
      e_color_map.append('black')
    else:
      e_color_map.append('lightgrey')

  if not weighted:
    nx.draw_networkx(graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)
  else:
    labels = nx.get_node_attributes(graph, 'weight') 
    nx.draw_networkx(graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)
    for v in graph.nodes():
      x,y=pos[v]
      plt.text(x,y+0.15,s=labels[v], bbox=dict(facecolor='white', alpha=0.5),horizontalalignment='center')

  ax = plt.gca()

  if not weighted:
    ax.set_title('Minimum Vertex Cover (red nodes)')
  else:
    if approx == 0:
      ax.set_title('Minimum Weight Vertex Cover (red nodes)')
    else:
      ax.set_title('2-Approximated Minimum Weight Vertex Cover (red nodes)')

  ax.margins(0.20)
  plt.axis("off")

  plt.show()

def plot_2app_vc(graph, vertices, edges):
  pos = nx.spring_layout(graph, seed=3113794652)
  vertices = [int(i) for i in vertices.split()]
  v_color_map = []
  e_color_map = []
  for node in graph.nodes():
    if node in vertices:
      v_color_map.append('red')
    else:
      v_color_map.append('#00b4d9')
  #edges = edges.replace(', ', ',')
  #edges = [eval(t) for t in edges.split()]
  edges = [tuple(sorted(t)) for t in edges]
  for e in graph.edges():
    if e in edges:
      #e_color_map.append('red')
      e_color_map.append('black')
    else:
      e_color_map.append('lightgrey')
  nx.draw_networkx(graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)            
  ax = plt.gca()
  ax.set_title('2-approximated Vertex Cover')
  ax.margins(0.20)
  plt.axis("off")

  plt.show()

def plot_indset(graph, vertices, edges, weighted=0):
  pos = nx.spring_layout(graph, seed=3113794652)
  vertices = [int(i) for i in vertices.split()]
  v_color_map = []
  e_color_map = []

  for node in graph.nodes():
    if node in vertices:
      v_color_map.append('red')
    else:
      v_color_map.append('#00b4d9')

  for e in graph.edges():
    if e in edges:
      e_color_map.append('black')
    else:
      e_color_map.append('lightgrey')

  if not weighted:
    nx.draw_networkx(graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)
  else:
    labels = nx.get_node_attributes(graph, 'weight')
    nx.draw_networkx(graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)
    for v in graph.nodes():
      x,y=pos[v]
      plt.text(x,y+0.15,s=labels[v], bbox=dict(facecolor='white', alpha=0.5),horizontalalignment='center')

  ax = plt.gca()

  if not weighted:
    ax.set_title('Maximum Independent Set (red nodes)')
  else:
    ax.set_title('Maximum Weight Independent Set (red nodes)')

  ax.margins(0.20)
  plt.axis("off")

  plt.show()

'''
GOAL SUMMARIES
'''
def print_goal_summary(goal,testcases,num_testcases_passed,num_testcases_correct_ans,num_testcases_wrong_ans,out_of_time, TAc,LANG):
  TAc.print(LANG.render_feedback("summary", f'\n# SUMMARY OF THE RESULTS FOR GOAL "{goal}":\n'), "white", ["bold"])

  for t,i in zip(testcases,range(1,1+len(testcases))):
    if t['answer_correct'] == True:
      TAc.print(LANG.render_feedback("right-ans", f'# TestCase {i}: Correct answer! Took time {t["measured_time"]} on your machine.\n'), "green")
    elif t['answer_correct'] == False:
      TAc.print(LANG.render_feedback("wrong-ans", f'# NO! You gave the wrong solution for the instance with this parameters:\n#num_vertices = {t["num_vertices"]}, num_edges={t["num_edges"]}, seed = {t["seed"]}.\n'), "yellow")
    else:
      TAc.print(LANG.render_feedback("out-of-time-ans", f'# The evaluation has been stopped since your solution took too much time on this or previous instances. The parameters of this instance are:\n#num_vertices = {t["num_vertices"]}, seed = {t["seed"]}.\n'), "white")
       
  if num_testcases_passed == len(testcases):
    TAc.print(LANG.render_feedback("right-in-time", f'# OK! Your solution achieved goal "{goal}".\n'), "green")

  if out_of_time > 0 and num_testcases_wrong_ans == 0:
    TAc.print(LANG.render_feedback("right-not-in-time", f'# OK! Though all answers produced by your solution are correct, still it exceeded the time limit on some instances. As such, you did not achieve goal "{goal}".\n'), "yellow")
  elif num_testcases_wrong_ans != 0:
    TAc.print(LANG.render_feedback("wrong-answ", f'# NO! Your solution gave wrong answers on at least one instance. Your solution does NOT achieve goal "{goal}".\n'), "red")

def print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG):    
  TAc.print(LANG.render_feedback('summary-of-results', '# SUMMARY OF RESULTS:'), 'green')
  num_instances = {}
  num_instances_passed = {}
  num_instances_correct_ans = {}
  num_instances_wrong_ans = {}
  alive = True

  for goal in goals:
      num_instances[goal] = len(instances[goal])
      num_instances_passed[goal] = 0
      num_instances_correct_ans[goal] = 0
      num_instances_wrong_ans[goal] = 0

      for instance in instances[goal]:
        if instance['answer_correct'] == False:
          num_instances_wrong_ans[goal] += 1
        elif instance['answer_correct'] == True:
          num_instances_correct_ans[goal] += 1

          if instance['measured_time'] <= MAX_TIME:
            num_instances_passed[goal] += 1

      if alive:
        print_goal_summary(goal,instances[goal],num_instances_passed[goal],num_instances_correct_ans[goal],num_instances_wrong_ans[goal], out_of_time, TAc,LANG)

      if num_instances_passed[goal] < num_instances[goal]:
        alive = False

  TAc.print(LANG.render_feedback('short-summary-of-results', '# SUMMARY OF RESULTS:'), 'green')

  for goal in goals:
    if num_instances_passed[goal] == num_instances[goal]:
      TAc.print(LANG.render_feedback('goal-passed', f'# Goal {goal}: PASSED (passed instances: {num_instances_passed[goal]}/{num_instances[goal]} instances)'), 'green', ['bold'])
    else:
      TAc.print(LANG.render_feedback('goal-NOT-passed', f'# Goal {goal}: NOT passed (passed instances: {num_instances_passed[goal]}/{num_instances[goal]} instances, correct answers: {num_instances_correct_ans[goal]}/{num_instances[goal]}, wrong answers: {num_instances_wrong_ans[goal]}/{num_instances[goal]} instances)'), 'red', ['bold'])
  
  TAc.print(f"\n# WE HAVE FINISHED", "white")
