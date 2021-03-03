#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_risp"
args_list = [
    ('num_pills',int),
    ('risp',int),
    ('ok_if_congruent_modulus',int),
    ('more_or_less_hint_if_wrong',bool),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

risps_correct = [ [1] * (ENV['num_pills']+2) for pill_I in range(ENV['num_pills']+1)]
for pills_I in range(1,ENV['num_pills']+1):
    risps_correct[pills_I][0] = risps_correct[pills_I-1][1]
    for pills_H in range(1,ENV['num_pills']+1):
        risps_correct[pills_I][pills_H] = risps_correct[pills_I][pills_H-1] + risps_correct[pills_I-1][pills_H+1]

risp_correct = risps_correct[ENV['num_pills']][0]

if ENV['ok_if_congruent_modulus'] == 0:
    if ENV['risp'] == risp_correct:
        if not ENV['silent']:
            TAc.print(LANG.render_feedback("ok-equal", f"We agree. With {ENV['num_pills']} pills you have {ENV['risp']} possible solutions."), "green", ["bold"])
    else:
        if ENV['more_or_less_hint_if_wrong']:
            if ENV['risp'] < risp_correct:
                TAc.print(LANG.render_feedback("more", f"No. With {ENV['num_pills']} pills the possible solutions are strictly more than {ENV['risp']}. If you don't believe this, you can check it out with the service check_solutions_set."), "red", ["bold"])
            else:
                TAc.print(LANG.render_feedback("less", f"No. With {ENV['num_pills']} pills the possible solutions are less than {ENV['risp']}. If you don't believe this, you can check it out with the service check_solutions_set."), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback("not-equal", f"No. With {ENV['num_pills']} pills the possible solutions are not {ENV['risp']}."), "red", ["bold"])
else:
    risp_correct %= ENV['ok_if_congruent_modulus'] 
    if ENV['risp'] == risp_correct:
        if not ENV['silent']:
            TAc.print(LANG.render_feedback("ok-congruent", f"We agree. With {ENV['num_pills']} pills the number of possible solutions is congruent to {ENV['risp']} modulo {ENV['ok_if_congruent_modulus']}."), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("not-congruent", f"No. With {ENV['num_pills']} pills the number of possible solutions is NOT congruent to {ENV['risp']} modulo {ENV['ok_if_congruent_modulus']}."), "red", ["bold"])
exit(0)
