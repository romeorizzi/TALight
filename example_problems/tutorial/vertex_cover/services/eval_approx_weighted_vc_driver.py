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
  MAX_TIME = 0.5
else:
  MAX_TIME = 1

if ENV['goal'] == 'small_instances':
  goals.append('small_instances')

  num_vertices = 10
  num_edges = 15
  NUM_INSTANCES = 5
  scaling_factor = 1.6

  instances['small_instances'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices, num_edges, 'random_seed', 1)

# INSTANCES FOR GOAL = approx
if ENV['goal'] == 'big_instances':
  goals.append('big_instances')

  num_vertices = 80
  num_edges = 130
  NUM_INSTANCES = 5
  scaling_factor = 4.5

  instances['big_instances'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices, num_edges, 'random_seed', 1)

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def test(instance):
  graph = instance['graph']
  num_vertices = instance['num_vertices']
  num_edges = instance['num_edges']

  TAc.print(LANG.render_feedback("graph-num-nodes",'# We have this number of vertices in the graph: '), "white", ["bold"], end='')
  TAc.print(num_vertices, "yellow", ["bold"])
  TAc.print(LANG.render_feedback("graph-num-edges",'# We have this number of edges in the graph: '), "white", ["bold"], end='')
  TAc.print(num_edges, "yellow", ["bold"])
  TAc.print(LANG.render_feedback("print-graph", f'\n# The graph is:\n'), "white", ["bold"])

  vcl.print_graph(num_vertices, num_edges, graph, 1)

  TAc.print(LANG.render_feedback("best-sol-question", f'\n# Which is a 2-approximation weighted vertex cover for this graph?'), "white", ["bold"])

  start = monotonic()
  size_answer = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
  answer = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)
  weight_answer = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
  #answer = ' '.join(map(str, answer))
  end = monotonic()
  instance['measured_time'] = end-start

  ok = False
  check = vcl.verify_vc(answer, graph)

  if check:
    appr_sol, size_sol, weight_sol = vcl.calculate_weighted_approx_vc(instance['graph'])

    if ENV['goal'] == 'small_instances':
      vc_sol, size_exact_sol, min_weight_sol = vcl.calculate_minimum_weight_vc(instance['graph'])

      if int(weight_answer) <= 2 * min_weight_sol:
        ok=True
    else:
      if int(weight_answer) <= weight_sol:
        ok = True
      
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
