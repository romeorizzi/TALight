#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="bit_edit_to_zero"
service="total_steps"
args_list = [
    ('number',str),
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
if ENV['number']=='any':
    n=el.rand_bit()
    s=''
    for i in range(len(n)):
        s+=f'{n[i]}'
    TAc.print(LANG.render_feedback("random-num", f'Random number: {s}'), "yellow", ["bold"])
elif ENV['number']=='my':
    TAc.print(LANG.render_feedback("insert-num-bin", 'Insert the number in binary form:'), "yellow", ["bold"])
    p=str(input())
    n=[]
    for i in range(len(p)):
        n.append(int(p[i]))
        
        

correct_steps=el.num_mosse(n)

      
TAc.print(LANG.render_feedback("insert-solu", 'Insert your solution:'), "yellow", ["bold"])
solu=int(input())

if solu==correct_steps:
    TAc.OK()
    TAc.print(LANG.render_feedback("correct", 'Correct!'), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("not-correct", 'This is not correct.'), "red", ["bold"])
    if solu<correct_steps:
        TAc.print(LANG.render_feedback("less", 'This doesn\'t transform the number to zero.'), "red", ["bold"])
    elif solu>correct_steps:
        TAc.print(LANG.render_feedback("more", 'Too much steps.'), "red", ["bold"])
                          
                                       
    """if ENV['please_do_it_for_me']==1:
        TAc.print(LANG.render_feedback("correct-num", f'The correct number is:{correct_bin}'), "green", ["bold"])
"""        
    
    
    
exit(0)