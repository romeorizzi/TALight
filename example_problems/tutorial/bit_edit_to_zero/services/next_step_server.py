#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="bit_edit_to_zero"
service="next_step"
args_list = [
    ('lang',str),
    ('ISATTY',bool),
]

from sys import exit
import bit_edit_to_zero_lib as el



from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 

n=el.rand_bit()
s=''
for i in range(len(n)):
    s+=f'{n[i]}'
TAc.print(LANG.render_feedback("random-num", f'Random number: {s}'), "yellow", ["bold"])

        
        

mossa=el.mossa(n)

      
TAc.print(LANG.render_feedback("insert-solu", 'Insert your move, 1 or 2?'), "yellow", ["bold"])
solu=TALinput(int, 1, TAc=TAc)[0]

if solu==mossa:
    TAc.OK()
    TAc.print(LANG.render_feedback("correct", 'Correct!'), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("not-correct", 'This is not correct.'), "red", ["bold"])


    
    
exit(0)

