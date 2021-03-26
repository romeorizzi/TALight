#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="bit_edit_to_zero"
service="trilly"
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
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

TAc.print(LANG.render_feedback("insert-num-bin", 'Insert the number in binary form:'), "yellow", ["bold"])
p=str(input())
n=[]
for i in range(len(p)):
    n.append(int(p[i]))
        
        

mossa=el.mossa(n)

  

TAc.print(LANG.render_feedback("correct", f'You should do the step {mossa} to reach your goal.'), "green", ["bold"])

    
    
exit(0)