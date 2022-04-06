#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

from math_modeling import ModellingProblemHelper

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('instance_format',str),
    ('sol_format',str),
    ('m',int), 
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('MIN_VAL_BIG',int),
    ('MAX_VAL_BIG',int),
    ('seed',str),
    ('big_seed',str),
    ('path',str),
    ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
if ENV['silent']:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
else:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

if ENV['source'] != 'catalogue':
    # Get random instance
    if ENV['seed'] == 'random_seed':
        seed = 0
    else:
        seed = int(ENV['seed'])
    if ENV['big_seed'] == 'random_seed':
        big_seed = 0
    else:
        big_seed = int(ENV['big_seed'])
    instance = tl.instances_generator(1, 1, ENV['MIN_VAL'], ENV['MAX_VAL'], ENV['n'], ENV['n'], ENV['m'], ENV['m'], ENV['MIN_VAL_BIG'], ENV['MAX_VAL_BIG'], seed, big_seed, ENV['path'],ENV['use'])[0]
    instance_str = tl.instance_to_str(instance, format_name=ENV['instance_format'])
    output_filename = f"random_instance_{seed}_{big_seed}.{ENV['instance_format']}.txt" 
else: # Get instance from catalogue
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR)
    if ENV['use'] == 'single' or ENV['use'] == 'double':
        instance_str=mph.get_file_str_from_path_by_use(ENV['use'], ENV['instance_format'])
    else:
        instance_str = mph.get_file_str_from_id(ENV['instance_id'], format_name=tl.format_name_to_file_extension(ENV['instance_format'], 'instance'))
    instance = tl.get_instance_from_str(instance_str, instance_format_name=ENV['instance_format'])
    output_filename = f"instance_{ENV['instance_id']}.{ENV['instance_format']}.txt"

# Print Instance
if ENV['silent']:
    if ENV['display']:
        print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {len(instance[0])} character and the second string of {len(instance[1])} character are:'), "yellow", ["bold"])
    if ENV['display']:
        TAc.print(instance_str, "white", ["bold"])
        if ENV['source'] != 'catalogue':
            TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])
if ENV['download']:
    TALf.str2output_file(instance_str,output_filename)
