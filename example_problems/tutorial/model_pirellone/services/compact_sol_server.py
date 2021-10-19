#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import model_pirellone_lib as pl
from services_utils import process_instance, process_user_sol

# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="compact_sol"
args_list = [
    ('input_mode',str),
    ('m',int), 
    ('n',int),
    ('seed',str),
    ('goal',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get pirellone and solution
instance, opt_sol_subset = process_instance(ENV, TAc, LANG)
opt_sol_seq = pl.subset_to_seq(opt_sol_subset)
# TAc.print(LANG.render_feedback("spoiler", f"{pl.sol_to_str(instance, opt_sol_subset)}"), "yellow", ["bold"])
# exit(0)

# Check if is unsolvable
if opt_sol_subset == pl.NO_SOL:
    TAc.print(LANG.render_feedback("unsolvable", f"The instance selected is unsolvable"), "red", ["bold"])
    exit(0)

# Get long solution
padded_sol = pl.get_padded_sol(ENV['m'], ENV['n'], opt_sol_seq, pad_size=6)
TAc.print(LANG.render_feedback("paddedsol-title", "Too long solution: (r=row, c=col)"), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("paddedsol", f"{pl.seq_to_str(padded_sol)}"), "white", ["reverse"])

# Get User solution
TAc.print(LANG.render_feedback("usersol-title", "Your short solution: "), "yellow", ["reverse"])
user_sol = process_user_sol(ENV, TAc, LANG, raw_sol=[input()], sol_style='seq')

# Get Goal
if ENV['goal'] == "m_plus_n":
    len_goal = ENV['n'] + ENV['m']
elif ENV['goal'] == "m_plus_n_half":
    len_goal = ((ENV['n'] + ENV['m']) // 2)
elif ENV['goal'] == "min":
    len_goal = len(opt_sol_seq)

# Check user solution
user_sol_subset = pl.seq_to_subset(user_sol, ENV['m'], ENV['n'])
(is_correct, certificate_of_no) = pl.check_sol(instance, user_sol_subset)

if not is_correct:
    TAc.NO()
    TAc.print(LANG.render_feedback('error', f"The solution is not correct. The pirellone cell in row={certificate_of_no[0]} and col={certificate_of_no[1]} stays on."), "red", ["bold"])
    exit(0)
else:
    TAc.print(LANG.render_feedback("solvable-correct", "All the lights have been turned off!"), "green", ["bold"])
    # provide feedback to user
    if len(user_sol) < len_goal:
        TAc.OK()
        TAc.print(LANG.render_feedback("shorter", "And your solution is shorter than what you set in goal."), "green", ["bold"])
    elif len(user_sol) == len_goal:
        TAc.OK()
        TAc.print(LANG.render_feedback("same", "And your solution is the same length as what you set in goal."), "yellow", ["bold"])
    elif len(user_sol) > len_goal:
        TAc.NO()
        TAc.print(LANG.render_feedback("bigger", "But your solution is bigger than what you set in goal but all lights are off."), "red", ["bold"])

exit(0)
