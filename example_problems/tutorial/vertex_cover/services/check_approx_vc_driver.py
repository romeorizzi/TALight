#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import os
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
  TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"], flush=True)
  
if ENV['display']:
  TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"], flush=True)
  TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"], flush=True)

if ENV['vc_sol_val'] == '0': # manual insertion
  TAc.print(LANG.render_feedback("insert-opt-value", f'\nWrite here your conjectured maximal matching size for this graph if you have one. Otherwise, if you only intend to be told about the approximation, enter "C".'), "yellow", ["bold"], flush=True)
  if ENV['plot'] and chk_backend:
    proc = multiprocessing.Process(target=vcl.plot_graph, args=(instance['graph'],))
    proc.start()
    #vcl.plot_graph(instance['graph'])

  choice = TALinput(str, 1, TAc=TAc)
  if choice[0] != 'C' and choice[0] != 'c':
    if not choice[0].isdigit():
      TAc.print(LANG.render_feedback("invalid-input", f'Input must be an integer number or "C". Aborting.\n'), "red", ["bold"], flush=True)
      if ENV['plot'] and chk_backend:
        proc.terminate()
      exit(0)

    TAc.print(LANG.render_feedback("waiting-matching", f'Please, provide the maximal matching:'), "yellow", ["bold"], flush=True)
    answer = []
    for i in range(int(choice[0])):
      TAc.print(LANG.render_feedback("insert-edge", f'Insert the two endpoints of edge {i}, that is, enter a line with two naturals in the interval [0,{ENV["num_vertices"]-1}],  separated by spaces.'), "yellow", ["bold"], flush=True)
      u,v = TALinput(int, 2, TAc=TAc)
      answer.append((u,v))

else:
  answer = [eval(t) for t in ENV['vc_sol_val'].split()]
  choice = ' '

if choice[0] != 'C' and choice[0] != 'c':
  for t in answer:
    if t not in instance['graph'].edges():
      TAc.print(LANG.render_feedback("edge-not-in-graph", f'Edge {t} is not an edge of the graph. Aborting.\n'), "red", ["bold"], flush=True)
      if ENV['plot'] and chk_backend:
        proc.terminate()
      exit(0)

if (ENV['source'] == "catalogue" and instance['exact_sol'] == 1) or (ENV['source'] != "catalogue"):
  size_sol,appr_sol,max_matching = vcl.calculate_approx_vc(instance['graph'], 'greedy')
else:
  #appr_sol = instance['sol'].replace(')(',' ').replace('(','').replace(')','').replace(',','')
  #max_matching = instance['sol']
  if not instance['weighted']:
    sol = instance['sol'].split('\n')
    appr_sol = sol[0]
    max_matching = sol[1]
    size_sol = len([int(i) for i in appr_sol.split() ])
  else:
    size_sol,appr_sol,max_matching = vcl.calculate_approx_vc(instance['graph'], 'greedy')

if choice[0] == 'C' or choice[0] == 'c':
  TAc.print(LANG.render_feedback("best-sol", f'A possible 2-approximated vertex cover is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{appr_sol}.', "white", ["bold"], flush=True)
  TAc.print(LANG.render_feedback("min-maximal-matching", f'A possible maximal matching is: '), "green", ["bold"], flush=True,  end='')
  TAc.print(f'{max_matching}.', "white", ["bold"], flush=True)
  TAc.print(LANG.render_feedback("size-sol", f'The size of the 2-approximated vertex cover is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{size_sol}.', "white", ["bold"], flush=True)
else:
  for e in answer:
    if e not in instance['graph'].edges():
      TAc.print(LANG.render_feedback("edge-not-in-graph", f'Edge {e} not in the graph. Aborting.'), "red", ["bold"], flush=True)
      if ENV['plot'] and chk_backend:
        proc.terminate()
      exit(0)

  size_ans = 2 * (len(answer))
  is_vertex_cover, reason, data = vcl.verify_approx_vc(answer, instance['graph'], 1)

  if is_vertex_cover:
    if size_ans == size_sol:
      TAc.OK()
      TAc.print(LANG.render_feedback("right-best-sol", f'We agree, the solution you provided is a valid 2-approximation vertex cover for the graph.'), "white", ["bold"], flush=True)
    elif size_ans > size_sol:
      TAc.print(LANG.render_feedback("right-sol", f'The solution you provided is a valid 2-approximation vertex cover for the graph. You can improve your approximation.'), "yellow", ["bold"], flush=True)
    else:
      TAc.OK()
      TAc.print(LANG.render_feedback("new-best-sol", f'Great! The solution you provided is a valid 2-approximation vertex cover for the graph and it\'s better than mine!'), "green", ["bold"], flush=True)
      
      if ENV['source'] == 'catalogue' and not instance['exact_sol'] and not instance['weighted']:
        #path=os.path.join(ENV.META_DIR, 'instances_catalogue', 'all_instances')
        path=os.path.join(ENV.META_DIR, 'instances_catalogue', ENV['collection'])
        instance_filename = f'instance_{str(ENV["instance_id"]).zfill(3)}'
        answer = ' '.join(map(str, answer))
        risp = f'{answer.replace(",", " ").replace("(", "").replace(")","")}'
        #matching = f'{answer.replace(",",", ").replace(") (", ")(")}'
        matching = f'{answer.replace(",",", ")}'
        new_data = f'{risp}\n{matching}'

        #vcl.update_instance_txt(path, instance_filename, answer)
        vcl.update_instance_txt(path, instance_filename, new_data)

  else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-sol", f'We don\'t agree, the solution you provided is not a valid 2-approximation vertex cover for the graph.'), "red", ["bold"], flush=True)
    if reason == 1:
      TAc.print(LANG.render_feedback("edge-incident", f'Reason: edge {data} incident to another one.'), "red", ["bold"], flush=True)
    elif reason == 2:
      TAc.print(LANG.render_feedback("not-vertex-cover", f'Reason: not a vertex cover. Edges not covered: '), "red", ["bold"], flush=True, end='')
      for t in data:
        TAc.print(f'{t} ', "red", ["bold"], flush=True, end='')
    elif reason == 3:
      TAc.print(LANG.render_feedback("node-already-visited", f'Reason: vertex {data} already visited.'), "red", ["bold"], flush=True)
    
  print()
        
if ENV['plot_sol'] and chk_backend:
  if ENV['plot']:
    proc.terminate()
  if choice[0] != 'C' and choice[0] != 'c':
    vertices = ' '.join(map(str, answer)).replace('(', '').replace(') (',' ').replace(')','').replace(',',' ')
    proc1 = multiprocessing.Process(target=vcl.plot_2app_vc, args=(instance['graph'],vertices,answer))
    proc1.start()
    #vcl.plot_2app_vc(instance['graph'], vertices, answer)
  else:
    proc1 = multiprocessing.Process(target=vcl.plot_2app_vc, args=(instance['graph'],appr_sol,[eval(t) for t in max_matching.replace(', ',',').split()]))
    proc1.start()
    #vcl.plot_2app_vc(instance['graph'], appr_sol, [eval(t) for t in max_matching.replace(', ',',').split()])

exit(0)
