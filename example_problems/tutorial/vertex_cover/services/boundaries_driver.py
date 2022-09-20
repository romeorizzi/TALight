#!/usr/bin/env python3
'''
Based on https://www.researchgate.net/publication/327764548_A_polynomial-time_algorithm_to_obtain_bounds_for_the_vertex_cover_number
NOTE: 2-apx is not guaranteed!
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
    #('weighted',bool),
    ('goal',str),
    ('print_sol_bounds',bool),
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
#weighted = ENV['weighted']
weighted = 0

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

## Calcolo soluzione esatta e bounds esatti
size_sol, vc_sol = vcl.calculate_minimum_vc(instance['graph'])
lb, S, ub, S_1 = vcl.calculate_bounds(instance['graph'])

if ENV['plot']:
  #thr1 = threading.Thread(target=vcl.plot_graph,args=(instance['graph'],))
  #thr1.start()
  vcl.plot_graph(instance['graph'])

if not ENV['print_sol_bounds']:
  ## Input lb, up e check
  if ENV['goal'] == 'lower_bound' or ENV['goal'] == 'both_bounds' or ENV['goal'] == '2apx':
    TAc.print(LANG.render_feedback("insert-lb", f'Enter your conjectured lower bound: '), "yellow", ["bold"], flush=True)
    lower_bound = TALinput(int, 1, TAc=TAc)[0]
    if lower_bound <= 0:
      TAc.print(LANG.render_feedback("wrong-lb-value-0", f'Lower bound must be greater than 0. Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)
    if lower_bound > instance['num_vertices']:
      TAc.print(LANG.render_feedback("wrong-lb-value-1", f'Lower bound must be less or equal to {instance["num_vertices"]}. Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)
    if lower_bound > size_sol:
      TAc.print(LANG.render_feedback("wrong-lb-value-2", f'Lower bound too high. Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)
  
    TAc.print(LANG.render_feedback("insert-match-lb", f'Enter your conjectured match for lower bound (integers separated by spaces): '), "yellow", ["bold"])
    lb_match = TALinput(int, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

    if len(lb_match) != lower_bound:
      TAc.print(LANG.render_feedback("wrong-nodes-number-match", f'Wrong number of nodes (they must be {lower_bound}). Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)

    if not vcl.verify_lb(lb_match, instance['graph']):
      TAc.print(LANG.render_feedback("invalid-lb-match", f'The lower bound you provided is not valid.\n'), "red", ["bold"], flush=True)
      exit(0)

  if ENV['goal'] == 'upper_bound' or ENV['goal'] == 'both_bounds'  or ENV['goal'] == '2apx':
    TAc.print(LANG.render_feedback("insert-ub", f'Enter your conjectured upper bound: '), "yellow", ["bold"], flush=True)
    upper_bound = TALinput(int, 1, TAc=TAc)[0]
    if upper_bound <= 0:
      TAc.print(LANG.render_feedback("wrong-ub-value-0", f'Upper bound must be greater than 0. Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)
    if upper_bound > instance['num_vertices']:
      TAc.print(LANG.render_feedback("wrong-ub-value-1", f'Upper bound must be less or equal to {instance["num_vertices"]}. Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)
    if upper_bound < size_sol:
      TAc.print(LANG.render_feedback("wrong-ub-value-2", f'Upper bound too low. Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)
    if 'lower_bound' in locals():
      if lower_bound > upper_bound:
        TAc.print(LANG.render_feedback("wrong-lb-ub-value", f'Upper bound must be greater than the lower bound. Aborting.\n'), "red", ["bold"], flush=True)
        exit(0)
  
    TAc.print(LANG.render_feedback("insert-cover-ub", f'Enter your conjectured node cover for upper bound (integers separated by spaces): '), "yellow", ["bold"], flush=True)
    ub_cover = TALinput(int, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

    if len(ub_cover) != upper_bound:
      TAc.print(LANG.render_feedback("wrong-nodes-number-cover", f'Wrong number of nodes (they must be {upper_bound}). Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)

    if not vcl.verify_ub(ub_cover, instance['graph']):
      TAc.print(LANG.render_feedback("invalid-ub-cover", f'The upper bound you provided is not valid.\n'), "red", ["bold"], flush=True)
      exit(0)

  if ENV['goal'] == '2apx':
    if upper_bound > 2 * lower_bound:
      TAc.print(LANG.render_feedback("not-2apx", f'The upper bound is more than two times of the lower bound. 2-approximation not reached (upper bound is {upper_bound/lower_bound} times the lower bound).\n'), "red", ["bold"], flush=True)
      exit(0)

## Stampa messaggi
if ENV['print_sol_bounds']:
  TAc.print(LANG.render_feedback("sol-bounds", f'Bounds for the vertex cover are '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{lb}-{ub}', "white", ["bold"], flush=True)
  TAc.print(f'Lower bound match: ', "green", ["bold"], flush=True, end='')
  TAc.print(f'{" ".join(map(str, sorted(S)))}', "white", ["bold"], flush=True)
  TAc.print(f'Upper bound node cover: ', "green", ["bold"], flush=True, end='')
  TAc.print(f'{" ".join(map(str, sorted(S_1)))}\n', "white", ["bold"], flush=True)
  
  if ENV['plot_sol']:
    vcl.plot_mvc(instance['graph'], vc_sol, [])
else:
  if ENV['goal'] == 'lower_bound':
    TAc.OK()
    TAc.print(LANG.render_feedback("goal-lb-reached", f'Vertex cover has a lower bound equal to {lower_bound}.'), "green", ["bold"], flush=True)
    TAc.print(f'Lower bound match: ', "green", ["bold"], flush=True, end='')
    TAc.print(f'{" ".join(map(str, sorted(lb_match)))}\n', "white", ["bold"], flush=True)
  elif ENV['goal'] == 'upper_bound':
    TAc.OK()
    TAc.print(LANG.render_feedback("goal-ub-reached", f'Vertex cover has an upper bound equal to {upper_bound}.'), "green", ["bold"], flush=True)
    TAc.print(f'Upper bound node cover: ', "green", ["bold"], flush=True, end='')
    TAc.print(f'{" ".join(map(str, sorted(ub_coveer)))}\n', "white", ["bold"], flush=True)
  elif ENV['goal'] == 'both_bounds':
    TAc.OK()
    TAc.print(LANG.render_feedback("goal-both-reached", f'Bounds for the vertex cover are {lower_bound}-{upper_bound}.'), "green", ["bold"], flush=True)
    TAc.print(f'Lower bound match: ', "green", ["bold"], flush=True, end='')
    TAc.print(f'{" ".join(map(str, sorted(lb_match)))}', "white", ["bold"], flush=True)
    TAc.print(f'Upper bound node cover: ', "green", ["bold"], flush=True, end='')
    TAc.print(f'{" ".join(map(str, sorted(ub_cover)))}\n', "white", ["bold"], flush=True)
    if ENV['plot_sol']:
      vcl.plot_mvc(instance['graph'], vc_sol, [])
  elif ENV['goal'] == '2apx':
    TAc.OK()
    TAc.print(LANG.render_feedback("goal-2apx-reached", f'Bounds for the vertex cover are {lower_bound}-{upper_bound}. 2-approximation reached (upper bound is {upper_bound/lower_bound} times the lower bound).'), "green", ["bold"], flush=True)
    TAc.print(f'Lower bound match: ', "green", ["bold"], flush=True, end='')
    TAc.print(f'{" ".join(map(str, sorted(lb_match)))}', "white", ["bold"], flush=True)
    TAc.print(f'Upper bound node cover: ', "green", ["bold"], flush=True, end='')
    TAc.print(f'{" ".join(map(str, sorted(ub_cover)))}\n', "white", ["bold"], flush=True)
    if ENV['plot_sol']:
      vcl.plot_mvc(instance['graph'], vc_sol, [])

exit(0)
