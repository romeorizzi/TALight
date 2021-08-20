#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from pills_lib import Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_num_sol"
args_list = [
    ('n_pills',int),
    ('risp',int),
    ('ok_if_congruent_modulus',int),
    ('more_or_less_hint_if_wrong',bool),
    ('silent',bool),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
p = Flask(ENV["n_pills"])
risp_correct = p.num_sol(ENV["n_pills"])
overflow = False
if ENV["ok_if_congruent_modulus"] != 0:
    overflow = ( risp_correct >= ENV["ok_if_congruent_modulus"] )
    risp_correct %= ENV["ok_if_congruent_modulus"] 

if ENV["risp"] == risp_correct:
    if not ENV["silent"]:
        TAc.OK()
        if overflow:
            TAc.print(LANG.render_feedback("ok-congruent", f'♥  We agree. The number of feasible treatments with {ENV["n_pills"]} pills is congruent to {ENV["risp"]} modulo {ENV["ok_if_congruent_modulus"]}.'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("ok-equal", f'♥  We agree. There are precisely {ENV["risp"]} feasible treatments with {ENV["n_pills"]} pills.'), "green", ["bold"])
    exit(0)

# NOW DEALING WITH WRONG ANSWER:
if ENV["ok_if_congruent_modulus"] == 0:
    TAc.print(LANG.render_feedback("not-equal", f'No. The feasible treatments with {ENV["n_pills"]} pills are not {ENV["risp"]}.'), "red", ["bold"])
else:
    TAc.print(LANG.render_feedback("not-congruent", f'No. The number of feasible treatments with {ENV["n_pills"]} pills is NOT congruent to {ENV["risp"]} modulo {ENV["ok_if_congruent_modulus"]}.'), "red", ["bold"])
    if overflow and risp_correct == ENV["risp"] % ENV["ok_if_congruent_modulus"]:
            TAc.print(LANG.render_feedback("however", f'However, I noticed that your risp={ENV["risp"]} is actually congruent modulo {ENV["ok_if_congruent_modulus"]} to the correct risp. Note that {ENV["ok_if_congruent_modulus"]} is the value of the parameter "ok_if_congruent_modulus" for the current call to the service (as you can see in the opening message). The role/use of the parameter "ok_if_congruent_modulus" is mentioned in the pages of the help or synopsis services (and possibly also in the statement of the problem).'), "yellow", ["bold"])

if ENV["more_or_less_hint_if_wrong"]:
    if ENV["ok_if_congruent_modulus"] == 0 or not overflow:
        if ENV["risp"] < risp_correct:
            TAc.print(LANG.render_feedback("more", f'Indeed, the feasible treatments with {ENV["n_pills"]} pills are strictly more than {ENV["risp"]}. If you do not believe this, you can check it out with the service check_sol_set.'), "red", ["bold"])
            if ENV["ok_if_congruent_modulus"] != 0:
                TAc.print(LANG.render_feedback("why_pertinent", f'And be told that the feasible treatments with {ENV["n_pills"]} pills are anyhow strictly less than {ENV["ok_if_congruent_modulus"]}, which is the value of the parameter "ok_if_congruent_modulus" for the current call to this service, as you can always check in the opening message.'), "red")
        else:
            TAc.print(LANG.render_feedback("less", f'Indeed, the feasible treatments with {ENV["n_pills"]} pills are actually strictly less than {ENV["risp"]}. You can check this out through the service check_sol_set.'), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback("no_pertinent", f'First, be told that the number of feasible treatments with {ENV["n_pills"]} pills overflows the value {ENV["ok_if_congruent_modulus"]} for the parameter "ok_if_congruent_modulus" as set for the current call to this service.'), "red")
        if ENV["risp"] < risp_correct:
            TAc.print(LANG.render_feedback("bigger-risp", f'This said, the correct value for the parameter risp is bigger than {ENV["risp"]}, though it would be here not proper to make assertions regarding the true number of solutions.'), "red")
        else:
            TAc.print(LANG.render_feedback("smaller-risp", f'This said, the correct value for the parameter risp is smaller than {ENV["risp"]}, though it would be here not proper to make assertions regarding the true number of solutions.'), "red")

exit(0)
