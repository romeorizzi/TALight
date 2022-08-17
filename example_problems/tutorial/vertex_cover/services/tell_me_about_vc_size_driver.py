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
    ('instance_id',int),
    ('instance_format',str),
    ('num_vertices',int),
    ('num_edges',int),
    ('size',int),
    ('seed',str),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

if ENV['size'] > ENV['num_vertices']:
  TAc.print(LANG.render_feedback("invalid-k", f'\nERROR: size k can\'t be higher than the number of vertices.\n'), "red", ["bold"])
  exit(0)

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

  if ENV['weighted']:
    TAc.print(LANG.render_feedback("insert-line", f'Enter nodes weights. Format: integers separated by spaces:'), "yellow", ["bold"])
    l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

    if len(l) != ENV['num_vertices']:
      TAc.print(LANG.render_feedback("wrong-weights-number", f'\nWrong number of weight ({len(l)} instead of {ENV["num_vertices"]})\n'), "red", ["bold"])
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
  instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance = vcl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])

TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"])
TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"])

if not ENV['size']: # manual insertion
  TAc.print(LANG.render_feedback("insert-opt-value", f'\nWrite here your conjectured size k of the vertex cover: if there is a vertex cover of size at least k, you will get a positive answer. Otherwise, if you only intend to be told about the size k of the vertex cover, enter "0".'), "yellow", ["bold"])
  answer = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)
  answer = int(answer[0])

else:
  answer = ENV['size']
  
if answer > instance['num_vertices']:
  TAc.print(LANG.render_feedback("invalid-k", f'ERROR: size k can\'t be higher than the number of vertices.'), "red", ["bold"])
  exit(0)

size, vc = vcl.calculate_minimum_vc(instance['graph'])

if answer == 0 or answer == 0:
  TAc.print(LANG.render_feedback("best-sol", f'Size k of the minimum vertex cover is: {size}.'), "green", ["bold"])
else:

  if answer == size:
    TAc.OK()
    TAc.print(LANG.render_feedback("right-exact-sol", f'We agree, the graph has a vertex cover of size exactly {answer}.'), "green", ["bold"])
  elif answer > size:
    TAc.print(LANG.render_feedback("right-sol", f'Yes, the graph has a vertex cover of size at least {answer}.'), "yellow", ["bold"])
  else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-sol", f'We don\'t agree, the graph don\'t have a vertex cover of size at least {answer}.'), "red", ["bold"])

exit(0)
