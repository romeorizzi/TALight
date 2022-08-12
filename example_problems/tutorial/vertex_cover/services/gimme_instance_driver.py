#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import random
import vertex_cover_lib as vcl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('instance_format',str),
    ('num_vertices',int),
    ('num_edges',int),
    ('weighted',bool),
    ('seed',str),
    ('silent', bool),
    ('display', bool),
    ('download',bool),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)

if ENV['silent']:
  LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
else:
  LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

if ENV['source'] != 'catalogue':
    # Get random instance
    instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'], ENV['weighted'])[0]
    instance_str = vcl.instance_to_str(instance, format_name=ENV['instance_format'])
    output_filename = f"random_instance_{ENV['seed']}.{ENV['instance_format']}.txt"
else: # Get instance from catalogue
    instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
    instance = vcl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
    output_filename = f"instance_{ENV['instance_id']}.{ENV['instance_format']}.txt"

# Print Instance
if ENV['silent']:
    if ENV['display']:
        print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'This is the instance:\n'), "yellow", ["bold"])
    if ENV['display']:
        #TAc.print(instance_str, "white", ["bold"])
        TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"])
        if ENV['source'] != 'catalogue': # display random instance
            output = ""
            output += f'\nThe parameters encoding this instance are:\nnum_vertices: {ENV["num_vertices"]}\nseed: {ENV["seed"]}'
            # TAc.print(LANG.render_feedback("output-instance", output), "yellow", ["bold"])

if ENV['download']:
    TALf.str2output_file(instance_str,output_filename)

exit(0)
