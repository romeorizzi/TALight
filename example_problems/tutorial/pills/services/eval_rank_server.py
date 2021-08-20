#!/usr/bin/env python3
from sys import stderr, exit
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from pills_lib import Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="eval_rank"
args_list = [
    ('sorting_criterion',str),
    ('goal',str),
    ('seed',int),
    ('code_lang',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
MAX_N = 14
if ENV["code_lang"]=="compiled":
    MAX_N += 1
instances = list(range(MAX_N + 1))
if ENV["goal"] == "efficient":
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

p = Flask(MAX_N)

def one_test(treatment):
    n_pills = len(treatment) //2
    assert n_pills <= MAX_N
    risp_correct = p.rank(treatment, ENV["sorting_criterion"])
    TAc.print(treatment, "yellow", ["bold"])
    start = monotonic()
    risp = TALinput(int, 1, TAc=TAc)[0]
    end = monotonic()
    t = end - start # è un float, in secondi
    if risp != risp_correct:
        TAc.print(LANG.render_feedback("not-correct", f'# No. Your solution is NOT correct. The correct rank is {risp_correct}. Not {risp}.'), "red", ["bold"])                        
        exit(0)
    return t   
        
for n_pills in instances:
    for i in range(3):
        treatment = p.rand_gen(n_pills, seed=n_pills*i+ENV["seed"])
        time = one_test(treatment)
        print(f"#Correct! [took {time} secs on your machine]")
        if time > 1:
            if n_pills > 13:
                TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥ Your solution correctly computes the rank of feasible treatments (checked with treatments up to {n_pills} pills).'), "green")
            TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to compute the rank of a feasible treatments with {n_pills} pills.'), "red", ["bold"])        
            exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is polynomial in the length of the treatment it ranks.'), "green")

exit(0)
