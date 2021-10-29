#!/usr/bin/env python3
from sys import stderr, exit
import random

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import model_pirellone_lib as pl
from services_utils import process_instance, process_user_sol, check_sol_with_feedback

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('input_mode',str),
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

# Print legends
user_sol = list()
TAc.print(LANG.render_feedback("usersol-title", "Your solution: "), "yellow", ["reverse"])
# Get the user solution
user_sol=[]
if ENV['sol_style'] == 'seq':
    raw_sol = TALinput(str,regex="^(r|c)(0|[1-9][0-9]{0,2})$", regex_explained="a single row or column (with indexes starting from 0). Example 1: r0 to specify the first row. Example 2: c2 to specify the third column.", line_explained="a subset of rows and columns where indexes start from 0. Example: r0 c5 r2 r7", TAc=TAc, LANG=LANG)
    for token in raw_sol:
        user_sol.append((token[0],int(token[1:])))
if ENV['sol_style'] == 'subset':
    raw_sol_rows = TALinput(bool, num_tokens=ENV['m'], line_explained=f"a line consisting of {ENV['m']} binary digits (0/1) separated by spaces, one for each row. A row gets switched iff the corresponding digit is a 1. Example: {' '.join(str(random.randint(0,1)) for _ in range(ENV['m']))}", TAc=TAc, LANG=LANG)
    for val,index in zip(raw_sol_rows,range(ENV['m'])):
        if val == 1:
            user_sol.append(('r',index))
    raw_sol_cols = TALinput(bool, num_tokens=ENV['n'], line_explained=f"a line consisting of {ENV['n']} binary digits (0/1) separated by spaces, one for each column. A column gets switched iff the corresponding digit is a 1. Example: {' '.join(str(random.randint(0,1)) for _ in range(ENV['n']))}", TAc=TAc, LANG=LANG)
    for val,index in zip(raw_sol_cols,range(ENV['n'])):
        if val == 1:
            user_sol.append(('c',index))

print(f"user_sol={user_sol}")

# Check the correctness of the user solution
check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, user_sol)

exit(0)
