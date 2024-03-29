#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors

import model_pirellone_lib as pl
from math_modeling import ModellingProblemHelper, get_problem_path_from



# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('input_mode',str),
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
if ENV['input_mode'] == 'instance_id':
    if ENV['instance_id'] == -1:
        TAc.print(LANG.render_feedback("no-mandatory-instanceid", f"If you select (input_mode='instance_id') then the (instance_id) argument must be differente from -1"), "red", ["bold"])
        exit(0)
    # Initialize ModellingProblemHelper
    mph = ModellingProblemHelper(TAc,get_problem_path_from(__file__))
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format=ENV['format'])
    instance = pl.get_instance_from_str(instance_str, format=ENV['format'])

else:
    if ENV['input_mode'] == 'random':
        # adjust solvability param
        if ENV['instance_solvability'] == 'solvable':
            solvable = True
        elif ENV['instance_solvability'] == 'unsolvable':
            solvable = False
        else:
            solvable = None
        # get random seed
        seed = pl.gen_instance_seed(solvable)

    elif ENV['input_mode'] == 'seed':
        if ENV['seed'] == 0:
            TAc.print(LANG.render_feedback("no-mandatory-seed", f"If you select (input_mode='seed') then the (seed) argument must be differente from 000000"), "red", ["bold"])
            exit(0)
        # get custom seed
        seed = ENV['seed']

    # Get pirellone
    try:
        instance = pl.gen_instance(ENV['m'], ENV['n'], seed)
        instance_str = pl.instance_to_str(instance, format=ENV['format'])
    except RuntimeError:
        TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
        exit(0)


# Print Instance
if ENV['silent']:
    print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f"The matrix {ENV['m']}x{ENV['n']} is:"), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance", f"{pl.instance_to_str(instance, format=ENV['format'])}"), "white", ["bold"])
    TAc.print(LANG.render_feedback("seed", f"The seed is: {seed}"), "yellow", ["bold"])

exit(0)
