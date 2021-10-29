#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl
from utils_lang import process_instance, process_user_seq_sol

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
(instance, opt_sol) = process_instance(ENV, TAc, LANG)
# TAc.print(LANG.render_feedback("spoiler", f"{pl.sol_to_str(instance, opt_sol)}"), "green", ["bold"])

# Get user solution
user_sol = list()
TAc.print(LANG.render_feedback("usersol-title", "Your solution: "), "yellow", ["reverse"])
if ENV['sol_style'] == 'seq':
    TAc.print(LANG.render_feedback("legend-seq", f"(r=row, c=col)"), "white", ["reverse"])
    user_sol = TALinput(str, regex="^(|(r|R|c|C)[1-9][0-9]*)$", sep=' ', TAc=TAc)
    process_user_seq_sol(ENV, TAc, LANG, user_sol)
    if len(user_sol) != len(pl.subset_to_seq(opt_sol)):
        TAc.NO()
        TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "red", ["bold"])
        exit(0)
    user_sol = pl.seq_to_subset(user_sol, ENV['m'], ENV['n'])
elif ENV['sol_style'] == 'subset':
    TAc.print(LANG.render_feedback("legend-subset", f"Insert rows and then columns:\n(FirstLine=rows_switch SecondLine=cols_switch)"), "white", ["reverse"])
    rows_str = TALinput(str, num_tokens=ENV['m'], regex=f"^(0|1)$", sep=' ', TAc=TAc)
    cols_str = TALinput(str, num_tokens=ENV['n'], regex=f"^(0|1)$", sep=' ', TAc=TAc)
    user_sol.append([int(e) for e in list(rows_str)])
    user_sol.append([int(e) for e in list(cols_str)])


# Check the correctness of the user solution
if pl.are_equiv(user_sol, opt_sol):
    TAc.OK()
    TAc.print(LANG.render_feedback('correct', "This sequence turns off all lights."), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback('not-correct', "This sequence doesn't turn off all lights see what happens using your solution"), "red", ["bold"])

exit(0)
