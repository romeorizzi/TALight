#!/usr/bin/env python3
from sys import stderr, exit
from time import monotonic
import copy
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import pirellone_lib as pl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('m',int),
    ('n',int),
    ('with_check_of_sol',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
m=ENV['m'] 
n=ENV['n'] 
with_check_of_sol=ENV['with_check_of_sol']
if ENV['seed']=='random_seed': 
    seed_service = random.randint(100000,999999)
else:
    seed_service = int(ENV['seed'])
random.seed(seed_service)
TAc.print(LANG.render_feedback("seed-service",f'# The service is running with seed={seed_service}'), "green")
TAc.print(LANG.render_feedback("explain-protocol","# Each instance describes a 0,1-matrix. Print \'y\' if this matrix can be turned off with the allowed moves, otherwise print \'n\'. After printing 'y', if the service has been called with the flag \'with_check_of_sol\' set to 1, you should also print, in the following line, a solution, i.e., a sequence of moves leading to the all zero matrix (example: r1 c3 r5)") , "green")


pirellone,_,sr,sc=pl.random_pirellone(m, n, solvable=True,s=True)
pl.print_pirellone(pirellone)
sol_togive=pl.solution_irredundant(pirellone,sr,sc)
TAc.print(LANG.render_feedback("given-sol",'Does this solution turn off the instance?'), "yellow")
print(" ".join(sol_togive))

answer=TALinput(str, num_tokens=1, regex="^(y|n)$", TAc=TAc, LANG=LANG)
moff,_=pl.check_off_lights(pirellone,sol_togive,LANG,TAc)

if moff==True and answer[0]=='y':
    TAc.print(LANG.render_feedback("correct", 'Yes you are right, this solution turns off the instance.'), "green",["bold"])
    exit(0)
elif moff==False and answer[0]=='n':
    TAc.print(LANG.render_feedback("correct-lights-off", 'Yes you are right, this solution does not turn off the instance.'), "green",["bold"])
    exit(0)
else:
    TAc.print(LANG.render_feedback("not-correct", 'No, your decision is not right'), "red",["bold"])
    if with_check_of_sol==1:
        TAc.print(LANG.render_feedback("sol", 'Look at the solution:'), "red",["bold"])
        print(" ".join(pl.solution_min(sr,sc)))
        
    exit(0)


exit(0)
