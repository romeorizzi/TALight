#!/usr/bin/env python3
from sys import stderr, exit, argv
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from parentheses_lib import Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
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
MAX_N_PAIRS = 10000
instances = list(range(MAX_N_PAIRS + 1))
if ENV['goal'] == "correct":
    MAX_N_PAIRS = 14
else:
    if ENV['answ_modulus'] == 0:
        MAX_N_PAIRS = 100
    instances = list(range(MAX_N_PAIRS + 1))
    scaling_factor = 1.5
    n = 10
    while True:
        n = 1 + int(n * scaling_factor)
        if n > MAX_N_PAIRS:
            break
        instances.append(n)

p = Par(MAX_N_PAIRS)

def one_test(n_pairs):
    assert n_pairs <= MAX_N_PAIRS:
    risp_correct = p.num_sol()
    TAc.print(n_pairs), "yellow", ["bold"])
    start = monotonic()
    risp = int(input())
    end = monotonic()
    t = end - start # è un float, in secondi
    if ENV['answ_modulus'] == 0:
        if risp != risp_correct:
        TAc.print(LANG.render_feedback("not-correct", f"No. You solution is not correct. The number of well-formed formulas with {n_pairs} pairs of parentheses is {risp_correct}. Not {risp}."), "red", ["bold"])                        
        exit(0)
    elif risp % ENV['answ_modulus'] != risp_correct % ENV['answ_modulus']:
        TAc.print(LANG.render_feedback("not-correct", f"No. You solution is not correct. The number of well-formed formulas with {n_pairs} pairs of parentheses is {risp_correct}. Taken modulus {ENV['answ_modulus']} this value boils down to {risp_correct % ENV['answ_modulus']}. Not {risp}."), "red", ["bold"])                
        exit(0)
    if t > 1:
        if n_pairs > 14:
            TAc.print(LANG.render_feedback("seems-correct", f"Ok. Your solution appears to correctly compute the number of well formed formulas (checked it up to {n_pairs} pairs of parentheses)."), "green")
        TAc.print(LANG.render_feedback("not-efficient", f"No. You solution is not efficient. When run on your machine, it took more than one second to compute the number of well-formed formulas with {n_pairs} pairs of parentheses."), "red", ["bold"])        
        exit(0)
        

for inst in instances:
   one_test(inst)   

exit(0)
