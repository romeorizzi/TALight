#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper, get_problem_path_from

import model_lcs_lib as ll


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_spec',str),
    ('m',int),
    ('n',int),
    ('alphabet', str),
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
    mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format=ENV['format'])
    instance = ll.get_instance_from_str(instance_str, format=ENV['format'])

else:
    # Get instance
    assert ENV['instance_spec'] == 'random'
    instance = ll.gen_instance(ENV['m'], ENV['n'], ENV['alphabet'], ENV['seed'])
    instance_str = ll.instance_to_str(instance, format=ENV['format'])


# Print Instance
if ENV['silent']:
    print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {len(instance[0])} character and the second string of {len(instance[1])} character are:'), "yellow", ["bold"])
    TAc.print(instance_str, "white", ["bold"])
    if not ENV['instance_spec'] == 'catalogue1':
        TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])

exit(0)
