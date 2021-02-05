#!/usr/bin/env python3

from os import environ
from sys import exit
from random import randrange

from multilanguage import *

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]
ENV_num_questions = int(environ["TAL_num_questions"])
ENV_colored_feedback = (environ["TAL_ISATTY"] == "1")

set_colors(ENV_colored_feedback)
messages_book = select_book_and_lang("sum_and_product_server", ENV_lang)
        
def print_lang(msg_code, *msg_rendering, **kwargs):
    msg_text=eval(f"f'{messages_book[msg_code]}'")
    TAcprint(msg_text, *msg_rendering, **kwargs)



print_lang("open-channel", "green")        
#English: print(f"# I will serve: problem=sum, service=sum_and_product, numbers={ENV_numbers}, num_questions={ENV_num_questions}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

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
            x = randrange(2**32)
            y = randrange(2**32)
    TAcprint(f"? {x+y} {x*y}", "yellow", ["bold"])
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_pair = False
    if a+b > x+y:
        TAcNO() 
        print_lang("over-sum", "yellow", ["underline"])        
        #English: print(f"indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:    
        TAcNO() 
        print_lang("under-sum", "yellow", ["underline"])        
        #English: print(f"indeed, {a}+{b}={a+b} < {x+y}.")
    elif a*b > x*y:    
        TAcNO() 
        print_lang("over-product", "yellow", ["underline"])        
        #English: print(f"indeed, {a}*{b}={a*b} > {x*y}.")
    elif a*b < x*y:    
        TAcNO() 
        print_lang("under-product", "yellow", ["underline"])        
        #English: print(f"indeed, {a}*{b}={a*b} < {x*y}.")
    else:
        TAcOK() 
        assert (a + b == x+y) and (a * b == x*y)
        print_lang("ok", "grey")        
        #English: print(f"indeed, {a}+{b}={x+y} and {a}*{b}={x*y}.")
        gen_new_pair = True

TAcFinished()
exit(0)
