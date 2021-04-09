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
from time import monotonic
import copy
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

for i in range(15):
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
    print(pirellone)
    sol_togive=pl.soluzione_min(copy.deepcopy(pirellone),m,n)
    a=monotonic()
    sol=input()
    sol_to_ver=[]
    if sol[0] != '#':
        for i in range(len(sol)):
            if sol[i]=='r':
                sol_to_ver.append(f'r{sol[i+1]}')
            if sol[i]=='c':
                sol_to_ver.append(f'c{sol[i+1]}')
    
        b=monotonic() 
        time=b-a
        if not pl.off_lista_noprint(pirellone,sol_to_ver):
            TAc.print(LANG.render_feedback("wrong",f"#No!The solution of the matrix of seed={_} is not correct."), "red", ["bold"])
            exit(0)
        if len(sol_to_ver)>len(sol_togive):
            TAc.print(LANG.render_feedback("semi-correct",f"#The solution of the matrix of seed={_} is not minimum."), "yellow", ["bold"])
        if time > 1:
            TAc.print(LANG.render_feedback("not-efficient", '#No. Your solution is not efficient. Run on your machine, it took more than one second to compute the solution.'), "red", ["bold"])        
            exit(0)
        else:
            TAc.print(LANG.render_feedback("efficient", '# ♥ Ok. Your solution is efficient.'), "green")
            if len(sol_to_ver)==len(sol_togive):
                TAc.print(LANG.render_feedback("correct", '# ♥ Your solution is the best one.'), "green",["bold"])
        sol_to_ver.clear()
        sol=''
        pirellone.clear()
    
exit(0)