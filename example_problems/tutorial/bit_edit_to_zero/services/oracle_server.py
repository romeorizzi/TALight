#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import bit_edit_to_zero_lib as el

# METADATA OF THIS TAL_SERVICE:
problem="bit_edit_to_zero"
service="trilly"
args_list = [
    ('binary_starting_number',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 

if ENV['binary_starting_number'] == 'lazy':
    TAc.print(LANG.render_feedback("insert-num-bin", 'Insert the number in binary form:'), "yellow", ["bold"])
    p=str(input())
else:
    p=ENV['binary_starting_number']
n=[]
for i in range(len(p)):
    n.append(int(p[i]))
        

mossa=el.mossa(n)  

TAc.print(LANG.render_feedback("oracle_response", f'You should play a step of type {mossa} as your very first move (in order to get down to zero as fast as possible).'), "green", ["bold"])

    
    
exit(0)
