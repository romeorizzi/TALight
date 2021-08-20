#!/usr/bin/env python3
from sys import stderr, exit
from random import randrange

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

# METADATA OF THIS TAL_SERVICE:
problem="games"
service="game123"
args_list = [
    ('num_questions',int),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 

gen_new_s = True    
for _ in range(ENV['num_questions']):
    if gen_new_s:
            s = randrange(5,100)
    TAc.print(f"? {s}", "yellow", ["bold"])
    a= TALinput(int, 1, TAc=TAc)[0]
    gen_new_s = False
    
    if a>3:
        TAc.NO() 
        TAc.print(LANG.render_feedback("wrong-intput", "Attention! Wrong input!"), "red", ["bold"])  
    else:
        if s%4==a and a!=0:
            gen_new_s = True
            TAc.OK()
            TAc.print(LANG.render_feedback("correct", "This is the best move you can do!"), "green", ["bold"])
        elif s%4==a and a==0:
            gen_new_s = True
            TAc.OK()
            TAc.print(LANG.render_feedback("correct", "You lose."), "green", ["bold"])
            
        else:
            TAc.NO() 
            TAc.print(LANG.render_feedback("not-correct", "This is not the best you can do."), "yellow", ["bold"])

            
TAc.Finished()
exit(0)
