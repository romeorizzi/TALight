#!/usr/bin/env python3
from sys import stderr, exit, argv
import random

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
if not ENV['silent']:
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
successes = 0
fails = 0
if ENV['start'] != 'general' and ENV['final'] != 'general':
    # in this case the test are equal, so num_tests must be 1
    num_tests = 1
for t in range(1, 2*num_tests, 2):
    for n in range(1, n_max + 1):
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
        user_sol, = TALinput(int, TAc=TAc)
        
        # check the user solution
        if modulus == 0 or not overflow: #case: not modulus or modulus irrilevant
            if user_sol == opt_sol:
                successes += 1
                TAc.print(LANG.render_feedback("success", "# success"), "green", ["bold"])
            else:
                fails += 1
                TAc.print(LANG.render_feedback("fail", "# fail"), "red", ["bold"])

        else: # case: modulus
            if user_sol == mod_sol:
                successes += 1
                TAc.print(LANG.render_feedback("success", "# success"), "green", ["bold"])
            else:
                fails += 1
                TAc.print(LANG.render_feedback("fail", "# fail"), "red", ["bold"])


# END
TAc.print(LANG.render_feedback("end", "end"), "green", ["bold"])
total = num_tests * n_max
assert total == successes + fails
TAc.print(LANG.render_feedback("stat-successes", f"# success:  {successes}/{total}"), "green", ["bold"])
TAc.print(LANG.render_feedback("stat-fails",     f"# fails:    {fails}/{total}"), "red", ["bold"])

exit(0)
