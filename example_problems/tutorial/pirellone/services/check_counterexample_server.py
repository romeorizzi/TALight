#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="check_counterexample"
args_list = [
    ('goal',str),
    ('lang',str),
    ('ISATTY',bool),
]
import pirellone_lib as pl
from sys import stderr, exit, argv
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
TAc.print("Counterexample:", "yellow", ["bold"])
p=[]
for i in range(0,n):
    row = list(map(int,input().strip().split()))[:n] 
    p.append(row)

if n!=len(p) or m!=len(p[0]):
    TAc.print("NOT RIGHT DIMENSION", "red", ["bold"])
    exit(0)

if ENV['goal']=='minimal':
    if m>2 or n>2:
        TAc.NO() 
        TAc.print("Not minimal", "red", ["bold"])
    else:
        if pl.is_solvable(p, n, m):
            TAc.NO() 
            TAc.print("Solvable!", "red", ["bold"])
        else:
            TAc.OK()
            TAc.print("Correct: not solvable and minimal", "green", ["bold"])
else:
    if pl.is_solvable(p, n, m):
            TAc.NO() 
            TAc.print("Solvable!", "red", ["bold"])
    else:
        TAc.OK()
        TAc.print("Correct but not minimal", "green", ["bold"])
    
exit(0)
