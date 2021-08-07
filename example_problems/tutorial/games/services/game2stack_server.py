#!/usr/bin/env python3
from sys import stderr, exit
from random import randrange

from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem="games"
service="game2stack"
args_list = [
    ('num_questions',int),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

gen_new_s = True    
for _ in range(ENV['num_questions']):
    if gen_new_s:
            a=randrange(1,100)
            b=randrange(5,100)
    TAc.print(f"? ({a},{b})", "yellow", ["bold"])
    sa,sb= (input().split())
    sa=int(sa)
    sb=int(sb)
    gen_new_s = False
    
    if a>b and sa==a-b and sb==0:
        gen_new_s = True
        TAc.OK()
        TAc.print(LANG.render_feedback("correct", "This is the best move you can do!"), "green", ["bold"])
    elif a<b and sa==0 and sb==b-a:
        gen_new_s = True
        TAc.OK()
        TAc.print(LANG.render_feedback("correct", "This is the best move you can do!"), "green", ["bold"])
    elif a==b and sa==0 and sb==0:
        gen_new_s = True
        TAc.OK()
        TAc.print(LANG.render_feedback("correct", "This is the best move you can do!"), "green", ["bold"])
    else:
        TAc.NO() 
        TAc.print(LANG.render_feedback("not-correct", "This is not the best you can do."), "yellow", ["bold"])
            
TAc.Finished()
exit(0)
      