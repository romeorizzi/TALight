#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_num_sol"
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
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

# risps_correct[pills_I][pills_H] = number of treatments starting with a bottle of <pills_I> integer pills and <pills_H> half pills.
risps_correct = [ [1] * (ENV['num_pills']+2) for pill_I in range(ENV['num_pills']+1)]
for pills_I in range(1,ENV['num_pills']+1):
    risps_correct[pills_I][0] = risps_correct[pills_I-1][1]
    for pills_H in range(1,ENV['num_pills']+1):
        risps_correct[pills_I][pills_H] = risps_correct[pills_I][pills_H-1] + risps_correct[pills_I-1][pills_H+1]

risp_correct = risps_correct[ENV['num_pills']][0]

overflow = False
if ENV['ok_if_congruent_modulus'] != 0:
    overflow = ( risp_correct >= ENV['ok_if_congruent_modulus'] )
    risp_correct %= ENV['ok_if_congruent_modulus'] 

if ENV['risp'] == risp_correct:
    if not ENV['silent']:
        if overflow:
            TAc.print(LANG.render_feedback("ok-equal", f"We agree. The number of possible treatments with {ENV['num_pills']} pills is congruent to {ENV['risp']} modulo {ENV['ok_if_congruent_modulus']}."), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("ok-equal", f"We agree. With {ENV['num_pills']} pills you have {ENV['risp']} possible solutions."), "green", ["bold"])
else:
    if ENV['more_or_less_hint_if_wrong']:
        if overflow:
            TAc.print(LANG.render_feedback("not-congruent", f"No. With {ENV['num_pills']} pills the number of possible solutions is NOT congruent to {ENV['risp']} modulo {ENV['ok_if_congruent_modulus']}."), "red", ["bold"])
            if ENV['ok_if_congruent_modulus'] > 0 and risp_correct == ENV['risp'] % ENV['ok_if_congruent_modulus']:
                TAc.print(LANG.render_feedback("however", f"However, let me tell you here that your risp={ENV['risp']} is actually congruent modulo {ENV['ok_if_congruent_modulus']} to the correct risp. Note that {ENV['ok_if_congruent_modulus']} is the value of the parameter 'ok_if_congruent_modulus' for the current call to the service (as you can see in the opening message). Investigate more about the parameter 'ok_if_congruent_modulus'. A description of its role and purpose can be found in the pages of the help command (and possibly also in the statement of the problem)."), "yellow", ["bold"])
        else:
            if ENV['risp'] < risp_correct:
                TAc.print(LANG.render_feedback("more", f"No. With {ENV['num_pills']} pills the possible solutions are strictly more than {ENV['risp']}. If you don't believe this, you can check it out with the service check_solutions_set."), "red", ["bold"])
                if ENV['ok_if_congruent_modulus'] != 0:
                    TAc.print(LANG.render_feedback("why_pertinent", f"And be told that the possible solutions with {ENV['num_pills']} pills are anyhow strictly less than {ENV['ok_if_congruent_modulus']} ({ENV['ok_if_congruent_modulus']} is the value of the parameter 'ok_if_congruent_modulus' for the current call to this service, as you can see in the opening message). If you don't believe this, also this can be conveniently checked out with the service check_solutions_set."), "red")
            else:
                TAc.print(LANG.render_feedback("less", f"No. With {ENV['num_pills']} pills the possible solutions are actually strictly less than {ENV['risp']}. If you don't believe this, you can check it out with the service check_solutions_set. If you don't believe this, you can check it out with the service check_solutions_set."), "red", ["bold"])
    else:
        if ENV['ok_if_congruent_modulus'] != 0:
            TAc.print(LANG.render_feedback("not-congruent", f"No. With {ENV['num_pills']} pills the number of possible solutions is NOT congruent to {ENV['risp']} modulo {ENV['ok_if_congruent_modulus']}."), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback("not-equal", f"No. With {ENV['num_pills']} pills the possible solutions are not {ENV['risp']}."), "red", ["bold"])
exit(0)
