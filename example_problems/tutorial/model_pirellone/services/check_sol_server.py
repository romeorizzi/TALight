#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl
from utils_services import process_instance, process_user_sol

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
if ENV['sol_style'] == 'seq':
    opt_sol_seq = pl.subset_to_seq(opt_sol_subset)
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
# if ENV['sol_style'] == 'seq':
#     user_sol_subset = pl.seq_to_subset(user_sol, ENV['m'], ENV['n'])
#     user_sol_seq = user_sol
# else:
#     user_sol_subset = user_sol
#     user_sol_seq = pl.subset_to_seq(user_sol)

# Case1: instance unsolvable
if opt_sol_subset == pl.NO_SOL:
    if user_sol == pl.NO_SOL:
        TAc.OK()
        TAc.print(LANG.render_feedback('correct-unsolvable', "This instance is not solvable."), "green", ["bold"])
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback('wrong-unsolvable', "This instance is not solvable!"), "red", ["bold"])
    exit(0)

# Case2: user said that a solvable instance is unsolvable
if user_sol == pl.NO_SOL:
    TAc.NO()
    TAc.print(LANG.render_feedback('wrong-solvable', "This instance is solvable!"), "red", ["bold"])
    exit(0)

# Case3: equals solutions
if user_sol == (opt_sol_seq if ENV['sol_style'] == 'seq' else opt_sol_subset):
    TAc.OK()
    TAc.print(LANG.render_feedback('correct-optimal', "The solution is correct and optimal."), "green", ["bold"])
    exit(0)

# Case4: check if is minimal
if ENV['sol_style'] == 'seq':
    if len(user_sol) != len(opt_sol_seq):
        TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])
    # Ok now is better use subset style for check the solution
    user_sol = pl.seq_to_subset(user_sol, ENV['m'], ENV['n'])
else:
    if not pl.is_optimal(user_sol):
        TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])

# Case5: check if is correct
is_correct, certificate_of_no = pl.check_sol(instance, user_sol)
if is_correct:
    TAc.OK()
    TAc.print(LANG.render_feedback('correct', "The solution is correct."), "green", ["bold"])
    exit(0)
else:
    TAc.NO()
    TAc.print(LANG.render_feedback('error', f"The solution is not correct. The pirellone cell in row={certificate_of_no[0]} and col={certificate_of_no[1]} stays on."), "red", ["bold"])
    exit(0)

exit(0)
