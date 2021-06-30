#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="bit_edit_to_zero"
service="decimal_to_binary"
args_list = [
    ('please_do_it_for_me',int),
    ('number',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import exit
import bit_edit_to_zero_lib as el
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
if ENV['number']=='any':
    n=random.randrange(0,100)
    TAc.print(LANG.render_feedback("random-num", f'Random number: {n}'), "yellow", ["bold"])
elif ENV['number']=='my':
    TAc.print(LANG.render_feedback("insert-num", 'Insert the number in decimal form:'), "yellow", ["bold"])
    n=TALinput(int, 1, TAc=TAc)
correct_bin=el.dec_to_bin(n) 
      
TAc.print(LANG.render_feedback("insert-solu", 'Insert your solution:'), "yellow", ["bold"])
solu=TALinput(int, 1, TAc=TAc)

if solu==correct_bin:
    TAc.OK()
    TAc.print(LANG.render_feedback("correct", 'Correct!'), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("not-correct", 'This is not correct.'), "red", ["bold"])
    if ENV['please_do_it_for_me']==1:
        TAc.print(LANG.render_feedback("correct-num", f'The correct number is:{correct_bin}'), "green", ["bold"])
        
    
    
    
exit(0)