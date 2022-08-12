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

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('instance_format',str),
    ('num_vertices',int),
    ('num_edges',int),
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
  instance['num_edges'] = ENV['num_edges']

  TAc.print(LANG.render_feedback("waiting-line", f'#? Waiting for the graph.\nGraph format: (x,y) (w,z) ... (n,m)\n'), "yellow")

  TAc.print(LANG.render_feedback("insert-line", f'Enter graph containing {ENV["num_vertices"]} vertices and {ENV["num_edges"]} edges:'), "yellow", ["bold"])
  l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

  edges = [eval(t) for t in l]

  if len(edges) != ENV['num_edges']:
    TAc.print(LANG.render_feedback("wrong-edges-number", f'\nWrong number of edges ({len(edges)} instead of {ENV["num_edges"]})\n'), "red", ["bold"])
    exit(0)

  TAc.print(LANG.render_feedback("insert-line", f'Enter nodes weights. Format: integers separated by spaces:'), "yellow", ["bold"])
  l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

  if len(l) != ENV['num_vertices']:
    TAc.print(LANG.render_feedback("wrong-weights-number", f'\nWrong number of weight ({len(l)} instead of {ENV["num_vertices"]})\n'), "red", ["bold"])
    exit(0)

  G = nx.Graph()
  G.add_nodes_from([int(v) for v in range(ENV['num_vertices'])])
  G.add_edges_from(edges)

  i = 0

  for v in G.nodes():
    G.add_node(v, weight=int(l[i]))
    i += 1

  instance['graph'] = G

  instance_str = vcl.instance_to_str(instance, format_name=ENV['instance_format'])
  output_filename = f"terminal_instance.{ENV['instance_format']}.txt"

elif ENV["source"] == 'randgen_1':
  # Get random instance
  instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'], 1)[0]

else: # take instance from catalogue
  instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance = vcl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])

if ENV['display']:
  TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"])
  TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"], end='')

  if not 'weighted' in instance:
    for n,w in nx.get_node_attributes(instance['graph'], 'weight').items():
      TAc.print(f'{w}', "white", ["bold"], end=' ')

    print('\n')
    

if ENV['vc_sol_val'] == '0': # manual insertion
  TAc.print(LANG.render_feedback("insert-opt-value", f'\nWrite here your conjectured approximated vertex cover for this weighted graph if you have one. Otherwise, if you only intend to be told about the approximation, enter "C".'), "yellow", ["bold"])
  answer = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG) # a quanto pare è un array: ogni elemento separato da spazio nella stringa è un elemento dell'array...
else:
  answer = ENV['vc_sol_val']

if (ENV['source'] == "catalogue" and instance['exact_sol'] == 1) or (ENV['source'] != "catalogue"):
  appr_sol = nx.approximation.min_weighted_vertex_cover(instance['graph'])
  #size_sol = len([int(i) for i in appr_sol.split() ])
  size_sol = len(appr_sol)
else:
  appr_sol = instance['sol'].replace(')(',' ').replace('(','').replace(')','').replace(',','')
  appr_sol = [int(i) for i in appr_sol.split()]
  size_sol = len(appr_sol)

if answer[0] == 'C' or answer[0] == 'c':
  TAc.print(LANG.render_feedback("best-sol", f'A possible 2-approximated weighted vertex cover is: '), "green", ["bold"], end='')
  TAc.print(f'{" ".join(map(str,appr_sol))}.', "white", ["bold"])
  TAc.print(LANG.render_feedback("size-sol", f'The size of the 2-approximated weighted vertex cover is: '), "green", ["bold"], end='')
  TAc.print(f'{size_sol}.', "white", ["bold"])

else:
  size_ans = 2 * (len([str(t) for t in answer]))

  if size_ans == size_sol:
    TAc.OK()
    TAc.print(LANG.render_feedback("right-best-sol", f'We agree, the solution you provided is a valid 2-approximation vertex cover for the graph.'), "green", ["bold"])
  elif size_ans > size_sol:
    TAc.print(LANG.render_feedback("right-sol", f'The solution you provided is a valid 2-approximation vertex cover for the graph. You can improve your approximation).'), "yellow", ["bold"])
  else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-sol", f'We don\'t agree, the solution you provided is not a valid 2-approximation vertex cover for the graph.'), "red", ["bold"])

exit(0)
