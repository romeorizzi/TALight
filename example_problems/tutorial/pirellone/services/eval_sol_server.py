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
        m=3
        n=3
    if ENV['size']=='medium':
        m=5
        n=5
    if ENV['size']=='large':
        m=8
        n=8
    pirellone,_=pl.random_pirellone(m, n, solvable=True)
    pirellone1=copy.deepcopy(pirellone)
    a=time.perf_counter() 
    sol_to_ver=ms.my_soluzione(pirellone1, m, n)
    b=time.perf_counter() 
    times.append(b-a)

TAc.print("Time: ", "yellow", ["bold"])
#print(times)
print(sum(times)/len(times))
    
    



exit(0)