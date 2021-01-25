#!/usr/bin/env python3

from os import environ
import yaml
from sys import exit
from random import randrange

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]
ENV_obj = environ["TAL_obj"]
ENV_num_questions = int(environ["TAL_num_questions"])

with open("sum_server." + ENV_lang + ".yaml", 'r') as stream:
    try:
        messages_book = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def print_lang(message_code, *args,**kwargs):
  tmpstr=messages_book[message_code]
  print(eval(f"f'{tmpstr}'"),*args,**kwargs)


        
print_lang("open-channel")        
#English: print(f"# I will serve: problem=sum, service=sum, numbers={ENV_numbers}, obj={ENV_obj}, num_questions={ENV_num_questions}, lang={ENV_lang}.")

gen_new_n = True    
for _ in range(ENV_num_questions):
    if gen_new_n:
        if ENV_numbers == "onedigit":
            n = randrange(10)
        elif ENV_numbers == "twodigits":
            n = randrange(100)
        else:
            n = randrange(2**64)
    print("?", n)
    spoon = input().strip()
    while spoon[0] == '#':
        print(spoon)
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_n = False
    if a+b > n:
       print_lang("too-much")        
       #English: print(f"n indeed, {a}+{b}={a+b} > {n}.")
    elif a+b < n:    
       print_lang("too-little")        
       #English: print(f"n indeed, {a}+{b}={a+b} < {n}.")
    else: # a + b == n
        print_lang("right-sum")        
        #English: print(f"y indeed, {a}+{b}={n}")
        if ENV_obj == "max_product":
            if a < b:
                a,b = b,a
            if a-b > 1:
                print_lang("not-balanced")        
                #English: print(f"n indeed, {a-1}+{b+1}={n} and {a-1}*{b+1}={(a-1)*(b+1)} > {a*b}={a}*{b}.")
            else:
                gen_new_n = True
                print_lang("max-product")        
                #English: print(f"y indeed, x={a} and y={b} have maximum product among the integer numbers with x+y={n}. Do you know why? Do you have a proof for your intuition?")
        else:
            gen_new_n = True
            
print_lang("got-bored")        
#English: print("! (I got bored)")
exit(0)
