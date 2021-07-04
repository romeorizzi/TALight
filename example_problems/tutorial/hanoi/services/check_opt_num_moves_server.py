#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="check_opt_num_moves"
args_list = [
    ('start', str),
    ('final', str),
    ('n',int),
    ('sol',int),
    ('ok_if_congruent_modulus',int),
    ('v',str),
    ('feedback',str),
    ('with_certificate',bool),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")


# INITIALIZATION
# Check arguments errors
if ENV['version'] == 'classic' and (\
    ENV['start'] != 'all_A' or \
    ENV['start'] != 'all_B' or \
    ENV['start'] != 'all_C' ):
    TAc.print(LANG.render_feedback("arg-classic-start-err", f"classic version wants start=all_A/B/C"), "red", ["bold"])
    exit(0)
if ENV['version'] == 'classic' and (\
    ENV['final'] != 'all_A' or \
    ENV['final'] != 'all_B' or \
    ENV['final'] != 'all_C' ):
    TAc.print(LANG.render_feedback("arg-classic-final-err", f"classic version wants final=all_A/B/C"), "red", ["bold"])
    exit(0)

# Get Start config
start = get_input_from(ENV['start'], ENV['n'])
if start == "err":
    TAc.print(LANG.render_feedback("arg-all-err", f"Wrong n for start_config"), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("print_start", f'Start config: {start}'), "yellow", ["bold"])

# Get Final config
final = get_input_from(ENV['final'], ENV['n'])
if final == "err":
    TAc.print(LANG.render_feedback("arg-all-err", f"Wrong n for final_config"), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("print_start", f'Final config: {final}'), "yellow", ["bold"])

# Check configs error
if len(start) != len(final):
    TAc.print(LANG.render_feedback("arg-config-err", f"len(start) != len(final)"), "red", ["bold"])
    exit(0)

# Init Hanoi Tower
hanoi = HanoiTowerProblem(ENV['v'])

# Get the correct solution
modulus = ENV['ok_if_congruent_modulus']
user_sol = ENV['sol']
corr_sol = hanoi.get_min_moves(start, final)
if modulus != 0:
    overflow = (corr_sol >= modulus)
    mod_sol = corr_sol % modulus

# check the user solution
if modulus == 0 or not overflow: #case: not modulus or modulus irrilevant
    if user_sol == corr_sol:
        TAc.print(LANG.render_feedback("sol-equal", f'user_sol == corr_sol'), "green", ["bold"])

    else:
        TAc.print(LANG.render_feedback("sol-wrong", f'user_sol != corr_sol'), "red", ["bold"])

        # Provide feedback
        if ENV["feedback"] == "true_val":
            TAc.print(LANG.render_feedback("get-sol", f'corr_sol = {corr_sol}'), "red", ["bold"])
        
        elif ENV["feedback"] == "smaller_or_bigger":
            if user_sol < corr_sol:
                TAc.print(LANG.render_feedback("sol-less", f'user_sol < corr_sol'), "red")
            else:
                TAc.print(LANG.render_feedback("sol-more", f'user_sol > corr_sol'), "red")

        # Provide certificate
        if ENV["with_certificate"] == 1:
            if user_sol < corr_sol:
                TAc.print(LANG.render_feedback("use_check_lower_bounds", f'use check_lower_bounds service'), "red")
            else:
                TAc.print(LANG.render_feedback("certificate", f'this is the certificate:'), "red")
                for e in hanoi.get_not_opt_sol(start, final, size=(user_sol-1)):
                    TAc.print(LANG.render_feedback("certificate_line", f'{e}'), "red")


else: # case: modulus
    if user_sol == mod_sol:
        TAc.print(LANG.render_feedback("sol-equal-mod", f'user_sol = mod_sol'), "green", ["bold"])

    else:
        TAc.print(LANG.render_feedback("sol-wrong-mod", f'user_sol != mod_sol'), "red", ["bold"])

        # Provide feedback
        if ENV["feedback"] == "true_val":
            TAc.print(LANG.render_feedback("get-sol-mod", f'mod_sol = {mod_sol} = {corr_sol} % {modulus}'), "red", ["bold"])
        
        elif ENV["feedback"] == "smaller_or_bigger":
            if user_sol < mod_sol:
                TAc.print(LANG.render_feedback("sol-less-mod", f'user_sol < mod_sol'), "red")
            else:
                TAc.print(LANG.render_feedback("sol-more-mod", f'user_sol > mod_sol'), "red")

        # Provide certificate
        if ENV["with_certificate"] == 1:
            if user_sol < corr_sol:
                TAc.print(LANG.render_feedback("use_check_lower_bounds", f'use check_lower_bounds service'), "red")
            else:
                TAc.print(LANG.render_feedback("certificate", f'this is the certificate:'), "red")
                for e in hanoi.get_not_opt_sol(start, final, size=len(user_sol) -1):
                    TAc.print(LANG.render_feedback("certificate_line", f'{e}'), "red")


exit(0)
