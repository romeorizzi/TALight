#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="check_opt_num_moves"
args_list = [
    ('v',str),
    ('start', str),
    ('final', str),
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
LANG.manage_opening_msg()

# START CODING YOUR SERVICE: 

# INITIALIZATION
N = ENV['n']

# Check arguments errors
if (ENV['start'] != "all_A" and ENV['start'] != "all_B" and ENV['start'] != "all_C"):
    N = len(ENV['start'])
elif (ENV['final'] != "all_A" and ENV['final'] != "all_B" and ENV['final'] != "all_C"):
    N = len(ENV['final'])
elif (N == -1):
    LANG.manage_opening_msg()
    TAc.print(LANG.render_feedback("arg-err", f"N!=-1 if start=all_X and final=all_X"), "red", ["bold"])
    exit(0)

# Get configurations
start = get_input_from(ENV['start'], N)
final = get_input_from(ENV['final'], N)

# Check configs error
if len(start) != len(final):
    LANG.manage_opening_msg()
    TAc.print(LANG.render_feedback("arg-config-err", f'len(start) != len(final)'), "red", ["bold"])
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
            TAc.print(LANG.render_feedback("answ-equal", f'user_answ == opt_answ'), "green", ["bold"])

    else:
        TAc.print(LANG.render_feedback("answ-wrong", f'user_answ != opt_answ'), "red", ["bold"])

        # Provide feedback
        if ENV["feedback"] == "true_val":
            TAc.print(LANG.render_feedback("get-answ", f'opt_answ = {opt_answ}'), "red", ["bold"])
        
        elif ENV["feedback"] == "smaller_or_bigger":
            if user_answ < opt_answ:
                TAc.print(LANG.render_feedback("answ-less", f'user_answ < opt_answ'), "red")
            else:
                TAc.print(LANG.render_feedback("answ-more", f'user_answ > opt_answ'), "red")

        # Provide certificate
        if ENV["with_certificate"] == 1:
            if user_answ < opt_answ:
                TAc.print(LANG.render_feedback("use_check_lower_bounds", f'use check_lower_bounds service'), "red")
            else:
                TAc.print(LANG.render_feedback("certificate", f'this is a certificate of size desired {user_answ-1}:'), "red")
                for e in hanoi.getNotOptimalSol(start, final, desired_size=(user_answ-1)):
                    TAc.print(LANG.render_feedback("certificate_line", f'{e}'), "red")


else: # case: modulus
    if user_answ == mod_answ:
        if not ENV['silent']:
            TAc.print(LANG.render_feedback("answ-equal-mod", f'user_answ = mod_answ'), "green", ["bold"])

    else:
        TAc.print(LANG.render_feedback("answ-wrong-mod", f'user_answ != mod_answ'), "red", ["bold"])

        # Provide feedback
        if ENV["feedback"] == "true_val":
            TAc.print(LANG.render_feedback("get-answ-mod", f'mod_answ = {mod_answ} = {opt_answ} % {modulus}'), "red", ["bold"])
        
        elif ENV["feedback"] == "smaller_or_bigger":
            if user_answ < mod_answ:
                TAc.print(LANG.render_feedback("answ-less-mod", f'user_answ < mod_answ'), "red")
            else:
                TAc.print(LANG.render_feedback("answ-more-mod", f'user_answ > mod_answ'), "red")

        # Provide certificate
        if ENV["with_certificate"] == 1:
            if user_answ < opt_answ:
                TAc.print(LANG.render_feedback("use_check_lower_bounds", f'use check_lower_bounds service'), "red")
            else:
                TAc.print(LANG.render_feedback("certificate", f'this is the certificate:'), "red")
                for e in hanoi.getNotOptimalSol(start, final, desired_size=len(user_answ) -1):
                    TAc.print(LANG.render_feedback("certificate_line", f'{e}'), "red")


exit(0)
