#!/usr/bin/env python3

from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl
from utils_lang import process_inputs

# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="check_your_sol"
args_list = [
    ('input_mode',str),
    ('m',int), 
    ('n',int),
    ('seed',str),
    ('coding',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get pirellone and solution
(instance, opt_sol) = process_inputs(ENV, TAc, LANG)
TAc.print(LANG.render_feedback("spoiler", f"{opt_sol}"), "green", ["bold"])

# Get and check solution
user_sol = list()
TAc.print(LANG.render_feedback("usersol-title", "Your solution: "), "yellow", ["reverse"])
if ENV['coding'] == 'seq':
    # Get user solution
    user_sol = TALinput(str, regex="^|[a-zA-Z][0-9]+$", sep=' ', TAc=TAc)
    if user_sol == ['']:    # To manage the case 'zero moves'
        user_sol.clear()
elif ENV['coding'] == 'subset':
    (user_sol_str,) = TALinput(str, regex=f"^(0|1){{{ENV['m']}}},(0|1){{{ENV['n']}}}$", sep=' ', TAc=TAc)
    user_sol_tmp = user_sol_str.split(',') #split into ['0000','1111']
    user_sol.append([int(e) for e in list(user_sol_tmp[0])]) #get: [0,0,0,0]
    user_sol.append([int(e) for e in list(user_sol_tmp[1])]) #get: [1,1,1,1]
    # ALTERNATIVE:
    # TAc.print(LANG.render_feedback("usersol-rows-title", "Rows:"), "yellow", ["reverse"])
    # user_sol.append(TALinput(int, num_tokens=ENV['m'], regex="^(0|1)+$", sep=' ', TAc=TAc))
    # TAc.print(LANG.render_feedback("usersol-rows-title", "Columns:"), "yellow", ["reverse"])
    # user_sol.append(TALinput(int, num_tokens=ENV['n'], regex="^(0|1)+$", sep=' ', TAc=TAc))

# Check the correctness of the user solution
if (user_sol == opt_sol):
    TAc.OK()
    TAc.print(LANG.render_feedback('correct', "This sequence turns off all lights."), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback('not-correct', "This sequence doesn't turn off all lights see what happens using your solution"), "red", ["bold"])

exit(0)
