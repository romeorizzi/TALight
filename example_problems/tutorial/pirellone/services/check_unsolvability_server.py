#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="check_unsolvability"
args_list = [
    ('goal',str),
    ('lang',str),
    ('ISATTY',bool),
]
import pirellone_lib as pl
from sys import exit
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
TAc.print(LANG.render_feedback("rows","Rows:"), "yellow", ["bold"])
m=int(input())
TAc.print(LANG.render_feedback("col","Columns:"), "yellow", ["bold"])
n=int(input())
TAc.print(LANG.render_feedback("insert-counter","Insert your counterexample:"), "yellow", ["bold"])
p=[]
for i in range(m):
    row = TALinput(int, num_tokens=n) 
    p.append(row)
if ENV['goal']=='minimum' or ENV['goal']=='any':
    if n>2 or m>2:
        TAc.NO() 
        TAc.print(LANG.render_feedback("no-min","Not minimum matrix."), "red", ["bold"])
    else:
        if pl.is_solvable(p, m, n):
            TAc.NO() 
            TAc.print(LANG.render_feedback("solvable","Solvable!"), "red", ["bold"])
        else:
            TAc.OK()
            TAc.print(LANG.render_feedback("correct","Correct: it is not solvable and minimum."), "green", ["bold"])
else:
    if pl.is_solvable(p, m, n):
            TAc.NO() 
            TAc.print(LANG.render_feedback("solvable","Solvable!"), "red", ["bold"])
    else:
        TAc.OK()
        TAc.print(LANG.render_feedback("correct-no-min","Correct but not minimum."), "green", ["bold"])
    
exit(0)
