#!/usr/bin/env python3
from sys import stderr, exit
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator, HanoiTowerProblem, generate_n_list


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="eval_opt_num_moves"
args_list = [
    ('v',str),
    ('start', str),
    ('final', str),
    ('ok_if_congruent_modulus',int),
    ('goal',str),
    ('seed',str),
    ('code_lang',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))



# START CODING YOUR SERVICE:
# get seed
seed = ENV['seed']
if seed == 'random_seed':
    seed = random.randint(100000, 999999)
else:
    seed = int(seed)
TAc.print(LANG.render_feedback("print-service-seed", f"# service seed = {seed}"), "yellow", ["bold"])


# Init Hanoi Tower and configGenerator
hanoi = HanoiTowerProblem(ENV['v'])
gen = ConfigGenerator(seed)


# Functions
def one_test(start, final):
    # Get the correct solution
    modulus = ENV['ok_if_congruent_modulus']
    opt_answ = hanoi.getMinMoves(start, final, True)
    if modulus != 0:
        overflow = (opt_answ >= modulus)
        mod_answ = opt_answ % modulus

    # Get user answer
    t_start = monotonic()
    user_answ, = TALinput(int, TAc=TAc, comment_lines_start_with='T:')
    t_end = monotonic()
    time = t_end - t_start # seconds in float


    # FOR DEBUGGING --------------------------------------------
    # time_user, = TALinput(str, TAc=TAc)
    # time_user = float(time_user[2:])
    # time = time_user
    # ----------------------------------------------------------

    
    # check the user answer
    if modulus == 0 or not overflow: #case: not modulus or modulus irrilevant
        if user_answ != opt_answ:
            return False, None
    else: # case: modulus
        if user_answ != mod_answ:
            return False, None

    return True, time


# Generate test list
if ENV['goal'] == 'efficient':
    n_list = generate_n_list(n_max=50, scaling_factor=1.2)
else:
    n_list = generate_n_list(n_max=14, scaling_factor=1.2)
    if ENV['v'] != 'clockwise':
        n_list += [n_list[-1] + 1]
    if ENV["code_lang"]=="compiled":
        n_list += [n_list[-1] + 1]


# Execute all test
TAc.print(LANG.render_feedback("start-tests", f"# Start Tests"), "green", ["bold"])
TAc.print(LANG.render_feedback("print-version", f"# version={ENV['v']}"), "green", ["bold"])
times = list()
for n in n_list:
    # get type of configurations
    start, final, error = gen.getConfigs(ENV['start'], ENV['final'], n)
    assert error == None
    TAc.print(LANG.render_feedback("print-n", f"# Test with n={n}"), "green", ["bold"])
    TAc.print(LANG.render_feedback("print-configs", f"{start}\n{final}"), "green", ["bold"])

    # run instance
    success, time = one_test(start, final)
    times.append(time)
    TAc.print(LANG.render_feedback("time", f'# time={time} (sec)'), "green", ["bold"])
    if success:
        if ENV['goal'] == 'correct':
            TAc.print(LANG.render_feedback("success", f'# success'), "green", ["bold"])
        else:
            if ((ENV['v'] == 'classic'   and time > 0.0400) or \
                (ENV['v'] == 'toddler'   and time > 0.0400) or \
                (ENV['v'] == 'clockwise' and time > 0.8000) ):
                TAc.print(LANG.render_feedback("fail", f'# fail: too slow'), "red", ["bold"])
                break
            else:
                TAc.print(LANG.render_feedback("success", f'# success'), "green", ["bold"])

    else:
        TAc.print(LANG.render_feedback("fail", f'# fail: wrong answer'), "red", ["bold"])
        TAc.print(LANG.render_feedback("print-service-seed", f"# service seed: {seed}"), "red", ["bold"])
        TAc.print(LANG.render_feedback("print-configs", f"{start}\n{final}"), "green", ["bold"])
        break

TAc.print(LANG.render_feedback("end", "Finish Tests"), "green", ["bold"])


# FOR DEBUGGING --------------------------------------------
# try:
#     with open('utils/data/mode.txt', 'r') as mode_file:
#         mode = mode_file.read()
# except FileNotFoundError:
#     with open('utils/data/mode.txt', 'w') as mode_file:
#         mode_file.write('0')
#         mode = '0'

# v = ENV['v']
# if mode == '0':
#     with open(f'utils/data/{v}_n.txt', 'w') as file:
#         file.write(f'{n_list}\n')
#     with open(f'utils/data/{v}_correct.txt', 'w') as file:
#         file.write(f'{times}')
#     with open('utils/data/mode.txt', 'w') as mode_file:
#         mode_file.write('1')
# else:
#     with open(f'utils/data/{v}_efficient.txt', 'w') as file:
#         file.write(f'{times}')
#     with open('utils/data/mode.txt', 'w') as mode_file:
#         mode_file.write('0')
# ----------------------------------------------------------

exit(0)
