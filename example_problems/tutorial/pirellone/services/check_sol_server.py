#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="check_sol"
args_list = [
    ('instance',str),
    ('coding',str),
    ('seed',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import exit
import pirellone_lib as pl
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
TAc.print(LANG.render_feedback("insert-num-rows", 'Insert the number of rows:'), "yellow", ["bold"])
m=int(input())
TAc.print(LANG.render_feedback("insert-num-col", 'Insert the number of columns:'), "yellow", ["bold"])
n=int(input())

if ENV['instance']=='random':
    pirellone, seed=pl.random_pirellone(m, n, ENV['seed'], solvable=True)
    TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
    pl.print_pirellone(pirellone)
elif ENV['instance']=='mine':
    TAc.print(LANG.render_feedback("instance-","Instance to check:"), "yellow", ["bold"])
    pirellone=[]
    for i in range(m):
        row = TALinput(int, num_tokens=n)
        pirellone.append(row)   

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


b,solvable=pl.check_off_lights(pirellone,solu)
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
