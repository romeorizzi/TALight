#!/usr/bin/env python3
from sys import stderr, exit, argv
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from parentheses_lib import Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="eval_next"
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

def one_test(wff):
    n_pairs = len(wff) //2
    assert n_pairs <= MAX_N_PAIRS
    risp_correct = p.next(wff, ENV["sorting_criterion"])
    TAc.print(wff, "yellow", ["bold"])
    start = monotonic()
    risp = input()
    end = monotonic()
    t = end - start # è un float, in secondi
    if risp != risp_correct:
        TAc.print(LANG.render_feedback("not-correct", f"No. Your solution is not correct. The next wff is\n {risp_correct}. Not\n {risp}."), "red", ["bold"])                        
        exit(0)
    return t   
        
for n_pairs in instances:
    if ENV["sorting_criterion"] == "loves_opening_par":
        first = '('*n_pairs + ')'*n_pairs
        last = '()'*n_pairs
    else:
        first = '()'*n_pairs
        last = '('*n_pairs + ')'*n_pairs
    for i in range(3):
        wff = p.rand_gen(n_pairs, seed=n_pairs*i+ENV["seed"])
        if wff == last:
            wff = first
        time = one_test(wff)
        print(f"#Correct! [took {time} secs on your machine]")
        if time > 1:
            if n_pairs > 13:
                TAc.print(LANG.render_feedback("seems-correct", f'# Ok. ♥ Your solution appears to correctly compute the well formed formula which immidiately follows a given well formed formula (checked it up to {n_pairs} pairs of parentheses).'), "green")
            TAc.print(LANG.render_feedback("not-efficient", f'No. You solution is not efficient. When run on your machine, it took more than one second to compute the next well-formed formula of this last wff with {n_pairs} pairs of parentheses.'), "red", ["bold"])        
            exit(0)

TAc.print(LANG.render_feedback("seems-correct", f'# Ok. ♥ Your solution appears to correctly compute the well formed formula which immidiately follows a given well formed formula (checked it on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is polynomial in the length of the formulas it manipulates.'), "green")

exit(0)
