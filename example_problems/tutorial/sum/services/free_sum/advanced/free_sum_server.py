#!/usr/bin/env python3
from sys import stderr, exit, argv
from random import randrange

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('num_questions',int),
    ('numbers',str),
    ('obj',str),
    ('META_TTY',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 

LANG.print_opening_msg()
gen_new_s = True    
for _ in range(ENV['num_questions']):
    if gen_new_s:
        if ENV['numbers'] == "onedigit":
            s = randrange(10)
        elif ENV['numbers'] == "twodigits":
            s = randrange(100)
        else:
            s = randrange(2**64)
    TAc.print(f"{s}", "yellow", ["bold"])
    a, b = TALinput(int, 2, TAc=TAc)
    gen_new_s = False
    if a+b > s:
        TAc.NO() 
        TAc.print(LANG.render_feedback("too-much", f"indeed, {a}+{b}={a+b} > {s}."), "yellow", ["underline"])        
    elif a+b < s:
        TAc.NO() 
        TAc.print(LANG.render_feedback("too-little", f"indeed, {a}+{b}={a+b} < {s}."), "yellow", ["underline"])        
    else: # a + b == n
        if ENV['obj'] == "max_product":
            if a < b:
                a,b = b,a
            if a-b > 1:
                TAc.NO() 
                TAc.print(LANG.render_feedback("not-balanced", f"indeed, {a-1}+{b+1}={s} and {a-1}*{b+1}={(a-1)*(b+1)} > {a*b}={a}*{b}."), "yellow", ["underline"])        
            else:
                gen_new_s = True
                TAc.OK()
                TAc.print(LANG.render_feedback("max-product", f"indeed, x={a} and y={b} have maximum product among the integer numbers with x+y={s}. Do you know why? Do you have a proof for your intuition?"), "grey")
        else:
            TAc.OK()
            TAc.print(LANG.render_feedback("right-sum", f"indeed, {a}+{b}={s}"), "grey")        
            gen_new_s = True
            
TAc.Finished()
exit(0)
