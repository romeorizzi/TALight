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

AVAILABLE_FORMATS = {'instance':{'simple':'simple.txt', 'with_vertices':'with_vertices.txt', 'vc_dat':'.dat'},'solution':{'all_solutions': 'all_solutions.txt'}}
DEFAULT_INSTANCE_FORMAT='with_vertices'
DEFAULT_SOLUTION_FORMAT='all_solutions'

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

def instance_to_txt_str(instance, format_name="with_vertices"):
    """Of the given <instance>, this function returns the .txt string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    output= f''

    if format_name == "with_vertices":
      num_vertices = instance['num_vertices']
      num_edges = instance['graph'].number_of_edges()
      output += f'{num_vertices} {num_edges}\n'

    graph = instance['graph'].edges()

    output += f'{"".join(map(str, graph))}\n'

    if 'risp' in instance:
      if 'exact_sol' in instance:
        if instance['exact_sol'] == 1:
          output += '1\n'
        else:
          output += '0\n'

      output += f'{instance["risp"]}'

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

    if format_name != "with_vertices":
      edges = str_to_arr[0].replace(', ', ',').replace(')(',') (').split()
      edges = [eval (t) for t in edges]
      G = nx.Graph()
      G.add_edges_from(edges)
      instance['graph'] = G
      instance['num_vertices'] = len([v for v in list(G.nodes())])
      instance['exact_sol'] = int(str_to_arr[1])
      instance['sol'] = str_to_arr[2]

    else:
      v_e_split = str_to_arr[0].split(' ')
      instance['num_vertices'] = int(v_e_split[0])
      instance['num_edges'] = int(v_e_split[1])
      
      edges = str_to_arr[1].replace(', ', ',').replace(')(',') (').split()
      edges = [eval (t) for t in edges]
      G = nx.Graph()
      G.add_nodes_from([int(n) for n in range(instance['num_vertices'])])
      G.add_edges_from(edges)
      instance['graph'] = G
      instance['exact_sol'] = int(str_to_arr[2])
      instance['sol'] = str_to_arr[3]
    
    return instance

def update_instance_txt(path, file, new_data):
  for format_gender in AVAILABLE_FORMATS['instance']:
    format_name = AVAILABLE_FORMATS['instance'][format_gender]
    if format_name.split('.')[1] == 'txt':
      instance_filename = f'{file}.{format_name}'
      full_path = os.path.join(path, instance_filename)

      lines = open(full_path, 'r').readlines()
      lines[-2] = f'{new_data}\n'
      open(full_path, 'w').writelines(lines)

# Da rivedere per VC
def instance_to_dat_str(instance,format_name='vc_dat'):
  """Of the given <instance>, this function returns the .dat string in format <format_name>"""
  assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
  graph = instance['graph']
  num_vertices = instance['num_vertices']
  num_edges = instance['num_edges']

  output = f"param num_vertices := {num_vertices};            # Number of vertices in the graph\n"
  output += f"param num_edges := {num_edges};                 # Number of edges in the graph\n"
  output += "param: EDGES OF THE GRAPH "
  output += f":= {list(graph.edges())};\n"
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
  edges = list(ast.literal_eval(get_param(split_instance[2]).replace("] [","],[").replace(", ",",").replace(')(',') ('))) # DA VERIFICARE!

  G = nx.Graph()
  G.add_nodes_from([c for v in range(instance['num_vertices'])])
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

    num_vertices = math.ceil(scaling_factor * num_vertices)
    num_edges = math.ceil(scaling_factor * num_edges)

    instance['measured_time'] = None
    instance['answer_correct'] = None

    instances.append(instance)

  return instances

def random_graph(num_vertices, num_edges, seed, weighted):
  random.seed(seed)

  G = nx.gnm_random_graph(num_vertices, num_edges, seed)

  # Aggiungo un peso ai nodi
  if weighted == 1:
    for n in G.nodes():
      G.add_node(n, weight=random.randint(1,10))

  # L'idea era di controllare se ci sono nodi non connessi e,
  # nel caso, rigenerare il grafo. Il problema è però il seed,
  # che va cambiato e quindi rende non replicabile il grafo...
  #while nx.number_of_isolates(G) != 0:
  #  G = nx.gnm_random_graph(num_vertices, num_edges, seed)
    
  return G

def print_graph(num_vertices, num_edges, graph, instance_format=DEFAULT_INSTANCE_FORMAT):
  print(f'{num_vertices} {num_edges}')
  print(f'{" ".join(map(str,graph))}')


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
        size, vc = calculate_minimum_vc(instance['graph'])
        sols['calculate_minimum_vc'] = f"{vc}"
        sols['vertex_cover_size'] = f"{size}"
      else:
        sols['calculate_minimum_vc'] = 'Instance too big! Please, use approximation.'

  elif sol_type == 'approx':
    size, vc, max_matching = calculate_approx_vc(instance['graph'])
    #vc1 = nx.approximation.min_weighted_vertex_cover(instance['graph'])
    sols['calculate_approx_vc'] = f"{vc}"
    sols['calculate_2-approx_vc_matching'] = f"{max_matching}"

  elif sol_type == 'both':
    # Caso di istanza da catalogo
    if 'exact_sol' in instance:
      if instance['exact_sol'] == 1:
        size_min, vc_min = calculate_minimum_vc(instance['graph'])
        sols['calculate_minimum_vc'] = f"{vc_min}"
        sols['vertex_cover_size'] = f"{size_min}"

      size_appr, vc_appr, max_matching = calculate_approx_vc(instance['graph'], 'greedy')
      sols['calculate_2-approx_vc'] = f"{vc_appr}"
      sols['calculate_2-approx_vc_matching'] = f"{max_matching}"

    # Istanza random
    else:
      if int(instance['num_vertices']) <= VMAX:
        size_min, vc_min = calculate_minimum_vc(instance['graph'])
        sols['calculate_minimum_vc'] = f"{vc_min}"
        sols['vertex_cover_size'] = f"{size_min}"
      else:
        sols['calculate_minimum_vc'] = 'Instance too big! Please, use approximation.'

      size_appr, vc_appr, max_matching = calculate_approx_vc(instance['graph'], 'greedy')

      sols['calculate_2-approx_vc'] = f"{vc_appr}"
      sols['calculate_2-approx_vc_matching'] = f"{max_matching}"

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

## Calcolo una 2-approssimazione del VC. La scelta dell'arco è greedy,
## Quindi in teoria dovrei avere sempre la miglior approssimazione
## possibile...
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

  return size, ' '.join(map(str,c)), ' '.join(map(str, max_matching))

## Verifico se un vertex cover fornito in input è un vc valido per il grafo
def verify_vc(vertices, graph):
  edges_list = list(graph.edges())
  vertices = list(map(int, vertices))

  # Scorro una copia della lista
  for e in edges_list[:]:
    for v in vertices:
      if v in e:
        edges_list.remove(e)
        break

  if(len(edges_list) > 0):
    return 0
  else:
    return 1

## Verifico se il vc approssimato fornito dall'utente è tale
def verify_approx_vc(matching, graph):
  curG = graph.copy()
  max_matching = [eval(t) for t in matching]

  visited = []
  
  while curG.number_of_edges() != 0:
    for e in max_matching:
      e = tuple(sorted(e))
      if e not in visited:
        curG.remove_edge(e[0],e[1])
      else: 
        return 0

      for v in e:
        for e1 in list(curG.edges())[:]:
          if v in e1 and e1 not in visited:
            curG.remove_edge(e1[0],e1[1])
            visited.append(e1)

  for e in max_matching:
    for v in e:
      if v in visited:
        return 0

  return 1

'''
VARIE
'''
def plot_graph(graph):
  nx.draw(graph, with_labels=True)

  plt.show()

'''
GOAL SUMMARIES
'''
# Da rivedere per VC
def print_goal_summary(goal,testcases,num_testcases_passed,num_testcases_correct_ans,num_testcases_wrong_ans,out_of_time, TAc,LANG):
  TAc.print(LANG.render_feedback("summary", f'\n# SUMMARY OF THE RESULTS FOR GOAL "{goal}":\n'), "white", ["bold"])

  for t,i in zip(testcases,range(1,1+len(testcases))):
    if t['answer_correct'] == True:
      TAc.print(LANG.render_feedback("right-ans", f'# TestCase {i}: Correct answer! Took time {t["measured_time"]} on your machine.\n'), "green")
    elif t['answer_correct'] == False:
      TAc.print(LANG.render_feedback("wrong-ans", f'# NO! You gave the wrong solution for the instance with this parameters:\n#num_vertices = {t["num_vertices"]}, seed = {t["seed"]}.\n'), "yellow")
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
