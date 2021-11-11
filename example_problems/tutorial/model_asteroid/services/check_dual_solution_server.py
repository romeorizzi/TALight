#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import model_asteroid_lib as al

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('m',int),
    ('n',int),
    ('feedback',str),
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
user_sol=[]
risp = None
while True:
#    risp=TALinput(int,2, exceptions = {"#END"}, line_explained="two integers (the row and column indexes of an asteroid). Otherwise, just enter the string '#END' to end your immission.", line_recognizer=lambda line,TAc,LANG: al.check_row_index(int(line.split()[0]),ENV['m'],TAc,LANG) and al.check_col_index(int(line.split()[1]),ENV['n'],TAc,LANG), TAc=TAc, LANG=LANG)
    risp=TALinput(int,2, exceptions = {"#END"}, line_explained="two integers (the row and column indexes of an asteroid). Otherwise, just enter the string '#END' to end your immission.", line_recognizer=lambda line,TAc,LANG: al.check_is_cell_containing_asteroid(int(line.split()[0]),int(line.split()[1]),matrix,TAc,LANG), TAc=TAc, LANG=LANG)
    if risp[0] == "#END":
        break
    user_sol.append((int(risp[0]),int(risp[1])))

if al.is_feasible_asteroid_set(ENV['m'],ENV['n'],matrix,user_sol,silent=False,TAc=TAc,LANG=LANG) and ENV['goal']=="check_optimality":
    al.is_optimal_asteroid_set(ENV['m'],ENV['n'],matrix,user_sol,silent=False,give_a_better_solution_if_any=ENV["feedback"]=="give_a_better_solution_if_any", TAc=TAc,LANG=LANG)
    
exit(0)
