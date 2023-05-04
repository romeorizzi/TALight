#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import random
import networkx as nx
import matplotlib.pyplot as plt
import vertex_cover_lib as vcl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('collection',str),
    ('instance_id',int),
    ('instance_format',str),
    ('num_vertices',int),
    ('num_edges',int),
    ('weighted',bool),
    ('goal_2apx',bool),
    ('upper_bound',int),
    ('lower_bound',int),
    ('plot',bool),
    ('plot_sol',bool),
    ('seed',str),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

weighted = ENV['weighted']
upper_bound = ENV['upper_bound']
lower_bound = ENV['lower_bound']

if not upper_bound and not lower_bound:
  TAc.print(LANG.render_feedback("insert-one-bound", f'ERROR: you must provide at least a lower bound or an upper bound.\n'), "red", ["bold"])
  exit(0)

# START CODING YOUR SERVICE:
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

# Trovo il peso totale del grafo ("no cover")
no_cover_weight = 0
for n,w in nx.get_node_attributes(instance['graph'], 'weight').items():
  no_cover_weight += w

# Calcolo soluzione
if weighted:
  vc_sol, size_sol, weight_sol = vcl.calculate_minimum_weight_vc(instance['graph'])
else:
  size_sol, vc_sol = vcl.calculate_minimum_vc(instance['graph'])

if ENV['goal_2apx']:
  if weighted:
    sol_apx, size_apx, weight_apx = vcl.calculate_weighted_approx_vc(instance['graph'])
  else:
    size_apx, sol_apx, matching = vcl.calculate_approx_vc(instance['graph'])

TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"], flush=True)
TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"], flush=True)

if weighted:
  TAc.print(LANG.render_feedback("nocover-weight", f'No cover weight of the graph: {no_cover_weight}\n'), "white", ["bold"], flush=True)

goal = False
# controlli lb / ub
if not ENV['lower_bound']:
  #  TAc.print(LANG.render_feedback("insert-lower-bound", 'Insert lower bound: '), "yellow", ["bold"], flush=True)
  #  lower_bound = TALinput(int, 1, TAc=TAc)[0]
  lower_bound = 1
else:
  if ENV['lower_bound'] <= 0:
    lower_bound = ENV['lower_bound'] + 1
  else:
    lower_bound = ENV['lower_bound']
  
if not ENV['upper_bound']:
  #  TAc.print(LANG.render_feedback("insert-upper-bound", 'Insert upper bound: '), "yellow", ["bold"], flush=True)
  #  upper_bound = TALinput(int, 1, TAc=TAc)[0]
  if weighted:
    upper_bound = no_cover_weight
  else:
    upper_bound = instance['num_vertices']
else:
  upper_bound = ENV['upper_bound']

