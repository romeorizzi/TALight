#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import asteroid_lib as al


# METADATA OF THIS TAL_SERVICE:
problem="asteroid"
service="minimum_laser_server"
args_list = [
    ('level',str),
    ('seed',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
if ENV['level']=='easy':
    q=5
if ENV['level']=='medium':
    q=8
if ENV['level']=='difficult':  
    q=11

quad,seed=al.random_quad(q,ENV['seed'])
TAc.print(LANG.render_feedback("instance", f'Instance (of seed: {seed}):'), "yellow", ["bold"])
al.visualizza(quad)  
TAc.print(LANG.render_feedback("solu", 'Insert your solution: '), "yellow", ["bold"]) 
solu0=TALinput(str,regex="^(r|c)(0|[1-9][0-9]{0,2})$", regex_explained="a single row or column (with indexes starting from 0). Example 1: r0 to specify the first row. Example 2: c2 to specify the third column.", line_explained="a subset of rows and columns where indexes start from 0. Example: r0 c5 r2 r7", TAc=TAc, LANG=LANG)
solu=[]
for row_or_col,index in solu0:
    solu.append((row_or_col,int(index)))

al.verifica(solu,quad,TAc,LANG)
    
exit(0)
