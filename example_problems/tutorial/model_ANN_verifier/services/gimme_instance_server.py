#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors

import model_ANN_lib as annl
from math_modeling import ModellingProblemHelper, get_problem_path_from


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_spec',str),
    ('n_nodes',str),
    ('seed',int),
    ('instance_id',int),
    ('format',str),
    ('silent',bool),
    ('display',bool),
    ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
if ENV['instance_spec'] == 'catalogue1':
    # Initialize ModellingProblemHelper
    mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], ENV['format'])
    #instance = annl.get_instance_from_str(instance_str)

else:
    # Get instance
    assert ENV['instance_spec'] == 'random'
    instance = annl.gen_instance(ENV['n_nodes'], ENV['seed'])
    instance_str = annl.instance_to_str(instance, ENV['format'])


# Print Instance
if ENV['display']: 
    if not ENV['silent']:
        TAc.print(LANG.render_feedback("instance-title", f'The ANN generated is:'), "yellow", ["bold"])
    if ENV['instance_spec'] == 'random':
        TAc.print(f'#Seed: {ENV["seed"]}', "yellow", ["bold"])
    TAc.print(instance_str, "white", ["bold"])

if ENV['download']:
    instance_file = open(f'download/instance_{ENV["seed"]}.txt', 'w')
    instance_file.write(instance_str)
    instance_file.close()

exit(0)
