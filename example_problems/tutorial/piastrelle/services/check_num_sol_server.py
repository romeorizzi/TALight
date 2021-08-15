#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="piastrelle"
service="check_num_sol"
args_list = [
    ('n',int),
    ('risp',int),
    ('ok_if_congruent_modulus',int),
    ('more_or_less_hint_if_wrong',bool),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
from piastrelle_lib import Par
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
p = Par(ENV["n"])
risp_correct=p.num_sol(ENV['n'])
overflow = False
if ENV['ok_if_congruent_modulus'] != 0:
    overflow = ( risp_correct >= ENV['ok_if_congruent_modulus'] )
    risp_correct %= ENV['ok_if_congruent_modulus'] 

if ENV['risp'] == risp_correct:
    if not ENV['silent']:
        if overflow:
            TAc.print(LANG.render_feedback("ok-equal", f"We agree. The number of well-formed tilings of a corridor of dimension 1x{ENV['n']} is congruent to {ENV['risp']} modulo {ENV['ok_if_congruent_modulus']}."), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("ok-equal", f"We agree. There are precisely {ENV['risp']} well-formed tilings of a corridor of dimension 1x{ENV['n']}."), "green", ["bold"])
else:
    if ENV['more_or_less_hint_if_wrong']:
        if overflow:
            TAc.print(LANG.render_feedback("not-congruent", f"No. The number of well-formed tilings of a corridor of dimension 1x{ENV['n']}is NOT congruent to {ENV['risp']} modulo {ENV['ok_if_congruent_modulus']}."), "red", ["bold"])
            if ENV['ok_if_congruent_modulus'] > 0 and risp_correct == ENV['risp'] % ENV['ok_if_congruent_modulus']:
                TAc.print(LANG.render_feedback("however", f"However, let me tell you here that your risp={ENV['risp']} is actually congruent modulo {ENV['ok_if_congruent_modulus']} to the correct risp. Note that {ENV['ok_if_congruent_modulus']} is the value of the parameter 'ok_if_congruent_modulus' for the current call to the service (as you can see in the opening message). Investigate more about the parameter 'ok_if_congruent_modulus'. A description of its role and purpose can be found in the pages of the help command (and possibly also in the statement of the problem)."), "yellow", ["bold"])
        else:
            if ENV['risp'] < risp_correct:
                TAc.print(LANG.render_feedback("more", f"No. The well-formed tilings of a corridor of dimension 1x{ENV['n']} are strictly more than {ENV['risp']}. If you don't believe this, you can check it out with the service check_sol_set."), "red", ["bold"])
                if ENV['ok_if_congruent_modulus'] != 0:
                    TAc.print(LANG.render_feedback("why_pertinent", f"And be told that the well-formed tilings of a corridor of dimension 1x{ENV['n']} are anyhow strictly less than {ENV['ok_if_congruent_modulus']} ({ENV['ok_if_congruent_modulus']} is the value of the parameter 'ok_if_congruent_modulus' for the current call to this service, as you can see in the opening message). If you don't believe this, also this can be conveniently checked out with the service check_sol_set."), "red")
            else:
                TAc.print(LANG.render_feedback("less", f"No. The well-formed tilings of a corridor of dimension 1x{ENV['n']} are actually strictly less than {ENV['risp']}. If you don't believe this, you can check it out with the service check_sol_set."), "red", ["bold"])
    else:
        if ENV['ok_if_congruent_modulus'] != 0:
            TAc.print(LANG.render_feedback("not-congruent", f"No. The number of well-formed tilings of a corridor of dimension 1x{ENV['n']} is NOT congruent to {ENV['risp']} modulo {ENV['ok_if_congruent_modulus']}."), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback("not-equal", f"No. The well-formed tilings of a corridor of dimension 1x{ENV['n']} are not {ENV['risp']}."), "red", ["bold"])

exit(0)
