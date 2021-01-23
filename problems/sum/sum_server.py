#!/usr/bin/env python3

from os import environ
import yaml
from sys import exit
from random import randrange

TC = 10

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]
ENV_obj = environ["TAL_obj"]

with open("sum_server." + ENV_lang + ".yaml", 'r') as stream:
    try:
        api = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

tmpstr=api["open-channel"]
print(eval(f"f'{tmpstr}'"))
#print(f"# I will serve: problem=sum, service=sum, numbers={ENV_numbers}, obj={ENV_obj}, lang={ENV_lang}.")

gen_new_n = True    
for _ in range(TC):
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
       tmpstr=api["too-much"]
       print(eval(f"f'{tmpstr}'"))
       #print(f"n indeed, {a}+{b}={a+b} > {n}.")
    elif a+b < n:    
       tmpstr=api["too-little"]
       print(eval(f"f'{tmpstr}'"))
       #print(f"n indeed, {a}+{b}={a+b} < {n}.")
    else: # a + b == n
        tmpstr=api["right-sum"]
        print(eval(f"f'{tmpstr}'"))
        #print(f"y indeed, {a}+{b}={n}")
        if ENV_obj == "max_product":
            if a < b:
                a,b = b,a
            if a-b > 1:
                tmpstr=api["not-balanced"]
                print(eval(f"f'{tmpstr}'"))
                #print(f"n indeed, {a-1}+{b+1}={n} and {a-1}*{b+1}={(a-1)*(b+1)} > {a*b}={a}*{b}.")
            else:
                gen_new_n = True
                tmpstr=api["max-product"]
                print(eval(f"f'{tmpstr}'"))
                #print(f"y indeed, x={a} and y={b} have maximum product among the integer numbers with x+y={n}. Do you know why? Do you have a proof for your intuition?")
        else:
            gen_new_n = True
            
tmpstr=api["got-bored"]
print(eval(f"f'{tmpstr}'"))
#print("! (I got bored)")
exit(0)
