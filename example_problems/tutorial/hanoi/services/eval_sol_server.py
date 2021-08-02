#!/usr/bin/env python3
from sys import stderr, exit, argv
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator, HanoiTowerProblem
from utils_lang import get_regex, get_std_move


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="eval_sol"
args_list = [
    ('v',str),
    ('start', str),
    ('final', str),
    ('format', str),
    ('seed',int),
    ('num_tests',int),
    ('n_max',int),
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

# Init Hanoi Tower
hanoi = HanoiTowerProblem(ENV['v'])
gen = ConfigGenerator(seed)

    
# Execute all test
TAc.print(LANG.render_feedback("start-tests", f"# Start Tests"), "green", ["bold"])
for t in range(1, ENV['num_tests'] + 1):
    for n in range(1, ENV['n_max'] + 1):
        # RUN TEST --------------------
        # get type of configurations
        start, final, error = gen.getConfigs(ENV['start'], ENV['final'], n)
        assert error == None
        TAc.print(LANG.render_feedback("print-configs", f"{start}\n{final}"), "green", ["bold"])
        
        # Get the correct solution
        opt_sol = hanoi.getMovesList(start, final)

        # Get user solution
        user_sol = list()
        regex, explain = get_regex(ENV['format'], ENV['lang'])
        while True:
            user_move, = TALinput(str, sep="\n", regex=regex, regex_explained=explain, exceptions={"end"}, TAc=TAc)
            if user_move == 'end':
                break
            user_sol.append(get_std_move(user_move, ENV['format'], ENV['lang']))


        # CHECK TEST ------------------
        if user_sol == opt_sol:
            TAc.print(LANG.render_feedback("success", "# success"), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("fail", "# fail"), "red", ["bold"])
            break

TAc.print(LANG.render_feedback("end", "Finish Tests"), "green", ["bold"])
exit(0)
