#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="check_sol"
args_list = [
    ('instance',str),
    ('coding',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
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
    TAc.print("Instance: ", "yellow", ["bold"])
    pirellone=pl.random_pirellone(m, n, solvable=True)
    pl.print_pirellone(pirellone)
elif ENV['instance']=='mine':
    TAc.print("Instance to check:", "yellow", ["bold"])
    pirellone=[]
    for i in range(0,m):
        row = TALinput(bool, num_tokens=n)
        #row = list(map(int,input().strip().split()))[:n]
        pirellone.append(row)   

if ENV['coding']=='seq':
    TAc.print("Sequence of rows and colums: ", "yellow", ["bold"])
    solu=input()
    solu=solu.split()
    pl.off_lista(pirellone,solu,TAc, LANG)
elif ENV['coding']=='subset':
    TAc.print("Rows solution: ", "yellow", ["bold"])
    rs = list(map(int,input().strip().split()))[:m] 
    TAc.print("Columns solution: ", "yellow", ["bold"])
    cs = list(map(int,input().strip().split()))[:n]
    pl.off(pirellone,rs,cs,TAc, LANG)

    
exit(0)
