#!/usr/bin/env python3
# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="sub_closure"
args_list = [
    ('n',int), 
    ('m',int),
    ('goal',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
from random import randrange
import copy
import pirellone_lib as pl
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 


n=ENV['n'] 
m=ENV['m'] 

TAc.print("Instance: ", "yellow", ["bold"])
pirellone0=pl.random_pirellone(10, 10, solvable=True)
pl.print_pirellone(pirellone0)
pirellone=[[0 for j in range(0,m)] for i in range(0,n)]
for i in range(0,n):
    for j in range(0,m):
        pirellone[i][j]=pirellone0[i][j]

TAc.print(f"Solution of the submatrix {n}x{m} : ", "yellow", ["bold"])
solu=input()
solu=solu.split()
pl.off_lista(pirellone,solu,TAc,LANG)

    
exit(0)
