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

# No need to have different instances for different goals
num_vertices = 20
num_edges = 30
NUM_INSTANCES = 10
scaling_factor = 1.6

# INSTANCES FOR GOALS
if ENV['goal'] == 'lower_bound':
  goals.append('lower_bound')
  instances['lower_bound'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices, num_edges)

if ENV['goal'] == 'upper_bound':
  goals.append('upper_bound')
  instances['upper_bound'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices, num_edges)

if ENV['goal'] == 'both_bounds':
  goals.append('both_bounds')
  instances['both_bounds'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices, num_edges)

if ENV['goal'] == '2apx':
  goals.append('2apx')
  instances['2apx'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices, num_edges)

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

  vcl.print_graph(num_vertices, num_edges, graph)

  if ENV['goal'] == 'lower_bound':
    TAc.print(LANG.render_feedback("lb-question", f'\n# Which is the vertex cover lower bound for this graph?'), "white", ["bold"])
  if ENV['goal'] == 'upper_bound':
    TAc.print(LANG.render_feedback("ub-question", f'\n# Which is the vertex cover upper bound for this graph?'), "white", ["bold"])
  if ENV['goal'] == 'both_bounds':
    TAc.print(LANG.render_feedback("both-question", f'\n# Which are the vertex cover bounds for this graph?'), "white", ["bold"])
  if ENV['goal'] == '2apx':
    TAc.print(LANG.render_feedback("2apx-question", f'\n# Which are the vertex cover bounds for this graph?'), "white", ["bold"])

  start = monotonic()
  lb = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
  S = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)
  ub = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
  S_1 = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)
  end = monotonic()
  instance['measured_time'] = end-start

  S = [int(v) for v in S]
  S_1 = [int(v) for v in S_1]

  if ENV['goal'] == 'lower_bound':
    check_lb = vcl.verify_lb(S, graph)

    if check_lb:
      instance['answer_correct'] = True
    else:
      instance['answer_correct'] = False

  elif ENV['goal'] == 'upper_bound':
    check_ub = vcl.verify_lb(S_1, graph)

    if check_ub:
      instance['answer_correct'] = True
    else:
      instance['answer_correct'] = False

  elif ENV['goal'] == 'both_bounds' or ENV['goal'] == '2apx':
    check_lb = vcl.verify_lb(S, graph)
    check_ub = vcl.verify_lb(S_1, graph)

    if check_lb and check_ub:
      if ENV['goal'] == '2apx':
        if int(ub) <= 2*int(lb):
          instance['answer_correct'] = True
        else:
          print(f'# 2*lb: {2*int(lb)} - ub: {int(ub)}')
          instance['answer_correct'] = False
      else:
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
