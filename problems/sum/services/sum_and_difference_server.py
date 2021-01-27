#!/usr/bin/env python3

from os import environ
from sys import exit
from random import randrange

from multilanguage import *

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]
ENV_num_questions = int(environ["TAL_num_questions"])
ENV_colored_feedback = (environ["TAL_colored_feedback"] == "yes")

set_colors(ENV_colored_feedback)
messages_book = select_book_and_lang("sum_and_difference_server", ENV_lang)
        
def print_lang(msg_code, *msg_rendering, **kwargs):
    msg_text=eval(f"f'{messages_book[msg_code]}'")
    TAcprint(msg_text, *msg_rendering, **kwargs)



print_lang("open-channel", "green", "on_blue")        
#English: print(f"# I will serve: problem=sum, service=sum_and_difference, numbers={ENV_numbers}, num_questions={ENV_num_questions}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

gen_new_pair = True    
for _ in range(ENV_num_questions):
    if gen_new_pair:
        if ENV_numbers == "onedigit":
            x = randrange(10)
            y = randrange(10)
        elif ENV_numbers == "twodigits":
            x = randrange(100)
            y = randrange(100)
        else:
            x = randrange(2**64)
            y = randrange(2**64)
    if x < y:
        x,y = y,x
    TAcprint(f"? {x+y} {x-y}", "yellow", "on_blue", ["bold"])
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_pair = False
    if a+b > x+y:
        TAcNO() 
        print_lang("over-sum", "yellow", "on_blue", ["underline"])        
        #English: print(f"indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:    
        TAcNO() 
        print_lang("under-sum", "yellow", "on_blue", ["underline"])        
        #English: print(f"indeed, {a}+{b}={a+b} < {x+y}.")
    elif abs(a-b) > x-y:    
        TAcNO() 
        print_lang("too-apart", "yellow", "on_blue", ["underline"])        
        #English: print(f"indeed, |{a}-{b}|={abs(a-b)} > {x-y}.")
    elif abs(a-b) < x-y:    
        TAcNO() 
        print_lang("too-close", "yellow", "on_blue", ["underline"])        
        #English: print(f"indeed, |{a}-{b}|={abs(a-b)} < {x-y}.")
    else:
        TAcOK() 
        assert (a + b == x+y) and (abs(a-b) == x-y)
        print_lang("ok", "grey", "on_blue")        
        #English: print(f"indeed, {a}+{b} = {x+y} and |{a}-{b}| = {x-y}.")
        gen_new_pair = True

TAcFinished()
exit(0)
