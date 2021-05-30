#!/usr/bin/env python3
from sys import stderr, exit, argv
import random

from multilanguage import Env, Lang, TALcolors

import pirellone_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="order_of_rows_columns"
args_list = [
    ('m',int), 
    ('n',int),
    ('seed',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
m=ENV['m'] 
n=ENV['n'] 

if ENV['seed']=='random_seed': 
    pirellone,seed,sr,sc=pl.random_pirellone(m, n, solvable=True,s=True)
else:
    pirellone,seed,sr,sc=pl.random_pirellone(m, n,ENV['seed'], solvable=True,s=True)
TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
pl.print_pirellone(pirellone)
TAc.print(LANG.render_feedback("sol","Solution: "), "yellow", ["bold"])
shortsol=pl.solution_min(sr,sc)
print(" ".join(shortsol))
random.seed(seed)
r=[]
c=[]
for i in range(0,m):
    r.append(f"{i+1}")
for i in range(0,n):
    c.append(f"{i+1}")  
random.shuffle(r)
random.shuffle(c)
TAc.print(LANG.render_feedback("rows","Permutation of rows: "), "yellow", ["bold"])
print(" ".join(r))
TAc.print(LANG.render_feedback("col","Permutation of columns: "), "yellow", ["bold"])
print(" ".join(c))

pc_pirellone=[[0 for j in range(0,n) ] for i in range(0,m)] 
p_pirellone=[[0 for j in range(0,n) ] for i in range(0,m)] 
for j in range(0,n):
    for i in range(0,m):
        pc_pirellone[i][j]=pirellone[i][int(c[j])-1]
for i in range(0,m):
        p_pirellone[i]=pc_pirellone[int(r[i])-1]

TAc.print("Solution of permuted matrix: ", "yellow", ["bold"])
solu=input()
solu=solu.split()

risultato,_=pl.check_off_lights(p_pirellone,solu)
if risultato :
    TAc.OK()
    TAc.print(LANG.render_feedback("shoter","Correct solution."), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("same-on","Some lights are on!"), "red", ["bold"])

    
exit(0)
