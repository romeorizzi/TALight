#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import os
import random
import networkx as nx
from networkx.algorithms import approximation
import vertex_cover_lib as vcl
import matplotlib
import multiprocessing

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('collection',str),
    ('instance_id',int),
    ('instance_format',str),
    ('num_vertices',int),
    ('num_edges',int),
    ('plot',bool),
    ('plot_sol',bool),
    ('seed',str),
    ('vc_sol_val',str),
    ('display',bool),
    ('silent',bool),
    ('lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

chk_backend = False
if matplotlib.get_backend() in vcl.backends:
  chk_backend = True

## Input Sources
if TALf.exists_input_file('instance'):
  instance = vcl.get_instance_from_str(TALf.input_file_as_str('instance'), instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("successful-load", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])

elif ENV["source"] == 'terminal':
  instance = {}
  instance['num_vertices'] = ENV['num_vertices']
  instance['num_edges'] = ENV['num_edges']

  #TAc.print(LANG.render_feedback("waiting-line", f'#? Waiting for the graph.\nGraph format: (x,y) (w,z) ... (n,m)\n'), "yellow")
  TAc.print(LANG.render_feedback("waiting-line", f'#? Waiting for the graph.\n'), "yellow")

  TAc.print(LANG.render_feedback("insert-edges", f'Given {ENV["num_vertices"]} vertices labelled with the naturals in the interval [0,{ENV["num_vertices"]-1}], you are now expected to enter {ENV["num_edges"]} edges. To specify an edge, simply enter its two endonodes separated by spaces.'), "yellow", ["bold"])
  edges = []
  for i in range(1,1+ENV["num_edges"]):
    TAc.print(LANG.render_feedback("insert-edge", f'Insert the two endpoints of edge {i}, that is, enter a line with two naturals in the interval [0,{ENV["num_vertices"]-1}],  separated by spaces.'), "yellow", ["bold"])
    u,v = TALinput(int, 2, TAc=TAc)
    edges.append([u,v])

  for u,v in edges:
    if u not in range(ENV['num_vertices']) or v not in range(ENV['num_vertices']):
      TAc.print(f'Edge ({u}, {v}) is not a valid edge for the graph. Aborting.\n', "red", ["bold"], flush=True)
      exit(0)

  if len(edges) != ENV['num_edges']:
    TAc.print(LANG.render_feedback("wrong-edges-number", f'\nWrong number of edges ({len(edges)} instead of {ENV["num_edges"]})\n'), "red", ["bold"])
    exit(0)

  TAc.print(LANG.render_feedback("insert-weights", f'Enter nodes weights. Format: integers separated by spaces:'), "yellow", ["bold"])
  l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

  if len(l) != ENV['num_vertices']:
    TAc.print(LANG.render_feedback("wrong-weights-number", f'\nWrong number of weights ({len(l)} instead of {ENV["num_vertices"]})\n'), "red", ["bold"])
    exit(0)

  for w in l:
    if not w.isdigit():
      TAc.print(LANG.render_feedback("wrong-weights-format", f'\nWeights must be integer numbers. Aborting.\n'), "red", ["bold"])
      exit(0)

  G = nx.Graph()
  G.add_nodes_from([int(v) for v in range(ENV['num_vertices'])])
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
  instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'], 1)[0]

else: # take instance from catalogue
  #instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance_str = TALf.get_catalogue_instancefile_as_str_from_id_collection_and_ext(ENV["collection"], ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance = vcl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
  if instance['weighted']:
    TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"], flush=True)
  else:
    TAc.print(LANG.render_feedback("graph-not-weighted", f'The instance with instance_id={ENV["instance_id"]} does not contain a weighted graph. Aborting.'), "red", ["bold"])
    exit(0)

if ENV['display']:
  TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"], flush=True)
  TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"], flush=True, end='')

  if not 'weighted' in instance:
    for n,w in nx.get_node_attributes(instance['graph'], 'weight').items():
      TAc.print(f'{w}', "white", ["bold"], flush=True, end=' ')

    print('\n', flush=True)
    

if ENV['vc_sol_val'] == '0': # manual insertion
  TAc.print(LANG.render_feedback("insert-opt-value", f'\nWrite here your conjectured approximated vertex cover for this weighted graph if you have one (format: integer numbers separated by spaces). Otherwise, if you only intend to be told about the approximation, enter "C".'), "yellow", ["bold"], flush=True)
  if ENV['plot'] and chk_backend:
    proc = multiprocessing.Process(target=vcl.plot_graph, args=(instance['graph'],))
    proc.start()
    #vcl.plot_graph(instance['graph'],1)
  answer = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG) # a quanto pare è un array: ogni elemento separato da spazio nella stringa è un elemento dell'array...
