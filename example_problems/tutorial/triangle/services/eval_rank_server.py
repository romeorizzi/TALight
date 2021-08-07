#!/usr/bin/env python3
from sys import stderr, exit
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from piastrelle_lib import Par

# METADATA OF THIS TAL_SERVICE:
problem="piastrelle"
service="eval_rank"
args_list = [
    ('sorting_criterion',str),
    ('goal',str),
    ('seed',str),
    ('code_lang',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
MAX_N_PAIRS = 14
if ENV["code_lang"]=="compiled":
    MAX_N_PAIRS += 1
instances = list(range(MAX_N_PAIRS + 1))
if ENV["goal"] == "efficient":
    MAX_N_PAIRS = 100
    if ENV["code_lang"]=="compiled":
        MAX_N_PAIRS *= 2
    scaling_factor = 1.2
    n = instances[-1]
    while True:
        n = 1 + int(n * scaling_factor)
        if n > MAX_N_PAIRS:
            break
        instances.append(n)

p = Par(MAX_N_PAIRS)

def one_test(wff):
    n_tiles = len(wff) //2
    assert n_tiles <= MAX_N_PAIRS
    risp_correct = p.rank(wff, ENV["sorting_criterion"])
    TAc.print(f"{wff} {ENV['sorting_criterion']}", "yellow", ["bold"])
    start = monotonic()
    risp = TALinput(int, 1, TAc=TAc)
    end = monotonic()
    t = end - start # è un float, in secondi
    if risp != risp_correct:
        TAc.print(LANG.render_feedback("not-correct", f'# No. Your solution is NOT correct. The correct rank is {risp_correct}. Not {risp}.'), "red", ["bold"])                        
        exit(0)
    return t   
        
for n_tiles in instances:
    for i in range(3):
        if ENV["seed"]=='random_seed':
            seed=random.randint(100000,999999)
        else:
            seed=int(ENV["seed"])
        wff = p.rand_gen(n_tiles, seed=n_tiles*i+seed)
        time = one_test(wff)
        print(f"#Correct! [took {time} secs on your machine]")
        if time > 1:
            if n_tiles > 13:
                TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. :) Your solution correctly computes the rank of well formed tilings of a corridor of dimension 1x{n_tiles}.'), "green")
            TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to compute the rank of a well-formed tiling of a corridor of dimension 1x{n_tiles}.'), "red", ["bold"])        
            exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. :)  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. :) Your solution is efficient: its running time is polynomial in the length of the tiling it ranks.'), "green")
exit(0)
