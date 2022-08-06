#!/usr/bin/env python3
from sys import stderr, exit

import random
import math
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import vertex_cover_lib as vcl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('code_lang',str),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

instances = {}
goals = []

if ENV['code_lang'] == 'compiled':
  MAX_TIME = 1
else:
  MAX_TIME = 2

# INSTANCES FOR GOAL = correct
if ENV['goal'] == 'feasible':
  goals.append('feasible')

  num_vertices = 10
  num_edges = 15
  NUM_INSTANCES = 5
  scaling_factor = 1.4

  instances['feasible'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices, num_edges)

# INSTANCES FOR GOAL = minimum
if ENV['goal'] == 'minimum':
  goals.append('minimum')

  num_vertices = 10
  num_edges = 15
  NUM_INSTANCES = 7
  scaling_factor = 1.4

  instances['minimum'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices, num_edges)

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def test(instance):
  graph = instance['graph']
  num_vertices = graph.number_of_nodes()
  num_edges = graph.number_of_edges()

  TAc.print(LANG.render_feedback("graph-size",'# We have this number of vertices in the graph: '), "white", ["bold"], end='')
  TAc.print(num_vertices, "yellow", ["bold"])
  TAc.print(LANG.render_feedback("graph-size",'# We have this number of edges in the graph: '), "white", ["bold"], end='')
  TAc.print(num_edges, "yellow", ["bold"])
  TAc.print(LANG.render_feedback("print-graph", f'\n# The graph is:\n'), "white", ["bold"])

  vcl.print_graph(list(graph.edges()))

  TAc.print(LANG.render_feedback("best-sol-question", f'\n# Which is the minimum vertex cover for this graph?'), "white", ["bold"])

  start = monotonic()
  size_answer = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
  answer = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)
  #answer = ' '.join(map(str, answer))
  end = monotonic()
  instance['measured_time'] = end-start

  if ENV['goal'] != 'feasible':
    check = vcl.verify_vc(answer, graph)
    size,vc = vcl.calculate_minimum_vc(graph)
    ok = False

    if check:
      print(f"# size_ans {size_answer} size {size}")
      if int(size_answer) == size:
        ok = True
  else:
    ok = vcl.verify_vc(answer, graph)

  if ok:
    instance['answer_correct'] = True
  else:
    instance['answer_correct'] = False

# MAIN: TEST ALL TESTCASES: 
out_of_time = 0

for goal in goals:
  for instance in instances[goal]:
    test(instance)

    if instance['measured_time'] > MAX_TIME:
      out_of_time += 1
      vcl.print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG)
      exit(0)
            
vcl.print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG)
exit(0)
