#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import bit_edit_to_zero_lib as el

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('number',str),
    ('feedback',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
if ENV['number']=='random':
    n=el.rand_bit()
    s=''
    for i in range(len(n)):
        s+=f'{n[i]}'
    TAc.print(LANG.render_feedback("random-num", f'# Random binary number from where to start:'), "yellow", ["bold"])
    TAc.print(s, "yellow", ["bold"])
else:
    assert ENV['number']=='my'
    TAc.print(LANG.render_feedback("insert-num-bin", 'Insert the starting number in binary form:'), "yellow", ["bold"])
    p=str(input())
    n=[]
    for i in range(len(p)):
        n.append(int(p[i]))
        
        

correct_steps=el.num_mosse(n)

      
TAc.print(LANG.render_feedback("insert-answ", '# Insert your answer (minimum numbr of total steps):'), "yellow", ["bold"])
answ=TALinput(int, 1, TAc=TAc)[0]

if answ==correct_steps:
    TAc.OK()
    TAc.print(LANG.render_feedback("correct", 'Correct!'), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("not-correct", 'This is not correct.'), "red", ["bold"])
    if ENV['feedback']=='true_val':
        print(LANG.render_feedback("true-val", f'The minimum number of steps needed is {correct_steps}.'))
    if ENV['feedback']=='smaller_or_bigger':
        if answ<correct_steps:
            print(LANG.render_feedback("more", f'More than {answ} steps are required in order to go from {s} to zero.'))
        if answ>correct_steps:
            print(LANG.render_feedback("less", f'You can go from {s} to zero in strictly less than {answ} steps.'))
   
    
exit(0)
