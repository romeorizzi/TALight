#!/usr/bin/env python3
from sys import stderr, exit, argv
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="eval_opt_num_moves"
args_list = [
    ('v',str),
    ('start', str),
    ('final', str),
    ('ok_if_congruent_modulus',int),
    ('goal',str),
    ('seed',int),
    ('num_tests',int),
    ('n_max',int),
    ('code_lang',str),
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
    modulus = ENV['ok_if_congruent_modulus']
    opt_sol = hanoi.getMinMoves(start, final)
    if modulus != 0:
        overflow = (opt_sol >= modulus)
        mod_sol = opt_sol % modulus

    # Get user solution
    t_start = monotonic()
    user_sol, = TALinput(int, TAc=TAc)
    t_end = monotonic()
    time_user = t_end - t_start # seconds in float
    
    # check the user solution
    if modulus == 0 or not overflow: #case: not modulus or modulus irrilevant
        if user_sol != opt_sol:
            return False, (start, final)

    else: # case: modulus
        if user_sol != mod_sol:
            return False, (start, final)

    return True, time_user


# Execute all test
# avg_time = 0
for t in range(1, 2*num_tests, 2):
    for n in range(1, n_max + 1):
        success, info = one_test(t, n)
        if success:
            TAc.print(LANG.render_feedback("success", "# success"), "green", ["bold"])
            # i = t * n_max + n
            # avg_time = (avg_time * i + info) / (i + 1) 

            # if abs(info[0] - info[1]) < 0.2:
            #     TAc.print(LANG.render_feedback("not_efficient", f"# not efficient {info[0]} vs {info[1]}"), "red", ["bold"])
            #     break
        else:
            TAc.print(LANG.render_feedback("fail", "# fail with {info}"), "red", ["bold"])
            break


# END
TAc.print(LANG.render_feedback("end", "end"), "green", ["bold"])

exit(0)
