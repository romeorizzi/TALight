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
TAc.print("Rows:", "yellow", ["bold"])
n=int(input())
TAc.print("Columns:", "yellow", ["bold"])
m=int(input())

if ENV['instance']=='any':
    TAc.print("Istance: ", "yellow", ["bold"])
    pirellone=pl.random_pirellone(n, m, solvable=True)
    pl.print_pirellone(pirellone)
elif ENV['instance']=='my':
    TAc.print("Instance to check:", "yellow", ["bold"])
    pirellone=[]
    for i in range(0,n):
        row = list(map(int,input().strip().split()))[:n] 
        pirellone.append(row)   

if ENV['coding']=='seq':
    TAc.print("Sequence of rows and colums: ", "yellow", ["bold"])
    solu=input()
    solu=solu.split()
    pl.off_lista(pirellone,solu,TAc, LANG)
elif ENV['coding']=='subset':
    TAc.print("Rows solution: ", "yellow", ["bold"])
    rs = list(map(int,input().strip().split()))[:n] 
    TAc.print("Columns solution: ", "yellow", ["bold"])
    cs = list(map(int,input().strip().split()))[:m]
    pl.off(pirellone,rs,cs,TAc, LANG)

    
exit(0)
