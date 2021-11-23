#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import model_pirellone_lib as pl
from services_utils import process_instance, get_user_sol, check_sol_with_feedback

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_spec',str),
    ('m',int), 
    ('n',int),
    ('sol_style',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get pirellone and solution
instance, opt_sol_subset = process_instance(ENV, TAc, LANG)
# TAc.print(LANG.render_feedback("spoiler", f"{pl.sol_to_str(instance, opt_sol_subset)}"), "yellow", ["bold"])

# Get user sol
user_sol = get_user_sol(ENV, TAc, LANG, style=ENV['sol_style'])

# Check the correctness of the user solution
check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, user_sol, m=ENV['m'], n=ENV['n'])

exit(0)
