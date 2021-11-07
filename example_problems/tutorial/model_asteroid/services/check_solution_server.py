#!/usr/bin/env python3
from sys import exit
import random
from functools import partial

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import asteroid_lib as al

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('input_mode',str),
    ('m',int),
    ('n',int),
    ('sol_style',str),
    ('goal',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
matrix,seed=al.gen_instance(ENV['m'],ENV['n'],ENV['seed'])
TAc.print(LANG.render_feedback("instance", f'Instance (of seed: {seed}):'), "yellow", ["bold"])
al.visualizza(matrix)  
TAc.print(LANG.render_feedback("user_sol", 'Insert your solution: '), "yellow", ["bold"]) 
user_sol=[]
if ENV['sol_style'] == 'seq':
    raw_sol = TALinput(str,regex="^\s*|(r|c)(0|[1-9][0-9]{0,2})$", regex_explained="a single row or column (with indexes starting from 0). Example 1: r0 to specify the first row. Example 2: c2 to specify the third column.", token_recognizer=lambda move,TAc,LANG: al.check_one_move_seq(move,ENV['m'],ENV['n'],TAc,LANG), line_explained="a subset of rows and columns where indexes start from 0. Example: r0 c5 r2 r7", TAc=TAc, LANG=LANG)
    for token in raw_sol:
      if token != "":  
        user_sol.append((token[0],int(token[1:])))
if ENV['sol_style'] == 'subset':
    raw_sol_rows = TALinput(bool, num_tokens=ENV['m'], line_explained=f"enter {ENV['m']} 0,1-digits separated by spaces, one for each row. Example: {' '.join(str(random.randint(0,1)) for _ in range(ENV['m']))}", TAc=TAc, LANG=LANG)
    for val,index in zip(raw_sol_rows,range(ENV['m'])):
        if val == 1:
            user_sol.append(('r',index))
    raw_sol_cols = TALinput(bool, num_tokens=ENV['n'], line_explained=f"enter {ENV['n']} 0,1-digits separated by spaces, one for each row. Example: {' '.join(str(random.randint(0,1)) for _ in range(ENV['n']))}", TAc=TAc, LANG=LANG)
    for val,index in zip(raw_sol_cols,range(ENV['n'])):
        if val == 1:
            user_sol.append(('c',index))

if al.is_feasible_shooting(ENV['m'],ENV['n'],matrix,user_sol,silent=False,TAc=TAc,LANG=LANG) and ENV.service=="check_optimality_of_your_laser_beams":
    al.is_optimal_shooting(ENV['m'],ENV['n'],matrix,user_sol,silent=False,TAc=TAc,LANG=LANG)
    
exit(0)
