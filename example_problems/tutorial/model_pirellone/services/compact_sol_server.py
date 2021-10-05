#!/usr/bin/env python3

from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl
from utils_lang import get_inputs

# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="compact_sol"
args_list = [
    ('input_mode',str),
    ('m',int), 
    ('n',int),
    ('seed',str),
    ('goal',str),
    ('level',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get parameters
m = ENV['m']
n = ENV['n']

# Get pirellone and solution
(instance, opt_sol) = get_inputs(ENV, TAc, LANG)
TAc.print(LANG.render_feedback("spoiler", f"{opt_sol}"), "green", ["bold"])

# Get Difficult
if ENV['level'] == "easy":
    pad_size = 4
elif ENV['level'] == "medium":
    pad_size = 6
elif ENV['level'] == "hard":
    pad_size = 8

# Get long solution
padded_sol = pl.get_padded_sol(m, n, opt_sol, pad_size)
TAc.print(LANG.render_feedback("paddedsol-title", "Too long solution: (r=row, c=col)"), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("paddedsol", f"{pl.get_str_from_sol(padded_sol)}"), "white", ["reverse"])

# Get User solution
TAc.print(LANG.render_feedback("usersol-title", "Your short solution: "), "yellow", ["reverse"])
user_sol = TALinput(str, regex="^|[a-zA-Z][0-9]+$", sep=' ', TAc=TAc)
if user_sol == ['']:    # To manage the case 'zero moves'
    user_sol.clear()

# Get Goal
if ENV['goal'] == "m_plus_n":
    len_goal = n + m
elif ENV['goal'] == "m_plus_n_half":
    len_goal = round((n + m) / 2)
elif ENV['goal'] == "min":
    len_goal = len(opt_sol)

# Check user solution
try:
    is_correct, min_lights = pl.check_off_lights(instance, user_sol)
    print(min_lights)
except RuntimeError as err:
    name = err.args[0]
    if name == 'invalid-cmd':
        TAc.print(LANG.render_feedback("invalid-cmd", f'# Error! ({err.args[1]}) is a invalid command.\nThe only command available are:\n- (rI) with 1 < I < m.\n- (cJ) with 1 < J < n.'), "red", ["bold"])
    elif name == 'row-index-exceeds-m':
        TAc.print(LANG.render_feedback("row-index-exceeds-m", f'# Error! In your solution the move ({err.args[1]}) is not applicable. Indeed: {err.args[2]} > {err.args[3]}.'), "red", ["bold"])
    elif name == 'row-index-exceeds-m':
        TAc.print(LANG.render_feedback("col-index-exceeds-m", f'# Error! In your solution the move ({err.args[1]}) is not applicable. Indeed: {err.args[2]} > {err.args[3]}.'), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback("error", f'# Error! {err}'), "red", ["bold"])
    exit(0)

# CASE1: solvable
if min_lights == 0:
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

# CASE2: unsolvable
else:
    if not is_correct:
        TAc.NO()
        TAc.print(LANG.render_feedback("unsolvable-not-correct", "the maximum number of lights possible has NOT been turned off!"), "red", ["bold"])
    else:
        TAc.OK()
        TAc.print(LANG.render_feedback("unsolvable-correct", "The maximum number of lights possible has been turned off!"), "green", ["bold"])

exit(0)
