#!/usr/bin/env python3
from sys import stderr, exit, argv
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator, HanoiTowerProblem


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
# LANG.manage_opening_msg()



# START CODING YOUR SERVICE: 
# get seed
seed = ENV['seed']
if seed == -1:
    seed = random.randint(1,9) * 100000
    seed += random.randint(0, 99999)
TAc.print(LANG.render_feedback("print-seed", f"# seed = {seed}"), "yellow", ["bold"])

# Init Hanoi Tower and configGenerator
hanoi = HanoiTowerProblem(ENV['v'])
gen = ConfigGenerator(seed)


# Functions
def one_test(n):
    # get type of configurations
    start, final, error = gen.getConfigs(ENV['start'], ENV['final'], n)
    assert error == None
    TAc.print(LANG.render_feedback("print-configs", f"{start}\n{final}"), "green", ["bold"])
    
    # Get the correct solution
    modulus = ENV['ok_if_congruent_modulus']
    opt_answ = hanoi.getMinMoves(start, final)
    if modulus != 0:
        overflow = (opt_answ >= modulus)
        mod_answ = opt_answ % modulus

    # Get user answer
    t_start = monotonic()
    user_answ, = TALinput(int, TAc=TAc)
    t_end = monotonic()
    time_user = t_end - t_start # seconds in float
    
    # check the user answer
    if modulus == 0 or not overflow: #case: not modulus or modulus irrilevant
        if user_answ != opt_answ:
            return False, None
    else: # case: modulus
        if user_answ != mod_answ:
            return False, None

    return True, time_user


# Execute all test
TAc.print(LANG.render_feedback("start-tests", f"# Start Tests"), "green", ["bold"])
for t in range(1, ENV['num_tests'] + 1):
    for n in range(1, ENV['n_max'] + 1):
        success, time = one_test(n)
        if success:
            if ENV['goal'] == 'correct':
                TAc.print(LANG.render_feedback("success", f'# success'), "green", ["bold"])
            else:
                pass
                # if time is not efficient:
                #     TAc.print(LANG.render_feedback("not_efficient", f'# fail: Not efficient'), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback("fail", f'# fail: wrong answer'), "red", ["bold"])
            break

TAc.print(LANG.render_feedback("end", "Finish Tests"), "green", ["bold"])
exit(0)
