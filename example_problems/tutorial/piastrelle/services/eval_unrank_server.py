#!/usr/bin/env python3
from sys import stderr, exit, argv
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from piastrelle_lib import Par

# METADATA OF THIS TAL_SERVICE:
problem="piastrelle"
service="eval_unrank"
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
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
MAX_N_PAIRS = 14
if ENV["code_lang"]=="compiled":
    MAX_N_PAIRS += 1
instances = list(range(2, MAX_N_PAIRS + 1))
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

def one_test(rank, n_pairs):
    assert n_pairs <= MAX_N_PAIRS
    risp_correct = p.unrank(n_pairs, rank, ENV['sorting_criterion'])
    TAc.print(f"{n_pairs} {rank} {ENV['sorting_criterion']}", "yellow", ["bold"])
    start = monotonic()
    risp = input()
    end = monotonic()
    t = end - start # è un float, in secondi
    if risp != risp_correct:
        TAc.print(LANG.render_feedback("not-correct", f'# No. Your solution is NOT correct. The wff of rank {rank} is\n {risp_correct}. Not\n {risp}.'), "red", ["bold"])                        
        exit(0)
    return t   
        
for n_pairs in instances:
    for i in range(3):
        random.seed(n_pairs*i+ENV["seed"])
        rank = random.randrange(1,p.num_sol(n_pairs)+1)
        time = one_test(rank, n_pairs)
        print(f"#Correct! [took {time} secs on your machine]")
        if time > 1:
            if n_pairs > 13:
                TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. sol:) Your solution correctly unranks well formed formulas (checked with formulas up to {n_pairs} pairs of parentheses).'), "green")
            TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to unrank a well-formed formula with {n_pairs} pairs of parentheses.'), "red", ["bold"])        
            exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. sol:)  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. sol:) Your solution is efficient: its running time is polynomial in the length of the formula it unranks.'), "green")

exit(0)
