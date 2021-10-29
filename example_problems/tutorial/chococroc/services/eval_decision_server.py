#!/usr/bin/env python3
from sys import stderr, exit
from time import monotonic
import copy

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import pirellone_lib as pl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('with_check_of_sol',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 

if ENV['seed']=='random_seed': 
    seed_service = random.randint(100000,999999)
else:
    seed_service = int(ENV['seed'])
random.seed(seed_service)
TAc.print(LANG.render_feedback("seed-service",f'# The service is running with seed={seed_service}'), "green")
TAc.print(LANG.render_feedback("explain-protocol","# Each instance describes a 0,1-matrix. Print \'y\' if this matrix can be turned off with the allowed moves, otherwise print \'n\'. After printing 'y', if the service has been called with the flag \'with_check_of_sol\' set to 1, you should also print, in the following line, a solution, i.e., a sequence of moves leading to the all zero matrix (example: r1 c3 r5)") , "green")

#             |   M                               | N  |
# correct     | 10 compilato; 7 python, java      | =M |
# efficient   | 100 compilato; 100 python, java   | =M |
#
# 1 secondo


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
    pirellone,_,sr,sc=pl.random_pirellone(m, n, solvable=True,s=True)
    print(pirellone)
    sol_togive=pl.solution_irredundant(pirellone,sr,sc)
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
        moff,_=pl.check_off_lights(pirellone,sol_to_ver)
        if not moff:
            TAc.print(LANG.render_feedback("wrong",f"# No!The solution of the matrix of seed={_} is not correct."), "red", ["bold"])
            exit(0)
        if len(sol_to_ver)>len(sol_togive):
            TAc.print(LANG.render_feedback("semi-correct",f"# The solution of the matrix of seed={_} is not minimum."), "yellow", ["bold"])
        if time > 1:
            TAc.print(LANG.render_feedback("not-efficient", '# No. Your solution is not efficient. Run on your machine, it took more than one second to compute the solution.'), "red", ["bold"])        
            exit(0)
        else:
            TAc.print(LANG.render_feedback("efficient", '# ♥ Ok. Your solution is efficient.'), "green")
            if len(sol_to_ver)==len(sol_togive):
                TAc.print(LANG.render_feedback("correct", '# ♥ Your solution is the best one.'), "green",["bold"])
        sol_to_ver.clear()
        sol=''
        pirellone.clear()
    
exit(0)
