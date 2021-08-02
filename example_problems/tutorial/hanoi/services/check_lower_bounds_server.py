#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="check_lower_bound"
args_list = [
    ('v',str),
    ('start', str),
    ('final', str),
    ('n',int),
    ('disk',int),
    ('answ',int),
    ('silent',bool),
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
# LANG.manage_opening_msg()



# START CODING YOUR SERVICE: 
# Get configurations
gen = ConfigGenerator()
start, final, error = gen.getConfigs(ENV['start'], ENV['final'], ENV['n'])

# Check errors
if error == 'n_not_valid':
    TAc.print(LANG.render_feedback("n_not_valid", f"If you use the all_* form for start and final, you must use a N >= 0."), "red", ["bold"])
    exit(0)
elif error == 'different_len':
    TAc.print(LANG.render_feedback("different_len", f'If you use a custom configuration for start and final, the length of start must be equal to the length of final'), "red", ["bold"])
    exit(0)


# Init Hanoi Tower
hanoi = HanoiTowerProblem(ENV['v'])

# Get the correct solution
disk = ENV['disk']
user_answ = ENV['answ']
opt_answ = hanoi.getMinMovesOf(start, final, disk)


# check the user solution
if user_answ == opt_answ:
    if not ENV['silent']:
        TAc.print(LANG.render_feedback("answ-equal", f'Nice! Your answer is correct.'), "green", ["bold"])

else:
    TAc.print(LANG.render_feedback("answ-wrong", f'Oh no! Your answer is wrong.'), "red", ["bold"])

    # Provide feedback
    if ENV["feedback"] == "true_val":
        TAc.print(LANG.render_feedback("get-answ", f'The lower bound for the disk={disk} is {opt_answ}.'), "red", ["reverse"])
    
    elif ENV["feedback"] == "smaller_or_bigger":
        if opt_answ < user_answ:
            TAc.print(LANG.render_feedback("answ-less", f'The correct lower bound for the disk={disk} is smaller then your answer.'), "red", ["reverse"])
        else:
            TAc.print(LANG.render_feedback("answ-more", f'The correct lower bound for the disk={disk} is bigger then your answer.'), "red", ["reverse"])

exit(0)
