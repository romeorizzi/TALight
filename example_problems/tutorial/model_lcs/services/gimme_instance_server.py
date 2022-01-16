#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper

import model_lcs_lib as ll


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_spec',str),
    ('m',int),
    ('n',int),
    ('alphabet', str),
    ('instance_id',int),
    ('instance_format',str),
    ('silent',bool),
    ('display',bool),
    ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

if ENV['instance_spec'] == 'catalogue1':
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR )
    
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format=ENV['instance_format'])
    instance = ll.get_instance_from_str(instance_str, format=ENV['instance_format'])
    output_filename = f"instance_catalogue1_{ENV['instance_id']}.{ENV['instance_format']}"

else:
    # Get instance
    assert ENV['instance_spec'] == 'random'
    instance = ll.gen_instance(ENV['m'], ENV['n'], ENV['alphabet'], ENV['seed'])
    instance_str = ll.instance_to_str(instance, format=ENV['instance_format'])
    output_filename = f"instance_{ENV['m']}_{ENV['n']}_{ENV['seed']}.{ENV['instance_format']}"


# Print Instance
if ENV['silent']:
    if ENV['display']:
        print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {len(instance[0])} character and the second string of {len(instance[1])} character are:'), "yellow", ["bold"])
    if ENV['display']:
        TAc.print(instance_str, "white", ["bold"])
        if not ENV['instance_spec'] == 'catalogue1':
            TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])
if ENV['download']:
    fout = open(os.path.join(ENV.OUTPUT_FILES,output_filename),'w')
    print(instance_str, file=fout)
    fout.close()

exit(0)
