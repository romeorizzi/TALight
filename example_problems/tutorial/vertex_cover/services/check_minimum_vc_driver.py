#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import random
import networkx as nx
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
if matplotlib.get_backend().lower() in map(str.lower,vcl.backends):
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

  G = nx.Graph()
  G.add_nodes_from([int(v) for v in range(ENV['num_vertices'])])
  G.add_edges_from(edges)

  instance['graph'] = G

  instance_str = vcl.instance_to_str(instance, format_name=ENV['instance_format'])
  output_filename = f"terminal_instance.{ENV['instance_format']}.txt"

elif ENV["source"] == 'randgen_1':
  # Get random instance
  instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'])[0]

else: # take instance from catalogue
  #instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance_str = TALf.get_catalogue_instancefile_as_str_from_id_collection_and_ext(ENV["collection"], ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance = vcl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])

if ENV['display']:
  TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"], flush=True)
  TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"], flush=True)

if ENV['vc_sol_val'] == '0': # manual insertion
  TAc.print(LANG.render_feedback("insert-opt-value", f'\nWrite here your conjectured vertex cover for this graph if you have one (format: integers separated by spaces). Otherwise, if you only intend to be told about the vertex cover, enter "C".'), "yellow", ["bold"], flush=True)
  if ENV['plot'] and chk_backend:
    proc = multiprocessing.Process(target=vcl.plot_graph, args=(instance['graph'],))
    proc.start()
    #vcl.plot_graph(instance['graph'])
  answer = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)
else:
  answer = [int(i) for i in ENV['vc_sol_val'].split()]

if answer[0] != 'C' and answer[0] != 'c':
  for v in answer:
    if int(v) not in instance['graph'].nodes():
      TAc.print(LANG.render_feedback("node-not-in-graph", f'Vertex {v} is not a vertex of the graph. Aborting'), "red", ["bold"], flush=True)
      if ENV['plot'] and chk_backend:
        proc.terminate()
      exit(0)

if (ENV['source'] == "catalogue" and instance['exact_sol'] != 1) or (ENV['source'] != "catalogue"):
  size_opt, opt_sol = vcl.calculate_minimum_vc(instance['graph'])
else:
  opt_sol = instance['sol']
  size_opt = len(instance['sol'].split())

if answer[0] == 'C' or answer[0] == 'c':
  TAc.print(LANG.render_feedback("best-sol", f'A possible minimum vertex cover is: '), "green", ["bold"], flush=True, end='') 
  TAc.print(f'{opt_sol}.', "white", ["bold"], flush=True)
  TAc.print(LANG.render_feedback("size-sol", f'The size of the minimum vertex cover is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{size_opt}.', "white", ["bold"], flush=True)
else:
  right_sol, rem_edges = vcl.verify_vc(answer, instance['graph'], 1)
  size_ans = len(answer)

  if right_sol:
    if size_ans == size_opt:
      TAc.OK()
      TAc.print(LANG.render_feedback("right-best-sol", f'We agree, the solution you provided is a valid minimum vertex cover for the graph.'), "green", ["bold"], flush=True)
    elif size_ans > size_opt:
      TAc.print(LANG.render_feedback("right-sol-not-min", f'The solution you provided is a valid vertex cover for the graph. However it`s not minimum (your size is {size_ans}).'), "yellow", ["bold"], flush=True)
  else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-sol", f'We don\'t agree, the solution you provided is not a valid vertex cover for the graph. Edges not covered: '), "red", ["bold"], flush=True, end='')
    for t in rem_edges:
      TAc.print(f'{t} ', "red", ["bold"], flush=True, end='')
    print('\n')

if ENV['plot_sol'] and chk_backend:
  if ENV['plot']:
    proc.terminate()
  if answer[0] != 'C' and answer[0] != 'c':
    answer = ' '.join(map(str,answer))
    proc1 = multiprocessing.Process(target=vcl.plot_mvc, args=(instance['graph'], answer, rem_edges))
    proc1.start()
    #vcl.plot_mvc(instance['graph'], answer, rem_edges)
  else:
    proc1 = multiprocessing.Process(target=vcl.plot_mvc, args=(instance['graph'], opt_sol, []))
    proc1.start()
    #vcl.plot_mvc(instance['graph'], opt_sol, [])
    
exit(0)
