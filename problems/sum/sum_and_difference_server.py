#!/usr/bin/env python3

from os import environ
import yaml
from sys import exit
from random import randrange

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]
ENV_num_questions = int(environ["TAL_num_questions"])

with open("sum_and_difference_server." + ENV_lang + ".yaml", 'r') as stream:
    try:
        messages_book = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def print_lang(message_code, *args,**kwargs):
  tmpstr=messages_book[message_code]
  print(eval(f"f'{tmpstr}'"),*args,**kwargs)



print_lang("open-channel")        
#English: print(f"# I will serve: problem=sum, service=sum_and_difference, numbers={ENV_numbers}, num_questions={ENV_num_questions}, lang={ENV_lang}.")

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
    print("?", x+y, x-y)
    spoon = input().strip()
    while spoon[0] == '#':
        print(spoon)
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_pair = False
    if a+b > x+y:
       print_lang("over-sum")        
       #English: print(f"n indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:    
       print_lang("under-sum")        
       #English: print(f"n indeed, {a}+{b}={a+b} < {x+y}.")
    elif abs(a-b) > x-y:    
        print_lang("too-apart")        
        #English: print(f"n indeed, |{a}-{b}|={abs(a-b)} > {x-y}.")
    elif abs(a-b) < x-y:    
        print_lang("too-close")        
        #English: print(f"n indeed, |{a}-{b}|={abs(a-b)} < {x-y}.")
    else:
        assert (a + b == x+y) and (abs(a-b) == x-y)
        print_lang("ok")        
        #English: print(f"y indeed, {a}+{b} = {x+y} and |{a}-{b}| = {x-y}.")
        gen_new_pair = True

print_lang("got-bored")        
#English: print("! (I got bored)")
exit(0)