else:
  answer = ENV['vc_sol_val']

if answer[0] != 'C' and answer[0] != 'c':
  for v in answer:
    if int(v) not in instance['graph'].nodes():
      TAc.print(LANG.render_feedback("node-not-in-graph", f'Vertex {v} is not a vertex of the graph. Aborting'), "red", ["bold"], flush=True)
      if ENV['plot'] and chk_backend:
        proc.terminate()
      exit(0)

weight_ans = 0
for n,w in nx.get_node_attributes(instance['graph'], 'weight').items():
  if str(n) in answer:
    weight_ans += w 

if (ENV['source'] == "catalogue" and instance['exact_sol'] == 1) or (ENV['source'] != "catalogue"):
  appr_sol, size_sol, weight_sol = vcl.calculate_weighted_approx_vc(instance['graph'])
else:
  appr_sol = instance['sol']
  appr_sol = [int(i) for i in appr_sol.split()]
  size_sol = len(appr_sol)

  weight_sol = instance['sol_weight']


if answer[0] == 'C' or answer[0] == 'c':
  TAc.print(LANG.render_feedback("best-sol", f'A possible 2-approximated weighted vertex cover is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{appr_sol}.', "white", ["bold"], flush=True)
  TAc.print(LANG.render_feedback("size-sol", f'The size of the 2-approximated weighted vertex cover is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{size_sol}.', "white", ["bold"], flush=True)
  TAc.print(LANG.render_feedback("weight-sol", f'The weight of the 2-approximated weighted vertex cover is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{weight_sol}.', "white", ["bold"], flush=True)

else:
  is_vertex_cover, rem_edges = vcl.verify_vc(answer, instance['graph'])
  vc_sol, size_exact_sol, min_weight_sol = vcl.calculate_minimum_weight_vc(instance['graph'])
  size_ans = len(answer)

  if is_vertex_cover and (weight_ans <= 2 * min_weight_sol):
    if weight_ans == weight_sol:
      TAc.OK()
      TAc.print(LANG.render_feedback("right-best-sol", f'We agree, the solution you provided is a valid 2-approximation of the weighted vertex cover for the graph (weight={weight_ans}).'), "green", ["bold"], flush=True)
    elif weight_ans > weight_sol:
      TAc.print(LANG.render_feedback("right-sol", f'The solution you provided is a valid 2-approximation of the weighted vertex cover for the graph (weight={weight_ans}). You can improve your approximation.'), "yellow", ["bold"], flush=True)
    else:
      TAc.OK()
      TAc.print(LANG.render_feedback("new-best-sol", f'Great! The solution you provided is a valid 2-approximation of the weighted vertex cover for the graph (weight={weight_ans}) and it\'s better than mine ({weight_sol})!'), "green", ["bold"], flush=True)
      
      if ENV['source'] == 'catalogue' and not instance['exact_sol']:
        #path=os.path.join(ENV.META_DIR, 'instances_catalogue', 'all_instances')
        path=os.path.join(ENV.META_DIR, 'instances_catalogue', ENV['collection'])
        instance_filename = f'instance_{str(ENV["instance_id"]).zfill(3)}'
        answer = ' '.join(map(str, answer))
        answer = f'{answer}\n{weight_ans}'

        vcl.update_instance_txt(path, instance_filename, answer)
  else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-sol", f'We don\'t agree, the solution you provided is not a valid 2-approximation weighted vertex cover for the graph.'), "red", ["bold"], flush=True)
    if not is_vertex_cover:
      TAc.print(LANG.render_feedback("reason-wrong-sol-no_vc", f'Not a vertex cover. Edges not covered: '), "red", ["bold"], flush=True, end='')
      for t in rem_edges:
        TAc.print(f'{t} ', "red", ["bold"], flush=True, end='')
      print('\n')
    else:
      TAc.print(LANG.render_feedback("reason-wrong-sol-weight", f'Your solution weight: {weight_ans}; max 2-approximation weight: {2 * min_weight_sol}.'), "red", ["bold"], flush=True)

if ENV['plot_sol'] and chk_backend:
  if ENV['plot']:
    proc.terminate()
  if answer[0] != 'C' and answer[0] != 'c':
    answer = ' '.join(map(str,answer))
    proc1 = multiprocessing.Process(target=vcl.plot_mvc, args=(instance['graph'],answer,rem_edges,1,1))
    proc1.start()
    #vcl.plot_mvc(instance['graph'], answer, rem_edges, 1, 1)
  else:
    proc1 = multiprocessing.Process(target=vcl.plot_mvc, args=(instance['graph'],appr_sol,[],1,1))
    proc1.start()
    #vcl.plot_mvc(instance['graph'], appr_sol, [], 1, 1)

exit(0)
