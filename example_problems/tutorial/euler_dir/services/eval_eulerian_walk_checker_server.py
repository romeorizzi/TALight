#!/usr/bin/env python3

from sys import stderr, exit, argv

import collections
import random
from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="euler_dir"
service="eval_eulerian_walk_checker"
args_list = [
    ('goal',str),
    ('code_lang',str),
    ('lang',str),
    ('seed',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

seed = ENV['seed']

x = random.randint(1, 4)

graph,circuit,error,a = certificateEvalWalk (x, seed)
TAc.print(f"\nSeed dell'istanza: {a}\n", "yellow")

print(graph)
print("\n")
print(circuit)

start = monotonic()
answer = input().lower()
end = monotonic()
time1 = end - start

if answer != "y" and answer != "n":
    TAc.print("\nStabilisci se si tratta di eulerian walk e rispondi solo con y o n !", "red")
    exit(0)

if ENV['goal'] == "correct":
    if answer == error:
        TAc.print("\nCORRETTO!", "green")
        exit(0)
    else:
        TAc.print("\nSBAGLIATO!", "red")
    exit(0)

if ENV['goal'] == 'efficient':
    if answer == error:
        if time1 <= 1:
            TAc.print(f"\nCORRETTO!\nCi sono voluti {time1} secs sulla tua macchina!\n","yellow")
        else:
            TAc.print("\nCORRETTO! \nMa il tuo algoritmo non è molto efficiente, ci mette più di un secondo\n","red")
    else:
        TAc.print("\nSBAGLIATO!", "red")
    exit(0)