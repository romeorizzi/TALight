#!/usr/bin/env python3
# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="sub_closure"
args_list = [
    ('m',int), 
    ('n',int),
    ('goal',str),
    ('submatrix_type',str),
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

TAc.print(LANG.render_feedback("instance",f"Instance {m}x{n}: "), "yellow", ["bold"])
pirellone0,_=pl.random_pirellone(m, n, solvable=True)
pirellone1=copy.deepcopy(pirellone0)
pl.print_pirellone(pirellone0)
TAc.print(LANG.render_feedback("instance-sol","Solution of instance: "), "yellow", ["bold"])
"".join(pl.soluzione_min(pirellone1,m,n))
sub_n=random.randint(2, n-1)
sub_m=random.randint(2, m-1)
pirellone=[[0 for j in range(0,sub_n)] for i in range(0,sub_m)]
if ENV['submatrix_type']=='consecutive':
    for i in range(0,sub_m):
        for j in range(0,sub_n):
            pirellone[i][j]=pirellone0[i][j]
elif ENV['submatrix_type']=='any':
    r=[]
    c=[]
    for i in range(m):
        r.append(i)
    for j in range(n):
        c.append(j)
    sub_r=random.sample(r, sub_m)
    sub_c=random.sample(c, sub_n)
    u=[]
    v=[]
    for i in sub_r:
        u.append(i)
    for j in sub_c:
        v.append(j)
    u.sort()
    v.sort()
    h=0
    k=0
    for i in u:
        for j in v:
            pirellone[h][k]=pirellone0[i][j]
            k+=1
        k=0
        h=+1
     
TAc.print(LANG.render_feedback("sub-matrix",f"Submatrix {sub_m}x{sub_n}"), "yellow", ["bold"])   
pl.print_pirellone(pirellone)     
TAc.print(LANG.render_feedback("bub-matrix-sol",f"Solution of the submatrix {sub_m}x{sub_n} : "), "yellow", ["bold"])
solu=input()
solu=solu.split()
pl.off_lista(pirellone,solu,TAc,LANG)

    
exit(0)
