#!/usr/bin/env python3

from os import environ
from sys import exit
from random import randrange

from multilanguage import *

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]
ENV_obj = environ["TAL_obj"]
ENV_num_questions = int(environ["TAL_num_questions"])
ENV_colored_feedback = (environ["TAL_ISATTY"] == "1")

set_colors(ENV_colored_feedback)
messages_book = select_book_and_lang("sum_server", ENV_lang)
        
def print_lang(msg_code, *msg_rendering, **kwargs):
    msg_text=eval(f"f'{messages_book[msg_code]}'")
    TAcprint(msg_text, *msg_rendering, **kwargs)

        

print_lang("open-channel", "green", "on_blue")        
#English: print(f"# I will serve: problem=sum, service=sum, numbers={ENV_numbers}, obj={ENV_obj}, num_questions={ENV_num_questions}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

gen_new_s = True    
for _ in range(ENV_num_questions):
    if gen_new_s:
        if ENV_numbers == "onedigit":
            s = randrange(10)
        elif ENV_numbers == "twodigits":
            s = randrange(100)
        else:
            s = randrange(2**64)
    TAcprint(f"? {s}", "yellow", "on_blue", ["bold"])
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_s = False
    if a+b > s:
        TAcNO() 
        print_lang("too-much", "yellow", "on_blue", ["underline"])        
        #English: print(f"indeed, {a}+{b}={a+b} > {s}.")
    elif a+b < s:
        TAcNO() 
        print_lang("too-little", "yellow", "on_blue", ["underline"])        
        #English: print(f"indeed, {a}+{b}={a+b} < {s}.")
    else: # a + b == n
        if ENV_obj == "max_product":
            if a < b:
                a,b = b,a
            if a-b > 1:
                TAcNO() 
                print_lang("not-balanced", "yellow", "on_blue", ["underline"])        
                #English: print(f"indeed, {a-1}+{b+1}={s} and {a-1}*{b+1}={(a-1)*(b+1)} > {a*b}={a}*{b}.")
            else:
                gen_new_s = True
                TAcOK()
                print_lang("max-product", "grey", "on_blue")        
                #English: print(f"indeed, x={a} and y={b} have maximum product among the integer numbers with x+y={s}. Do you know why? Do you have a proof for your intuition?")
        else:
            TAcOK()
            print_lang("right-sum", "grey", "on_blue")        
            #English: print(f"indeed, {a}+{b}={s}")
            gen_new_s = True
            
TAcFinished()
exit(0)
