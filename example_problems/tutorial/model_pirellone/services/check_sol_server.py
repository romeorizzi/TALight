#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import model_pirellone_lib as pl
from services_utils import process_instance, process_user_sol, check_sol_with_feedback

# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="check_sol"
args_list = [
    ('input_mode',str),
    ('m',int), 
    ('n',int),
    ('seed',str),
    ('sol_style',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get pirellone and solution
instance, opt_sol_subset = process_instance(ENV, TAc, LANG)
# TAc.print(LANG.render_feedback("spoiler", f"{pl.sol_to_str(instance, opt_sol_subset)}"), "yellow", ["bold"])

# Print legends
user_sol = list()
TAc.print(LANG.render_feedback("usersol-title", "Your solution: "), "yellow", ["reverse"])
if ENV['sol_style'] == 'seq':
    TAc.print(LANG.render_feedback("legend-seq", f"(r=row, c=col)"), "white", ["reverse"])
elif ENV['sol_style'] == 'subset':
    TAc.print(LANG.render_feedback("legend-subset", f"Insert rows and then columns:\n(FirstLine=rows_switch SecondLine=cols_switch)"), "white", ["reverse"])

# Get the user solution
raw_sol = list()
raw_sol.append(input())
if ENV['sol_style'] == 'subset':
    raw_sol.append(input())
user_sol = process_user_sol(ENV, TAc, LANG, raw_sol)

# Check the correctness of the user solution
check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, user_sol)

exit(0)
