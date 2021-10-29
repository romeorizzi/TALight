#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('coding',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
TAc.print(LANG.render_feedback("insert-num-rows", 'Insert the number of rows:'), "yellow", ["bold"])
m=TALinput(int, 1, TAc=TAc)[0]
TAc.print(LANG.render_feedback("insert-num-col", 'Insert the number of columns:'), "yellow", ["bold"])
n=TALinput(int, 1, TAc=TAc)[0]

if ENV['seed']=='random_seed':
    pirellone, seed=pl.random_pirellone(m, n, seed="random_seed", solvable=True)
else:
    pirellone, seed=pl.random_pirellone(m, n, ENV['seed'], solvable=True)
    
TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
pl.print_pirellone(pirellone)

if ENV['coding']=='seq':
    TAc.print(LANG.render_feedback("sequence-r-c","Sequence of rows and columms: "), "yellow", ["bold"])
    solu=input()
    solu=solu.split()
elif ENV['coding']=='subset':
    TAc.print(LANG.render_feedback("rows-sol","Rows solution: "), "yellow", ["bold"])
    rs = TALinput(int, num_tokens=m)
    TAc.print(LANG.render_feedback("col-sol","Columns solution: "), "yellow", ["bold"])
    cs = TALinput(int, num_tokens=n)
    solu=[]
    for i in range(len(rs)):
        if rs[i]:
            solu.append(f'r{i+1}')
    for j in range(len(cs)):
        if cs[j]:
            solu.append(f'c{j+1}')


b,solvable=pl.check_off_lights(pirellone,solu,LANG, TAc)
if b and solvable=='s':
    TAc.OK()
    TAc.print(LANG.render_feedback('correct',"This sequence turns off all lights."), "green", ["bold"])
if b==False and solvable=='s':
    TAc.NO()
    TAc.print(LANG.render_feedback('not-correct',"This sequence doesn't turn off all lights see what happens using your solution:"), "red", ["bold"])
    pl.print_pirellone(pirellone)    

if b and solvable=='n':
    TAc.OK()
    TAc.print(LANG.render_feedback('no-more-lights',"You can not turn off more lights."), "green", ["bold"])
if b==False and solvable=='n':
    TAc.NO()
    TAc.print(LANG.render_feedback('do-better',"You can turn off more lights, check it: "), "red", ["bold"])
    pl.print_pirellone(pirellone)   
    
exit(0)
