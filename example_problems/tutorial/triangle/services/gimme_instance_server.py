#!/usr/bin/env python3
from sys import stderr, exit
import random

from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('silent',bool),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
if ENV['seed'] == 0:
    # get random seed
    seed = random.randrange(1,1000000)
else:
    seed = ENV['seed']

# Get Triangle
instance = tl.random_triangle(ENV['n'], ENV['MIN_VAL'], ENV['MAX_VAL'], seed)

# Print Instance
if ENV['silent']:
    tl.print_triangle(instance)
else:
    TAc.print(LANG.render_feedback("show_instance", f"The triangle you asked for is:"), "yellow", ["bold"])
    tl.print_triangle(instance)
    TAc.print(LANG.render_feedback("seed", f"The seed is: {seed}"), "yellow", ["bold"])

exit(0)
