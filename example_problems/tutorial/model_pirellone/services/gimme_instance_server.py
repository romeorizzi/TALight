#!/usr/bin/env python3

from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors

import pirellone_lib as pl



# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="gimme_instance"
args_list = [
    ('input_mode',str),
    ('m',int),
    ('n',int),
    ('seed',int),
    ('instance_solvability',str),
    ('silent',bool),
    # ('display',bool),
    # ('download',bool),
    ('lang',str),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
if ENV['input_mode'] == 'random':
    # adjust solvability param
    if ENV['instance_solvability'] == 'solvable':
        solvable = True
    elif ENV['instance_solvability'] == 'unsolvable':
        solvable = False
    else:
        solvable = None
    # get random seed
    seed = pl.gen_pirellone_seed(solvable)

elif ENV['input_mode'] == 'seed':
    if ENV['seed'] == 0:
        TAc.print(LANG.render_feedback("no-mandatory-seed", f"If you select (input_mode='seed') then the (seed) argument must be differente from 000000"), "red", ["bold"])
        exit(0)
    # get custom seed
    seed = ENV['seed']

# Get pirellone
try:
    instance = pl.gen_pirellone(ENV['m'], ENV['n'], seed)
except RuntimeError:
    TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
    exit(0)

# Print Instance
if ENV['silent']:
    # print(f"{ENV['m']} {ENV['n']}")
    print(pl.pirellone_to_str(instance))
else:
    TAc.print(LANG.render_feedback("instance-title", f"The matrix {ENV['m']}x{ENV['n']} is:"), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance", f"{pl.pirellone_to_str(instance)}"), "white", ["bold"])
    TAc.print(LANG.render_feedback("seed", f"The seed is: {seed}"), "yellow", ["bold"])

exit(0)