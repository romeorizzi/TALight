#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl
from utils_services import process_instance, process_user_seq_sol

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
(instance, opt_sol) = process_instance(ENV, TAc, LANG)
# TAc.print(LANG.render_feedback("spoiler", f"{pl.subset_to_str(opt_sol)}"), "green", ["bold"])

# Get long solution
padded_sol = pl.get_padded_sol(ENV['m'], ENV['n'], pl.subset_to_seq(opt_sol), pad_size=6)
TAc.print(LANG.render_feedback("paddedsol-title", "Too long solution: (r=row, c=col)"), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("paddedsol", f"{pl.seq_to_str(padded_sol)}"), "white", ["reverse"])

# Get User solution
TAc.print(LANG.render_feedback("usersol-title", "Your short solution: "), "yellow", ["reverse"])
user_sol = TALinput(str, regex="^(|(r|R|c|C)[1-9][0-9]*)$", sep=' ', TAc=TAc)
process_user_seq_sol(ENV, TAc, LANG, user_sol)

# Get Goal
if ENV['goal'] == "m_plus_n":
    len_goal = ENV['n'] + ENV['m']
elif ENV['goal'] == "m_plus_n_half":
    len_goal = round((ENV['n'] + ENV['m']) / 2)
elif ENV['goal'] == "min":
    len_goal = len(opt_sol)


# Check user solution
user_sol_subset = pl.seq_to_subset(user_sol, ENV['m'], ENV['n'])
is_correct = (pl.get_light_on_after(instance, user_sol_subset) == 0)

if not is_correct:
    TAc.NO()
    TAc.print(LANG.render_feedback("solvable-not-correct", "Some lights remained on, but could have been turned off!"), "red", ["bold"])
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
