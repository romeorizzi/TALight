#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

from math_modeling import ModellingProblemHelper

import model_lcs_lib as ll

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('generator',str),
    ('m',int),
    ('n',int),
    ('alphabet', str),
    ('instance_format',str),
    ('silent',bool),
    ('display',bool),
    ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

if ENV['source'] == 'random':
    # Get random instance
    if ENV['generator'] == 'randgen_1':
        instance = ll.instance_randgen_1(ENV['m'], ENV['n'], ENV['alphabet'], ENV['seed'])
    else:
        assert False
    instance_str = ll.instance_to_str(instance, format_name=ENV['instance_format'])
    output_filename = f"instance_{ENV['m']}_{ENV['n']}_{ENV['seed']}.{ENV['instance_format']}"
else:
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR)
    
    # Get instance from catalogue
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format_name=ll.format_name_to_file_extension(ENV['instance_format'], 'instance'))
    instance = ll.get_instance_from_str(instance_str, instance_format_name=ENV['instance_format'])
    output_filename = f"instance_catalogue1_{ENV['instance_id']}.{ENV['instance_format']}"



# Print Instance
if ENV['silent']:
    if ENV['display']:
        print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {len(instance[0])} character and the second string of {len(instance[1])} character are:'), "yellow", ["bold"])
    if ENV['display']:
        TAc.print(instance_str, "white", ["bold"])
        if not ENV['source'] == 'catalogue1':
            TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])
if ENV['download']:
    TALf.str2output_file(instance_str,output_filename)
 
exit(0)
