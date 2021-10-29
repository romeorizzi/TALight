#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import asteroid_lib as al

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('m',int),
    ('n',int),
    ('feedback',bool),
    ('goal',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
matrix,seed=al.gen_instance(ENV['m'],ENV['n'],ENV['seed'])
TAc.print(LANG.render_feedback("instance", f'Instance (of seed: {seed}):'), "yellow", ["bold"])
al.visualizza(matrix)  
TAc.print(LANG.render_feedback("user_sol", 'Insert your set of independent asteroids: '), "yellow", ["bold"]) 
solu0=input().split()
solu=[]
for i in range(len(solu0)):
    solu.append((int(solu0[i][0]),int(solu0[i][2])))

if al.is_feasible_asteroid_set(ENV['m'],ENV['n'],matrix,user_sol,silent=False,TAc=TAc,LANG=LANG) and ENV['goal']=="check_optimality":
    al.is_optimal_asteroid_set(ENV['m'],ENV['n'],matrix,user_sol,silent=False,give_a_better_solution_if_any=ENV["give_a_better_solution_if_any"]TAc=TAc,LANG=LANG)
    
exit(0)
