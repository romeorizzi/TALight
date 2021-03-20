#!/usr/bin/env python3
# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="sub_closure"
args_list = [
    ('m',int), 
    ('n',int),
    ('goal',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
import random
import copy
import pirellone_lib as pl
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 


m=ENV['m'] 
n=ENV['n'] 

TAc.print(f"Instance {m}x{n}: ", "yellow", ["bold"])
pirellone0,_=pl.random_pirellone(m, n, solvable=True)
pirellone1=copy.deepcopy(pirellone0)
pl.print_pirellone(pirellone0)
TAc.print("Solution of the instance: ", "yellow", ["bold"])
pl.stampa_lista(pl.soluzione_min(pirellone1,m,n))
sub_n=random.randint(2, n-1)
sub_m=random.randint(2, m-1)
pirellone=[[0 for j in range(0,sub_n)] for i in range(0,sub_m)]
for i in range(0,sub_m):
    for j in range(0,sub_n):
        pirellone[i][j]=pirellone0[i][j]

TAc.print(f"Solution of the submatrix {sub_n}x{sub_m} : ", "yellow", ["bold"])
solu=input()
solu=solu.split()
pl.off_lista(pirellone,solu,TAc,LANG)

    
exit(0)
