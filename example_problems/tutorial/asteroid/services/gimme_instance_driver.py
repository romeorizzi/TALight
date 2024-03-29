#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors

import asteroid_lib as pl
#from math_modeling import ModellingProblemHelper, get_problem_path_from


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_spec',str),
    ('m',int),
    ('n',int),
    ('instance_id',int),
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
    mph = ModellingProblemHelper(get_problem_path_from(__file__))
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format=ENV['format'])
    instance = pl.get_instance_from_str(instance_str, format=ENV['format'])

else:
    # Get instance
    assert ENV['instance_spec'] == 'random'
    instance = pl.gen_instance(ENV['m'], ENV['n'], ENV['seed'])
    instance_str = pl.instance_to_str(instance, format=ENV['format'])


# Print Instance
if ENV['silent']:
    print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'The {ENV["m"]}x{ENV["n"]} 0,1-matrix is:'), "yellow", ["bold"])
    TAc.print(pl.instance_to_str(instance, format=ENV["format"]), "white", ["bold"])
    TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])

exit(0)
