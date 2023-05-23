#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('assertion',str),
    ('with_certificate',int),
]
ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
TAc.print(LANG.render_feedback("rows","Rows:"), "yellow", ["bold"])
m=TALinput(int, 1, TAc=TAc)[0]
TAc.print(LANG.render_feedback("col","Columns:"), "yellow", ["bold"])
n=TALinput(int, 1, TAc=TAc)[0]
TAc.print(LANG.render_feedback("insert-counter","Insert your counterexample:"), "yellow", ["bold"])
p=[]
for i in range(m):
    row = TALinput(int, num_tokens=n) 
    p.append(row)

if n>2 or m>2:
    TAc.NO() 
    TAc.print(LANG.render_feedback("no-min","Not minimum matrix."), "red", ["bold"])
else:
    if pl.is_solvable(p):
        TAc.NO() 
        TAc.print(LANG.render_feedback("solvable","Solvable!"), "red", ["bold"])
        if ENV['with_certificate']:
            TAc.print(LANG.render_feedback("sol","This is the solution: "), "yellow", ["bold"])
            sol=pl.solution(p)
            print(" ".join(sol))
    else:
        TAc.OK()
        TAc.print(LANG.render_feedback("correct","Correct: it is not solvable and minimum."), "green", ["bold"])

exit(0)
