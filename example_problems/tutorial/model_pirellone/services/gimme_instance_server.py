#!/usr/bin/env python3
from sys import stderr, exit
from os import environ

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper, get_problem_path_from

import model_pirellone_lib as pl



# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_spec',str),
    ('m',int),
    ('n',int),
    ('instance_id',int),
    ('instance_solvability',str),
    ('format',str),
    ('silent',bool),
    # ('display',bool),
    # ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
if ENV['instance_spec'] == 'catalogue1':
    # Initialize ModellingProblemHelper
    mph = ModellingProblemHelper(TAc,get_problem_path_from(__file__))
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format=ENV['format'])
    instance = pl.get_instance_from_str(instance_str, format=ENV['format'])

else:
    assert ENV['instance_spec'] == 'random'
    if environ["TAL_seed"] == "random_seed":
        # adjust the ENV['seed'] value to the solvability param
        if ENV['instance_solvability'] == 'solvable':
            ENV.arg['seed'] = pl.gen_instance_seed(solvable=True)
        elif ENV['instance_solvability'] == 'unsolvable':
            ENV.arg['seed'] = pl.gen_instance_seed(solvable=False)

    # Get pirellone
    try:
        instance = pl.gen_instance(ENV['m'], ENV['n'], ENV['seed'])
        instance_str = pl.instance_to_str(instance, format=ENV['format'])
    except RuntimeError:
        TAc.print(LANG.render_feedback("error", f'It is not possible to generate an unsolvable {ENV["m"]}x{ENV["n"]} 0,1-matrix."), "red", ["bold'])
        exit(0)


# Print Instance
if ENV['silent']:
    print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'The {ENV["m"]}x{ENV["n"]} 0,1-matrix is:'), "yellow", ["bold"])
    TAc.print(pl.instance_to_str(instance, format=ENV['format']), "white", ["bold"])
    TAc.print(LANG.render_feedback("instance-descriptor", f'The instance descriptor of the above pseudo-random 0,1-matrix is <n={ENV["m"]},m={ENV["n"]},seed={ENV["seed"]}>.'), "yellow", ["bold"])

exit(0)
