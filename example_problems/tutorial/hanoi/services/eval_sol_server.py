#!/usr/bin/env python3
from sys import stderr, exit, argv
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="eval_sol"
args_list = [
    ('v',str),
    ('start', str),
    ('final', str),
    ('seed',int),
    ('num_tests',int),
    ('n_max',int),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")


# INITIALIZATION
# get seed
seed = ENV['seed']
if seed == -1:
    seed = random.randint(1,9) * 100000
    seed += random.randint(0, 99999)
TAc.print(LANG.render_feedback("print-seed", f"# seed = {seed}"), "yellow", ["bold"])

# Init Hanoi Tower
hanoi = HanoiTowerProblem(ENV['v'])


# START TESTS
num_tests = ENV['num_tests']
n_max = ENV['n_max']
if ENV['start'] != 'general' and ENV['final'] != 'general':
    # in this case the test are equal, so num_tests must be 1
    num_tests = 1

def one_test(t, n):
    # get type of configurations
    start = get_input_from(ENV['start'], n, seed, t)
    final = get_input_from(ENV['final'], n, seed, t + 1)
    TAc.print(LANG.render_feedback("print-configs", f"{start}\n{final}"), "green", ["bold"])
    
    # Get the correct solution
    opt_sol = hanoi.getMovesList(start, final)

    # Get user solution
    user_sol = list()
    while True:
        move, = TALinput(str, sep="\n", regex="^\d{1,1000}:(A|B|C)(A|B|C)$", regex_explained="N:FT  where N=DISK, F=FROM and T=TO", exceptions={"end"}, TAc=TAc)
        if move == 'end':
            break
        user_sol.append(move)

    return user_sol == opt_sol
    
# Execute all test
for t in range(1, 2*num_tests, 2):
    for n in range(1, n_max + 1):
        success = one_test(t, n)
        if success:
            TAc.print(LANG.render_feedback("success", "# success"), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("fail", "# fail"), "red", ["bold"])
            break


# END
TAc.print(LANG.render_feedback("end", "end"), "green", ["bold"])

exit(0)
