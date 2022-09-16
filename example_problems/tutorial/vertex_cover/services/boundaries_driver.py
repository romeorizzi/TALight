#!/usr/bin/env python3
'''
Based on https://www.researchgate.net/publication/327764548_A_polynomial-time_algorithm_to_obtain_bounds_for_the_vertex_cover_number
'''
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import random
import networkx as nx
import matplotlib.pyplot as plt
import vertex_cover_lib as vcl
import threading

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('collection',str),
    ('instance_id',int),
    ('instance_format',str),
    ('num_vertices',int),
    ('num_edges',int),
    ('weighted',bool),
    ('goal',str),
    ('plot',bool),
    ('plot_sol',bool),
    ('seed',str),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:
weighted = ENV['weighted']

## Input Sources
if TALf.exists_input_file('instance'):
  instance = vcl.get_instance_from_str(TALf.input_file_as_str('instance'), instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("successful-load", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])

elif ENV["source"] == 'terminal':
  instance = {}
  instance['num_vertices'] = ENV['num_vertices']
  instance['num_edges'] = ENV['num_edges']

  instance['weighted'] = ENV['weighted']

  #TAc.print(LANG.render_feedback("waiting-line", f'#? Waiting for the graph.\nGraph format: (x,y) (w,z) ... (n,m)\n'), "yellow")
  TAc.print(LANG.render_feedback("waiting-line", f'#? Waiting for the graph.\n'), "yellow")

  TAc.print(LANG.render_feedback("insert-edges", f'Given {ENV["num_vertices"]} vertices labelled with the naturals in the interval [0,{ENV["num_vertices"]-1}], you are now expected to enter {ENV["num_edges"]} edges. To specify an edge, simply enter its two endonodes separated by spaces.'), "yellow", ["bold"])
  edges = []
  for i in range(1,1+ENV["num_edges"]):
    TAc.print(LANG.render_feedback("insert-edge", f'Insert the two endpoints of edge {i}, that is, enter a line with two naturals in the interval [0,{ENV["num_vertices"]-1}],  separated by spaces.'), "yellow", ["bold"])
    u,v = TALinput(int, 2, TAc=TAc)
    edges.append([u,v])

  for u,v in edges:
    if u not in range(instance['num_vertices']) or v not in range(instance['num_vertices']):
      TAc.print(f'Edge ({u}, {v}) is not a valid edge for the graph. Aborting.\n', "red", ["bold"], flush=True)
      exit(0)

  if len(edges) != instance['num_edges']:
    TAc.print(LANG.render_feedback("wrong-edges-number", f'\nWrong number of edges ({len(edges)} instead of {instance["num_edges"]})\n'), "red", ["bold"])
    exit(0)

  if instance['weighted']:
    TAc.print(LANG.render_feedback("insert-weights", f'Enter nodes weights. Format: integers separated by spaces:'), "yellow", ["bold"])
    l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

    if len(l) != instance['num_vertices']:
      TAc.print(LANG.render_feedback("wrong-weights-number", f'\nWrong number of weights ({len(l)} instead of {instance["num_vertices"]})\n'), "red", ["bold"])
      exit(0)

    for w in l:
      if not w.isdigit():
        TAc.print(LANG.render_feedback("wrong-weights-format", f'\nWeights must be integer numbers. Aborting.\n'), "red", ["bold"])
        exit(0)

  G = nx.Graph()
  G.add_nodes_from([int(v) for v in range(instance['num_vertices'])])
  G.add_edges_from(edges)

  i = 0

  for v in sorted(G.nodes()):
    G.add_node(v, weight=int(l[i]))
    i += 1

  instance['graph'] = G

  instance_str = vcl.instance_to_str(instance, format_name=ENV['instance_format'])
  output_filename = f"terminal_instance.{ENV['instance_format']}.txt"

elif ENV["source"] == 'randgen_1':
  # Get random instance
  if not weighted:
    instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'])[0]
  else:
    instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'], 1)[0]

