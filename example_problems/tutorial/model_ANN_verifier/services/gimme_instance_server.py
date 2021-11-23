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
    ('silent',bool),
    ('display',bool),
    ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
n_nodes = ENV['n_nodes'].split(' ')
n_nodes = list(map(int, n_nodes))

if ENV['instance_spec'] == 'catalogue1':
    # Initialize ModellingProblemHelper
    mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'])
    instance = annl.get_instance_from_str(instance_str)

else:
    # Get instance
    assert ENV['instance_spec'] == 'random'
    instance = annl.gen_instance(n_nodes, ENV['seed'])
    instance_str = annl.instance_to_str(instance)


# Print Instance
if ENV['silent']:
    TAc.print(LANG.render_feedback("instance", f'Seed: {ENV["seed"]} \n{instance_str}'), "yellow", ["bold"])
else:
    TAc.print(LANG.render_feedback("instance-title", f'The ANN composed by {len(n_nodes)} layers is:'), "yellow", ["bold"])
    TAc.print(annl.instance_to_str(instance), "white", ["bold"])
    if not ENV['instance_spec'] == 'instance_id':
        TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])

exit(0)