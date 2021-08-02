#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="check_opt_num_moves"
args_list = [
    ('v',str),
    ('start',str),
    ('final',str),
    ('n',int),
    ('answ',int),
    ('ok_if_congruent_modulus',int),
    ('silent',bool),
    ('feedback',str),
    ('with_certificate',bool),
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

# Get the correct answer
modulus = ENV['ok_if_congruent_modulus']
user_answ = ENV['answ']
opt_answ = hanoi.getMinMoves(start, final)
if modulus != 0:
    overflow = (opt_answ >= modulus)
    mod_answ = opt_answ % modulus

# check the user answer
if modulus == 0 or not overflow: #case: not modulus or modulus irrilevant
    if user_answ == opt_answ:
        if not ENV['silent']:
            TAc.print(LANG.render_feedback("answ-equal", f'Nice! Your answer is equal to the optimal minimum number.'), "green", ["bold"])

    else:
        TAc.print(LANG.render_feedback("answ-wrong", f'Oh no! Your answer is not equal to the optimal minimum number.'), "red", ["bold"])

        # Provide feedback
        if ENV["feedback"] == "true_val":
            TAc.print(LANG.render_feedback("get-answ", f'The optimal minimum number of moves is {opt_answ}.'), "red", ["reverse"])
        
        elif ENV["feedback"] == "smaller_or_bigger":
            if opt_answ < user_answ:
                TAc.print(LANG.render_feedback("answ-less", f'The optimal minimum number of moves is smaller then your answer.'), "red", ["reverse"])
            else:
                TAc.print(LANG.render_feedback("answ-more", f'The optimal minimum number of moves is bigger then your answer.'), "red", ["reverse"])

        # Provide certificate
        if ENV["with_certificate"] == 1:
            if user_answ < opt_answ:
                TAc.print(LANG.render_feedback("use-check_lower_bounds", f'Use check_lower_bounds service for check it.'), "red", ["reverse"])
            else:
                TAc.print(LANG.render_feedback("certificate", f'This is a certificate of a solution with less moves:'), "red", ["reverse"])
                for e in hanoi.getNotOptimalMovesList(start, final, desired_size=(user_answ-1)):
                    disk, current, target = hanoi.parseMove(e)
                    TAc.print(LANG.render_feedback("certificate-line", f'Move disk {disk} from {current} peg to {target} peg.'), "yellow", ["reverse"])


else: # case: modulus
    if user_answ == mod_answ:
        if not ENV['silent']:
            TAc.print(LANG.render_feedback("answ-equal-mod", f'Oh no! Your answer is equal to the optimal minimum number in modulo={modulus}.'), "red", ["bold"])

    else:
        TAc.print(LANG.render_feedback("answ-wrong-mod", f'Oh no! Your answer is not equal to the optimal minimum number in modulo={modulus}.'), "red", ["reverse"])

        # Provide feedback
        if ENV["feedback"] == "true_val":
            TAc.print(LANG.render_feedback("get-answ-mode", f'The optimal minimum number in modulo={modulus} of moves is {mod_answ} = {opt_answ} % {modulus}.'), "red", ["reverse"])
        
        elif ENV["feedback"] == "smaller_or_bigger":
            if mod_answ < user_answ:
                TAc.print(LANG.render_feedback("answ-less-mod", f'The optimal minimum number in modulo={modulus} of moves is smaller then your answer.'), "red", ["reverse"])
            else:
                TAc.print(LANG.render_feedback("answ-more-mod", f'The optimal minimum number in modulo={modulus} of moves is bigger then your answer.'), "red", ["reverse"])

        # Provide certificate
        if ENV["with_certificate"] == 1:
            if user_answ < opt_answ:
                TAc.print(LANG.render_feedback("use-check_lower_bounds", f'Use check_lower_bounds service for check it.'), "red", ["reverse"])
            else:
                TAc.print(LANG.render_feedback("certificate", f'This is a certificate of a solution with less moves:'), "red", ["reverse"])
                for e in hanoi.getNotOptimalMovesList(start, final, desired_size=len(user_answ) -1):
                    disk, current, target = hanoi.parseMove(e)
                    TAc.print(LANG.render_feedback("certificate-line", f'Move disk {disk} from {current} peg to {target} peg.'), "yellow", ["reverse"])


exit(0)
