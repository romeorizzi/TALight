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
if ENV['goal'] == 'correct':
  goals.append('correct')

  num_vertices = 10
  NUM_INSTANCES = 5
  scaling_factor = 1.6

  instances['correct'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices)

# INSTANCES FOR GOAL = approx
if ENV['goal'] == 'big_instances':
  goals.append('big_instances')

  num_vertices = 80
  NUM_INSTANCES = 5
  scaling_factor = 1.2

  instances['big_instances'] = vcl.instances_generator(NUM_INSTANCES, scaling_factor, num_vertices)

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def test(instance):
  graph = instance['graph']
  num_vertices = instance['num_vertices']

  TAc.print(LANG.render_feedback("graph-size",'# We have this number of vertices in the graph: '), "white", ["bold"], end='')
  TAc.print(num_vertices, "yellow", ["bold"])
  TAc.print(LANG.render_feedback("print-graph", f'\n# The graph is:\n'), "white", ["bold"])
  #TAc.print(num_vertices, "white", ["bold"])
  #TAc.print(graph[0], "white", ["bold"])

  vcl.print_graph(num_vertices, graph)

  TAc.print(LANG.render_feedback("best-sol-question", f'\n# Which is the 2-approximation vertex cover for this graph?'), "white", ["bold"])

  start = monotonic()
  size_answer = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
  answer = TALinput(str, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)
  #answer = ' '.join(map(str, answer))
  end = monotonic()
  instance['measured_time'] = end-start

  ans = []
  edges = ''

  for i in range(0, len(answer), 2):
    edges += '{' + answer[i] + ',' + answer[i+1] + '}'

  ans.append(edges)

  if ENV['goal'] == 'correct':
    check = vcl.verify_approx_vc(ans, graph)
    size,vc = vcl.calculate_minimum_vc(num_vertices, graph)
    ok = False

    if check:
      if int(size_answer)/size <= 2:
        ok = True
  else:
    ok = vcl.verify_approx_vc(ans, graph)

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
