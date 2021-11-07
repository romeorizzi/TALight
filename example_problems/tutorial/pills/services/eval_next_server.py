#!/usr/bin/env python3
from sys import stderr, exit
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from pills_lib import Flask

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('sorting_criterion',str),
    ('goal',str),
    ('code_lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
MAX_N = 14
if ENV["code_lang"]=="compiled":
    MAX_N += 1
instances = list(range(2, MAX_N + 1))
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
    risp_correct = p.next(treatment, ENV["sorting_criterion"])
    TAc.print(treatment, "yellow", ["bold"])
    start = monotonic()
    risp = input()
    end = monotonic()
    t = end - start # è un float, in secondi
    if risp != risp_correct:
        TAc.print(LANG.render_feedback("not-correct", f'# No. Your solution is NOT correct. The next treatment is\n {risp_correct}. Not\n {risp}.'), "red", ["bold"])                        
        exit(0)
    return t   
        
for n_pills in instances:
    if ENV["sorting_criterion"] == "lovesI":
        first = '('*n_pills + ')'*n_pills
        last = '()'*n_pills
    else:
        first = '()'*n_pills
        last = '('*n_pills + ')'*n_pills
    for i in range(3):
        treatment = p.rand_gen(n_pills, seed=n_pills*i+ENV["seed"])
        if treatment == last:
            treatment = first
        time = one_test(treatment)
        print(f"#Correct! [took {time} secs on your machine]")
        if time > 1:
            if n_pills > 13:
                TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥ Your solution correctly computes the feasible treatment immidiately following a given one (checked with treatments up to {n_pills} pills).'), "green")
            TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to compute the next feasible treatment of this last treatment with {n_pills} pills.'), "red", ["bold"])        
            exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is polynomial in the length of the treatments it manipulates.'), "green")

exit(0)
