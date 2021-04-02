#!/usr/bin/env python3
from sys import stderr, exit, argv
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from pills_lib import Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="eval_num_sol_server"
args_list = [
    ('answ_modulus',int),
    ('goal',str),
    ('code_lang',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
MAX_N = 14
if ENV["code_lang"]=="compiled":
    MAX_N += 1
instances = list(range(MAX_N + 1))
if ENV["goal"] == "efficient":
    MAX_N = 1000
    if ENV["answ_modulus"] == 0:
        MAX_N = 100
    if ENV["code_lang"]=="compiled":
        MAX_N *= 2
    scaling_factor = 1.2
    n = instances[-1]
    while True:
        n = 1 + int(n * scaling_factor)
        if n > MAX_N:
            break
        instances.append(n)

p = Flask(MAX_N, nums_mod=ENV["answ_modulus"])

def one_test(n_pills):
    assert n_pills <= MAX_N
    risp_correct = p.num_sol(n_pills)
    TAc.print(n_pills, "yellow", ["bold"])
    start = monotonic()
    risp = int(input())
    end = monotonic()
    t = end - start # è un float, in secondi
    if ENV["answ_modulus"] == 0:
        if risp != risp_correct:
            TAc.print(LANG.render_feedback("not-equal", f'# No. You solution is NOT correct. The number of feasible treatments with {n_pills} pills is:\n {risp_correct}. Not {risp}.'), "red", ["bold"])                        
            exit(0)
    elif (risp % ENV["answ_modulus"]) != (risp_correct % ENV["answ_modulus"]):
        TAc.print(LANG.render_feedback("not-equiv", f'No. You solution is not correct. The number of feasible treatments with {n_pills} pills is {risp_correct}. Taken modulus {ENV["answ_modulus"]} this value boils down to {risp_correct % ENV["answ_modulus"]}. Not {risp}.'), "red", ["bold"])                
        exit(0)
    return t   
        
for n_pills in instances:
   time = one_test(n_pills)
   print(f"#Correct! [took {time} secs on your machine]")
   if time > 1:
       if n_pills > 13:
           TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥  Your solution correctly computes the number of feasible treatments up to {n_pills} pills.'), "green")
       TAc.print(LANG.render_feedback("not-efficient", f'# No. Your solution is not efficient. Run on your machine, it took more than one second to compute the number of feasible treatments with {n_pills} pills.'), "red", ["bold"])        
       exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥  Your solution is efficient: its running time is logarithmic in the number of treatments it counts.'), "green")

exit(0)