else: # take instance from catalogue
  #instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance_str = TALf.get_catalogue_instancefile_as_str_from_id_collection_and_ext(ENV["collection"], ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance = vcl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"], flush=True)

TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"], flush=True)
TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"], flush=True)

if weighted:
  TAc.print(LANG.render_feedback("nocover-weight", f'No cover weight of the graph: {no_cover_weight}\n'), "white", ["bold"], flush=True)

size_sol, vc_sol = vcl.calculate_minimum_vc(instance['graph'])

if ENV['plot']:
  #thr1 = threading.Thread(target=vcl.plot_graph,args=(instance['graph']))
  #thr1.start()
  vcl.plot_graph(instance['graph'])

## Input lb, up e check
if ENV['goal'] == 'lower_bound' or ENV['goal'] == 'both_bounds' or ENV['goal'] == '2apx':
  TAc.print(LANG.render_feedback("insert-lb", f'Enter you conjectured lower bound: '), "yellow", ["bold"])
  lower_bound = TALinput(int, 1, TAc=TAc)[0]
  if lower_bound <= 0:
    TAc.print(LANG.render_feedback("wrong-lb-value-0", f'Lower bound must be greater than 0. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  if lower_bound > instance['num_vertices']:
    TAc.print(LANG.render_feedback("wrong-lb-value-1", f'Lower bound must be less or equal to {instance["num_vertices"]}. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  
  TAc.print(LANG.render_feedback("insert-match-lb", f'Enter you conjectured match for lower bound (integers separated by spaces): '), "yellow", ["bold"])
  lb_match = TALinput(int, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

  if len(lb_match) != lower_bound:
    TAc.print(LANG.render_feedback("wrong-nodes-number-match", f'Wrong number of nodes (they must be {lower_bound}). Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)

if ENV['goal'] == 'upper_bound' or ENV['goal'] == 'both_bounds'  or ENV['goal'] == '2apx':
  TAc.print(LANG.render_feedback("insert-ub", f'Enter you conjectured upper bound: '), "yellow", ["bold"])
  upper_bound = TALinput(int, 1, TAc=TAc)[0]
  if upper_bound <= 0:
    TAc.print(LANG.render_feedback("wrong-ub-value-0", f'Upper bound must be greater than 0. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  if upper_bound > instance['num_vertices']:
    TAc.print(LANG.render_feedback("wrong-ub-value-1", f'Upper bound must be less or equal to {instance["num_vertices"]}. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)

  TAc.print(LANG.render_feedback("insert-cover-ub", f'Enter you conjectured cover for upper bound (integers separated by spaces): '), "yellow", ["bold"])
  ub_cover = TALinput(int, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

  if len(ub_cover) != upper_bound:
    TAc.print(LANG.render_feedback("wrong-nodes-number-cover", f'Wrong number of nodes (they must be {upper_bound}). Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)

if 'lower_bound' in locals() and 'upper_bound' in locals():
  if lower_bound > upper_bound:
    TAc.print(LANG.render_feedback("wrong-lb-ub-value", f'Lower bound can\'t be greater than upper bound. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)

## Ordino i nodi per grado
CurG = instance['graph'].copy()
deg_list = list(CurG.degree())
deg_list.sort(key=lambda tup: tup[1], reverse=True)

sum_deg = 0
i = 0
S = [] # Lower bound
VminS = []

while sum_deg < instance['num_edges']:
  sum_deg += deg_list[i][1]
  S.append(deg_list[i][0])
  i += 1

for v in list(CurG.nodes())[:]:
  if v not in S:
    VminS.append(v)
  else:
    CurG.remove_node(v)

if ENV['goal'] == 'lower_bound' or ENV['goal'] == 'both_bounds' or ENV['goal'] == '2apx':
  if lower_bound != len(S):
    TAc.print(LANG.render_feedback("invalid-lb-size", f'The size of the lower bound you provided is not correct.\n'), "red", ["bold"], flush=True) 
    exit(0)
  for i in lb_match:
    if i not in S:
      TAc.print(LANG.render_feedback("invalid-lb-match", f'The lower bound match you provided is not a valid match.\n'), "red", ["bold"], flush=True)
      exit(0)

S_1 = S.copy() # Upper bound

for v in list(CurG.nodes())[:]:
  if CurG.degree(v) > 0:
    S_1.append(v)
    CurG.remove_node(v)

if ENV['goal'] == 'upper_bound' or ENV['goal'] == 'both_bounds' or ENV['goal'] == '2apx':
  if upper_bound != len(S_1):
    TAc.print(LANG.render_feedback("invalid-ub-size", f'The size of the upper bound you provided is not correct.\n'), "red", ["bold"], flush=True)
    exit(0)
  for i in ub_cover:
    if i not in S_1:
      TAc.print(LANG.render_feedback("invalid-ub-cover", f'The upper bound node cover you provided is not a valid node cover.\n'), "red", ["bold"], flush=True)
      exit(0)

if ENV['goal'] == '2apx':
  if upper_bound > 2 * lower_bound:
    TAc.print(LANG.render_feedback("not-2apx", f'The upper bound is more than two times of the lower bound. Approximation is not correct.\n'), "red", ["bold"], flush=True)
    exit(0)

if ENV['goal'] == 'lower_bound':
  TAc.OK()
  TAc.print(LANG.render_feedback("goal-lb-reached", f'Vertex cover has a lower bound equal to {lower_bound}.'), "green", ["bold"], flush=True)
  TAc.print(f'Lower bound match: ', "green", ["bold"], flush=True, end='')
  TAc.print(f'{" ".join(map(str, sorted(S)))}\n', "white", ["bold"], flush=True)
elif ENV['goal'] == 'upper_bound':
  TAc.OK()
  TAc.print(LANG.render_feedback("goal-ub-reached", f'Vertex cover has an upper bound equal to {upper_bound}.'), "green", ["bold"], flush=True)
  TAc.print(f'Upper bound node cover: ', "green", ["bold"], flush=True, end='')
  TAc.print(f'{" ".join(map(str, sorted(S_1)))}\n', "white", ["bold"], flush=True)
elif ENV['goal'] == 'both_bounds':
  TAc.OK()
  TAc.print(LANG.render_feedback("goal-both-reached", f'Bounds for the vertex cover are included in the range {lower_bound}-{upper_bound}.'), "green", ["bold"], flush=True)
  TAc.print(f'Lower bound match: ', "green", ["bold"], flush=True, end='')
  TAc.print(f'{" ".join(map(str, sorted(S)))}', "white", ["bold"], flush=True)
  TAc.print(f'Upper bound node cover: ', "green", ["bold"], flush=True, end='')
  TAc.print(f'{" ".join(map(str, sorted(S_1)))}\n', "white", ["bold"], flush=True)
  if ENV['plot_sol']:
    vcl.plot_mvc(instance['graph'], vc_sol, [])
elif ENV['goal'] == '2apx':
  TAc.OK()
  TAc.print(LANG.render_feedback("goal-2apx-reached", f'Bounds for the vertex cover are included in the range {lower_bound}-{upper_bound}. Upper bound is {upper_bound/lower_bound} times the lower bound.'), "green", ["bold"], flush=True)
  TAc.print(f'Lower bound match: ', "green", ["bold"], flush=True, end='')
  TAc.print(f'{" ".join(map(str, sorted(S)))}', "white", ["bold"], flush=True)
  TAc.print(f'Upper bound node cover: ', "green", ["bold"], flush=True, end='')
  TAc.print(f'{" ".join(map(str, sorted(S_1)))}\n', "white", ["bold"], flush=True)
  if ENV['plot_sol']:
    vcl.plot_mvc(instance['graph'], vc_sol, [])

exit(0)
