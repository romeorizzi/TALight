#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import asteroid_lib as al
from math_modeling import ModellingProblemHelper


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('m',int),
    ('n',int),
    ('instance_id',int),
    ('format',str),
    ('silent',bool),
    ('display',bool),
    ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:
if ENV['source'] == 'catalogue':
    # Initialize ModellingProblemHelper
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR)
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format_name=ENV['format'])
    instance = al.get_instance_from_str(instance_str, format=ENV['format'])
    if ENV['format']=='only_matrix.txt':
        m=len(instance)
    else:
        m=instance[0][0]
    output_filename = f"instance_catalogue_{ENV['instance_id']}.{ENV['format']}"

else:
    # Get instance
    assert ENV['source'] == 'random'
    instance = al.gen_instance(ENV['m'], ENV['n'], ENV['seed'])
    instance_str = al.instance_to_str(instance, format=ENV['format'])
    output_filename = f"instance_{ENV['m']}_{ENV['n']}_{ENV['seed']}.{ENV['format']}"

# Print Instance
if ENV['silent']:
        if ENV['display']:
            print(instance_str)
elif not ENV['source'] == 'catalogue':
    TAc.print(LANG.render_feedback("instance-title", f'The {ENV["m"]}x{ENV["n"]} 0,1-matrix is:'), "yellow", ["bold"])
    TAc.print(al.instance_to_str(instance, format=ENV["format"]), "white", ["bold"])
    TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])
else:
    TAc.print(LANG.render_feedback("instance-title", f'The {m}x{len(instance[1])} 0,1-matrix is:'), "yellow", ["bold"])
    TAc.print(instance_str, "white", ["bold"])

if ENV['download']:
    TALf.str2output_file(instance_str,output_filename)
exit(0)
