#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="check_lower_bound"
args_list = [
    ('v',str),
    ('start', str),
    ('final', str),
    ('n',int),
    ('disk',int),
    ('sol',int),
    ('silent',bool),
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")


# INITIALIZATION
N = ENV['n']

# Check arguments errors
if (ENV['start'] != "all_A" and ENV['start'] != "all_B" and ENV['start'] != "all_C"):
    N = len(ENV['start'])
elif (ENV['final'] != "all_A" and ENV['final'] != "all_B" and ENV['final'] != "all_C"):
    N = len(ENV['final'])
elif (N == -1):
    TAc.print(LANG.render_feedback("arg-err", f"N!=-1 if start=all_X and final=all_X"), "red", ["bold"])
    exit(0)

# Get configurations
start = get_input_from(ENV['start'], N)
final = get_input_from(ENV['final'], N)

# Check configs error
if len(start) != len(final):
    TAc.print(LANG.render_feedback("arg-config-err", f"len(start) != len(final)"), "red", ["bold"])
    exit(0)

# Init Hanoi Tower
hanoi = HanoiTowerProblem(ENV['v'])

# Get the correct solution
user_sol = ENV['sol']
opt_sol = hanoi.getMinMovesOf(start, final, ENV['disk'])

# check the user solution
if user_sol == opt_sol:
    if not ENV['silent']:
        TAc.print(LANG.render_feedback("sol-equal", f'user_sol == opt_sol'), "green", ["bold"])

else:
    TAc.print(LANG.render_feedback("sol-wrong", f'user_sol != opt_sol'), "red", ["bold"])

    # Provide feedback
    if ENV["feedback"] == "true_val":
        TAc.print(LANG.render_feedback("get-sol", f'opt_sol = {opt_sol}'), "red", ["bold"])
    
    elif ENV["feedback"] == "smaller_or_bigger":
        if user_sol < opt_sol:
            TAc.print(LANG.render_feedback("sol-less", f'user_sol < opt_sol'), "red")
        else:
            TAc.print(LANG.render_feedback("sol-more", f'user_sol > opt_sol'), "red")

exit(0)
