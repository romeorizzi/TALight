#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import random
import networkx as nx
import vertex_cover_lib as vcl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
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

## Input Sources
if TALf.exists_input_file('instance'):
  instance = vcl.get_instance_from_str(TALf.input_file_as_str('instance'), instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("successful-load", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])

elif ENV["source"] == 'terminal':
  instance = {}
  instance['num_vertices'] = ENV['num_vertices']

  graph = []
  TAc.print(LANG.render_feedback("waiting-line", f'#? Waiting for the graph.\nGraph format: (x,y) (w,z) ... (n,m) \n'), "yellow")

  TAc.print(LANG.render_feedback("insert-line", f'Enter graph containing {ENV["num_vertices"]} vertices and {ENV["num_edges"]}:'), "yellow", ["bold"])
  l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)
  
  edges = [eval(t) for t in l]

  if len(edges) != ENV['num_edges']:
    TAc.print(LANG.render_feedback("wrong-edges-number", f'\nWrong number of edges ({len(edges)} instead of {ENV["num_edges"]})\n'), "red", ["bold"])
    exit(0)

  TAc.print(LANG.render_feedback("insert-weights", f'Enter nodes weights. Format: integers separated by spaces:'), "yellow", ["bold"])
  l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

  if len(l) != ENV['num_vertices']:
    TAc.print(LANG.render_feedback("wrong-weights-number", f'\nWrong number of weights ({len(l)} instead of {ENV["num_vertices"]})\n'), "red", ["bold"])
    exit(0)

  G = nx.Graph()
  G.add_edges_from(edges)

  instance['graph'] = G

  instance_str = vcl.instance_to_str(instance, format_name=ENV['instance_format'])
  output_filename = f"terminal_instance.{ENV['instance_format']}.txt"

elif ENV["source"] == 'randgen_1':
  # Get random instance
  instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'], 1)[0]

else: # take instance from catalogue
  instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance = vcl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"], flush=True)

if ENV['display']:
  TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"], flush=True)
  TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"], flush=True)

if ENV['vc_sol_val'] == '0': # manual insertion
  TAc.print(LANG.render_feedback("insert-opt-value", f'\nWrite here your conjectured maximum weight independent set for this graph if you have one. Otherwise, if you only intend to be told about the independent set, enter "C".'), "yellow", ["bold"], flush=True)
  if ENV['plot']:
    vcl.plot_graph(instance['graph'],1)
  answer = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)
else:
  answer = ENV['vc_sol_val']

for v in answer:
  if int(v) not in instance['graph'].nodes():
    TAc.print(LANG.render_feedback("node-not-in-graph", f'Vertex {v} is not a vertex of the graph. Aborting'), "red", ["bold"], flush=True)
    exit(0)

opt_sol, size_opt, weight_opt = vcl.calculate_minimum_weight_vc(instance['graph'])
opt_sol = opt_sol.split()
opt_sol = [int(x) for x in opt_sol]
ind_set = []

#for v in range(instance['num_vertices']):
for v in instance['graph'].nodes():
  if v not in opt_sol:
    ind_set.append(v)

weight_indset = 0
for n,w in nx.get_node_attributes(instance['graph'], 'weight').items():
  if n in ind_set:
    weight_indset += w

ind_set = ' '.join(map(str, ind_set))

if answer[0] == 'C' or answer[0] == 'c':
  TAc.print(LANG.render_feedback("best-sol", f'The maximum weight independent set is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{ind_set}.', "white", ["bold"], flush=True)
  TAc.print(LANG.render_feedback("size-sol", f'The size of the maximum weight independent set is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{instance["num_vertices"] - size_opt}.', "white", ["bold"], flush=True)
  TAc.print(LANG.render_feedback("weight-sol", f'The maximum weight of the independent set is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{weight_indset}.', "white", ["bold"], flush=True)
else:
  ind_set_check = True
  vc_sol = vcl.verify_vc(answer, instance['graph'])
  answer = [int(x) for x in answer]
  size_ans = len(answer)
  weight_ans = 0
  for n,w in nx.get_node_attributes(instance['graph'], 'weight').items():
    if n in answer:
      weight_ans += w
  edges = list(instance['graph'].edges())

  if not vc_sol:
    rem_edges = []
    # Controllo che i nodi non siano collegati da un arco
    for i in range(size_ans -1):
      for ii in range(i+1,size_ans):
        edge = (answer[i],answer[ii])
        edge = tuple(sorted(edge))

        if edge in edges:
          ind_set_check = False
          rem_edges.append(edge)
          break

      #if not ind_set_check:
      #  break

    if ind_set_check:
      if weight_ans == weight_indset:
        TAc.OK()
        TAc.print(LANG.render_feedback("right-best-sol", f'We agree, the solution you provided is a valid maximum weight independent set for the graph.'), "green", ["bold"], flush=True)
      elif weight_ans > weight_indset:
        TAc.print(LANG.render_feedback("right-sol-not-min", f'The solution you provided is not a maximum weight independent set.'), "yellow", ["bold"], flush=True)
    else:
      TAc.NO()
      TAc.print(LANG.render_feedback("wrong-sol", f'We don\'t agree, the solution you provided is not a valid maximum weight independent set for the graph. These edges connect nodes: '), "red", ["bold"], flush=True)
      for t in rem_edges:
        TAc.print(f'{t} ', "red", ["bold"], flush=True, end='')
      print('\n')
  else:
    TAc.NO()
    TAc.print(LANG.render_feedback("vertex-cover", f'We don\'t agree, the solution you provided is not a valid independent set for the graph: you provide a vertex cover.'), "red", ["bold"], flush=True)

if ENV['plot_sol']:
  if answer[0] != 'C' and answer[0] != 'c':
    answer = ' '.join(map(str,answer))
    vcl.plot_indset(instance['graph'], answer, rem_edges, 1)
  else:
    vcl.plot_indset(instance['graph'], ind_set, [], 1)

exit(0)
