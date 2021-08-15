#!/usr/bin/env python3
from sys import stderr, exit
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from parentheses_lib import Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="gen_random_sol"
args_list = [
    ('n_pairs',int),
    ('seed',str),
    ('verbose',int),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if ENV["verbose"] == 3:
    LANG.print_opening_msg()

if ENV["seed"]=='random_seed':
    seed=random.randint(100000,999999)
    if ENV["verbose"] >= 1:
        TAc.print(seed, "yellow")
else:
    seed=int(ENV["seed"])
    if ENV["verbose"] >= 2:
        TAc.print(seed, "yellow")
p=Par(ENV["n_pairs"])
wff = p.rand_gen(ENV["n_pairs"], seed=seed)
print(wff)    
exit(0)
