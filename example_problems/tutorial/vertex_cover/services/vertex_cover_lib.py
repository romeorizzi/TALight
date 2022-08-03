#!/usr/bin/env python3
import os
import sys
import random
import math
from datetime import datetime

from termcolor import colored
from contextlib import redirect_stdout

AVAILABLE_FORMATS = {'instance':{'simple':'simple.txt', 'with_vertices':'with_vertices.txt', 'vertex_cover_dat':'.dat'},'solution':{'all_solutions': 'all_solutions.txt'}}
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
    graph = instance['graph'] 
    output= f''

    if format_name == "with_vertices":
      num_vertices = instance['num_vertices']
      output += f'{num_vertices}\n'

    for i in graph:
      output += str(i)

    output += '\n'

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
    str_to_arr = instance_as_str.split()

    if format_name != "with_vertices":
      instance['graph'] = str_to_arr
      #instance['num_vertices'] = len(str_to_arr)

    else:
      instance['graph'] = str_to_arr[1:]
      instance['num_vertices'] = len(str_to_arr[1:])
    
    return instance

# Da rivedere per VC
def instance_to_dat_str(instance,format_name='vertex_cover_dat'):
  """Of the given <instance>, this function returns the .dat string in format <format_name>"""
  assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
  graph = instance['graph'][0]
  num_vertices = instance['num_vertices']

  output = f"param vertices := {num_vertices};                  # Number of vertices in the graph\n"
  output += "param: EDGES OF THE GRAPH "
  output += f":= {graph} "
  output += ";\nend;"
    
  return output

def get_instance_from_dat(instance_as_str, format_name):
  """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
  assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
  split_instance = instance_as_str.split(";")
  instance = {}

  instance['num_vertices'] = int(get_param(split_instance[0])) # assign seq_len
  instance['graph'] = list(ast.literal_eval(get_param(split_instance[1]).replace("] [","],[").replace(" ","")))

  return instance


'''
GENERATORE GRAFI
'''
def instances_generator(num_instances, scaling_factor: float, num_vertices: int, seed = "random_seed"):
  instances = []

  for _ in range(num_instances):
    instance = {}
    if seed == "random_seed":
      seed = random.randint(100000,999999)

    instance['num_vertices'] = num_vertices
    instance['graph'] = random_graph(num_vertices, seed)
    instance['seed'] = seed

    num_vertices = math.ceil(scaling_factor * num_vertices)

    instance['measured_time'] = None
    instance['answer_correct'] = None

    instances.append(instance)

  return instances

def random_graph(num_vertices, seed):
  random.seed(seed)

  graph = []
  #graph = ''
  edge = ''

  for i in range(num_vertices):
    for j in range(i+1, num_vertices):
      arco = random.choice([0,1])

      if arco:
        #edge = str(i) + ',' + str(j)
        #graph.append('{' + edge + '}')
        edge += '{' + str(i) + ',' + str(j) + '}'
        #graph += edge

  graph.append(edge)

  return graph

def print_graph(num_vertices, graph, instance_format=DEFAULT_INSTANCE_FORMAT):
  print(f'{num_vertices}')  
  print(f'{graph[0]}')


'''
SOLUTORI
'''
def solutions(sol_type,instance,instance_format=DEFAULT_INSTANCE_FORMAT):
  sols = {}

  if sol_type == 'minimum':
    size, vc = calculate_minimum_vc(instance['num_vertices'], instance['graph'])
    sols['calculate_minimum_vc'] = f"{vc}"

  elif sol_type == 'approx':
    size, vc = calculate_approx_vc(instance['num_vertices'], instance['graph'])
    sols['calculate_approx_vc'] = f"{vc}"

  elif sol_type == 'both':
    size_min, vc_min = calculate_minimum_vc(instance['num_vertices'], instance['graph'])
    size_appr, vc_appr = calculate_approx_vc(instance['num_vertices'], instance['graph'],'greedy')
    sols['calculate_minimum_vc'] = f"{vc_min}"
    sols['calculate_approx_vc'] = f"{vc_appr}"

  return sols

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

'''
solutore vero e proprio: uso un algoritmo Branch and Bound
'''
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

## Calcolo una 2-approssimazione del VC. La scelta dell'arco è greedy,
## Quindi in teoria dovrei avere sempre la miglior approssimazione
## possibile...
def calculate_approx_vc(num_vertices, graph, mode='random'):
  G = get_edges(graph)
  curG = G.copy()
  curG.sort(key=lambda tup: tup[0])

  visited = []
  c = []

  while curG != []:
    if mode == 'greedy':
      vertices_list = [i for i in range(num_vertices)]
      v = find_maxdeg(vertices_list, curG)[0]
      neighbour = neighbours(v, curG)
      vertices_list.remove(v)
    
      v1 = find_maxdeg(neighbour, curG)[0]
      vertices_list.remove(v1)
    
      arco = (v,v1)
      arco = tuple(sorted(arco))

    ## Prendo un arco casualmente
    elif mode == 'random':
      i = random.randint(0,len(curG)-1)
      arco = curG[i]
      arco = tuple(sorted(arco))
      v = arco[0]
      v1 = arco[1]

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

## Verifico se un vertex cover fornito in input è un vc valido per il grafo
def verify_vc(vertices, graph):
  edges_list = get_edges(graph)
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
def verify_approx_vc(vc_edges, graph):
  edges_list = get_edges(graph)
  curG = edges_list.copy()
  curG.sort(key=lambda tup: tup[0])
  edges_vc = get_edges(vc_edges)

  visited = []
  
  while curG != []:
    for e in edges_vc:
      e = tuple(sorted(e))
      if e not in visited:
        curG.remove(e)
      else: 
        return 0

      for v in e:
        for e1 in curG[:]:
          if v in e1 and e1 not in visited:
            curG.remove(e1)
            visited.append(e1)

  for e in edges_vc:
    for v in e:
      if v in visited:
        return 0

  return 1

## Verifico se una soluzione approssimata è 2-approssimazione per il VC
def is_2_approx(c, c_star):
  if len(c)/len(c_star) <= 2:
    return 1
  
  return 0

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
