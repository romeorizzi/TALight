#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="eval_sol"
args_list = [
    ('size',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
import pirellone_lib as pl
import time
import copy
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
times=[]
import my_sol as ms
for i in range(5):
    if ENV['size']=='small':
        n=3
        m=3
        pirellone=pl.random_pirellone(n, m, solvable=True)
    if ENV['size']=='medium':
        n=5
        m=5
        pirellone=pl.random_pirellone(n, m, solvable=True)
    if ENV['size']=='large':
        n=8
        m=8
        pirellone=pl.random_pirellone(n, m, solvable=True)

    pirellone1=copy.deepcopy(pirellone)
    a=time.perf_counter() 
    sol_to_ver=ms.my_soluzione(pirellone1, n, m)
    b=time.perf_counter() 
    times.append(b-a)

TAc.print("Time: ", "yellow", ["bold"])
#print(times)
print(sum(times)/len(times))
    
    



exit(0)