#!/usr/bin/env python3

from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl
from utils_lang import process_inputs

# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="get_our_sol"
args_list = [
    ('input_mode',str),
    ('m',int), 
    ('n',int),
    ('seed',str),
    ('coding',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get pirellone and solution
(instance, opt_sol) = process_inputs(ENV, TAc, LANG)

# Print instance
TAc.print(LANG.render_feedback("instance-title", f"The matrix {ENV['m']}x{ENV['n']} is:"), "yellow", ["bold"])
TAc.print(LANG.render_feedback("instance", f"{pl.get_str_from_pirellone(instance)}"), "white", ["bold"])

# Print solution
TAc.print(LANG.render_feedback("solution-title", f"The optimal solution for this instance is:"), "green", ["bold"])
TAc.print(LANG.render_feedback("solution", f"{pl.get_str_from_sol(opt_sol, ENV['coding'])}"), "white", ["reverse"])

exit(0)