if not weighted:
  if upper_bound > instance['num_vertices']:
    TAc.print(LANG.render_feedback("wrong-ub-value", f'Upper bound must be lower than {instance["num_vertices"]}. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  if upper_bound < lower_bound:
    TAc.print(LANG.render_feedback("wrong-lb-ub-value", f'Upper bound must be greater than lower bound . Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  if lower_bound <= 0:
    TAc.print(LANG.render_feedback("wrong-lb-value", f'Lower bound must be greater than 0. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  if ENV['goal_2apx']:
    if upper_bound > 2*int(size_sol):
      TAc.print(LANG.render_feedback("wrong-ub-value.apx", f'Upper bound must be lower than than {2*int(size_sol)}. Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)
else:
  if upper_bound > no_cover_weight:
    TAc.print(LANG.render_feedback("wrong-ub-value-w", f'Upper bound must be lower than {no_cover_weight}. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  if upper_bound < lower_bound:
    TAc.print(LANG.render_feedback("wrong-lb-ub-value", f'Upper bound must be greater than lower bound. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  if lower_bound <= 0:
    TAc.print(LANG.render_feedback("wrong-lb-value", f'Lower bound must be greater than 0. Aborting.\n'), "red", ["bold"], flush=True)
    exit(0)
  if ENV['goal_2apx']:
    if upper_bound > 2*int(weight_sol):
      TAc.print(LANG.render_feedback("wrong-ub-value.apx", f'Upper bound must be lower than than {2*int(weight_sol)}. Aborting.\n'), "red", ["bold"], flush=True)
      exit(0)

if not weighted:
  if not ENV['goal_2apx']:
    if int(size_sol) <= upper_bound and int(size_sol) >= lower_bound:
      if int(size_sol) == lower_bound and int(size_sol) == upper_bound:
        TAc.OK()
        TAc.print(LANG.render_feedback("goal", f'You reached the goal! The size of the vertex cover is exactly {size_sol}!'), "green", ["bold"], flush=True)
        TAc.print(LANG.render_feedback("sol-exact", f'Solution: node cover {vc_sol}'), "green", ["bold"], flush=True)
        goal = True
      else:
        TAc.print(LANG.render_feedback("size-in-interval", f'We agree, the size of the vertex cover is contained in the interval {lower_bound}-{upper_bound}'), "green", ["bold"], flush=True)
    elif int(size_sol) > upper_bound:
      TAc.print(LANG.render_feedback("size-too-high", f'The size of the vertex cover is outside the given interval {lower_bound}-{upper_bound}. Hint: try a higher upper bound!'), "red", ["bold"], flush=True)
    elif int(size_sol) < lower_bound:
      TAc.print(LANG.render_feedback("size-too-low", f'The size of the vertex cover is outside the given interval {lower_bound}-{upper_bound}. Hint: try a smaller lower bound!'), "red", ["bold"], flush=True)
  else:
    if upper_bound >= int(size_apx) and upper_bound <= 2*int(size_sol) and lower_bound <= int(size_apx):
      if upper_bound == int(size_apx) and lower_bound == int(size_apx):
        TAc.OK()
        TAc.print(LANG.render_feedback("goal-apx", f'You reached the goal! The size of the vertex cover is exactly {size_apx}!'), "green", ["bold"], flush=True)
        TAc.print(LANG.render_feedback("sol-approx", f'Solutions: node cover {sol_apx} - maximal matching {matching}'), "green", ["bold"], flush=True)
        goal = True
      else:
        TAc.print(LANG.render_feedback("size-in-interval-apx", f'We agree, the size of the 2-approximated  vertex cover is contained in the interval {lower_bound}-{upper_bound}'), "green", ["bold"], flush=True)
    elif 2*int(size_sol) < upper_bound or upper_bound < int(size_apx):
      TAc.print(LANG.render_feedback("size-too-high-apx", f'The size of the 2-approximated vertex cover is outside the given interval {lower_bound}-{upper_bound}. Hint: try a higher upper bound!'), "red", ["bold"], flush=True)
    elif int(size_sol) > lower_bound: ### Correggere
      TAc.print(LANG.render_feedback("size-too-low-apx", f'The size of the 2-approximated vertex cover is outside the given interval {lower_bound}-{upper_bound}. Hint: try a smaller lower bound!'), "red", ["bold"], flush=True)
    
  print('\n')
else:
  if not ENV['goal_2apx']:
    if weight_sol <= upper_bound and weight_sol >= lower_bound:
      if weight_sol == lower_bound and weight_sol == upper_bound:
        TAc.OK()
        TAc.print(LANG.render_feedback("goal-w", f'You reached the goal! The minimum weight of the vertex cover is exactly {weight_sol}!'), "green", ["bold"], flush=True)
        TAc.print(LANG.render_feedback("sol-exact-w", f'Solution: node cover {vc_sol}'), "green", ["bold"], flush=True)
        goal = True
      else:
        TAc.print(LANG.render_feedback("weight-in-interval", f'We agree, the minimum weight of the vertex cover is contained in the interval {lower_bound}-{upper_bound}'), "green", ["bold"], flush=True)
    elif weight_sol > upper_bound:
      TAc.print(LANG.render_feedback("weight-too-high", f'The minimum weight of the vertex cover is outside the given interval {lower_bound}-{upper_bound}. Hint: try a higher upper bound!'), "red", ["bold"], flush=True)
    elif weight_sol < lower_bound:
      TAc.print(LANG.render_feedback("weight-too-low", f'The minimum weight of the vertex cover is outside the given interval {lower_bound}-{upper_bound}. Hint: try a smaller lower bound!'), "red", ["bold"], flush=True)
  else:
    print(weight_sol)
    if upper_bound >= int(weight_apx) and lower_bound <= int(weight_apx):
      if upper_bound == int(weight_apx) and lower_bound == int(weight_apx):
        TAc.OK()
        TAc.print(LANG.render_feedback("goal-apx-w", f'You reached the goal! The weight of the vertex cover is exactly {weight_apx}!'), "green", ["bold"], flush=True)
        TAc.print(LANG.render_feedback("sol-approx-w", f'Solution: node cover {sol_apx}'), "green", ["bold"], flush=True)
        goal = True
      else:
        TAc.print(LANG.render_feedback("size-in-interval-apx", f'We agree, the size of the 2-approximated vertex cover is contained in the interval {lower_bound}-{upper_bound}'), "green", ["bold"], flush=True)
    elif 2*int(weight_sol) < upper_bound or upper_bound < int(weight_apx):
      TAc.print(LANG.render_feedback("weight-too-high-apx", f'The weight of the 2-approximated vertex cover is outside the given interval {lower_bound}-{upper_bound}. Hint: try a higher upper bound!'), "red", ["bold"], flush=True)
    elif int(weight_apx) < lower_bound: ### Correggere
      TAc.print(LANG.render_feedback("weight-too-low-apx", f'The weight of the 2-approximated vertex cover is outside the given interval {lower_bound}-{upper_bound}. Hint: try a smaller lower bound!'), "red", ["bold"], flush=True)
    
  print('\n')


if ENV['plot']:
  if weighted:
    vcl.plot_graph(instance['graph'], 1)
  else:
    vcl.plot_graph(instance['graph'])

if goal and ENV['plot_sol']:
  if not ENV['goal_2apx']:
    if weighted:
      vcl.plot_mvc(instance['graph'], vc_sol, [], 1)
    else:
      vcl.plot_mvc(instance['graph'], vc_sol, [])
  else:
    if weighted:
      vcl.plot_mvc(instance['graph'], sol_apx, [], 1)
    else:
      vcl.plot_2app_vc(instance['graph'], sol_apx, [eval(t) for t in matching.replace(', ',',').split()])

exit(0)
