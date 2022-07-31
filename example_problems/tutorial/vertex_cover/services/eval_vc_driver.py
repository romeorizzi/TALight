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
MAX_TIME = 2

# INSTANCES FOR GOAL = correct
if ENV['goal'] == 'correct':
  goals.append('correct')

  num_vertices = 8
  NUM_INSTANCES = 5
  scaling_factor = 1.3

  instances['correct'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices)

# INSTANCES FOR GOAL = minimum
if ENV['goal'] == 'minimum':
  goals.append('minimum')

  num_vertices = 10
  NUM_INSTANCES = 7
  scaling_factor = 1.4

  instances['minimum'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices)

# INSTANCES FOR GOAL = approx
if ENV['goal'] == 'approx':
  goals.append('approx')

  num_vertices = 80
  NUM_INSTANCES = 5
  scaling_factor = 1.2

  instances['approx'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices)

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def test(instance):
  graph = instance['graph']
  num_vertices = instance['num_vertices']

  TAc.print(LANG.render_feedback("graph-size",'# We have this number of vertices in the graph: '), "white", ["bold"], end='')
  TAc.print(num_vertices, "yellow", ["bold"])
  TAc.print(LANG.render_feedback("print-graph", f'\n# The sequence is:\n'), "white", ["bold"])
  #TAc.print(num_vertices, "white", ["bold"])
  #TAc.print(graph[0], "white", ["bold"])

  vcl.print_graph(num_vertices, graph)

  if num_vertices < 80:
    TAc.print(LANG.render_feedback("best-sol-question", f'\n# Which is the minimum vertex cover for this graph?'), "white", ["bold"])
  else:
    TAc.print(LANG.render_feedback("best-sol-question", f'\n# Which is the approximated vertex cover for this graph?'), "white", ["bold"])

  start = monotonic()
  answer = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)
  #answer = ' '.join(map(str, answer))
  end = monotonic()
  instance['measured_time'] = end-start

  if num_vertices < 80:
    #size,vc = vcl.calculate_minimum_vc(num_vertices, graph)
    ok = vcl.verify_vc(answer, graph)
  else:
    #size,vc = vcl.calculate_approx_vc(num_vertices, graph)
    ans = []
    edges = ''

    for i in range(0, len(answer), 2):
      edges += '{' + answer[i] + ',' + answer[i+1] + '}'

    ans.append(edges)

    ok = vcl.verify_approx_vc(ans, graph)

  #if answer == vc:
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
