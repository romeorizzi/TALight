#!/usr/bin/env python3

from os import environ
import yaml
from sys import exit
from random import randrange

TC = 10

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]

with open("sum_and_difference_server." + ENV_lang + ".yaml", 'r') as stream:
    try:
        api = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

tmpstr=api["open-channel"]
print(eval(f"f'{tmpstr}'"))
#print(f"# I will serve: problem=sum, service=sum_and_difference, numbers={ENV_numbers}, lang={ENV_lang}.")

gen_new_pair = True    
for _ in range(TC):
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
       tmpstr=api["over-sum"]
       print(eval(f"f'{tmpstr}'"))
       #print(f"n indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:    
       tmpstr=api["under-sum"]
       print(eval(f"f'{tmpstr}'"))
       #print(f"n indeed, {a}+{b}={a+b} < {x+y}.")
    elif abs(a-b) > x-y:    
        tmpstr=api["too-apart"]
        print(eval(f"f'{tmpstr}'"))
        #print(f"n indeed, |{a}-{b}|={abs(a-b)} > {x-y}.")
    elif abs(a-b) < x-y:    
        tmpstr=api["too-close"]
        print(eval(f"f'{tmpstr}'"))
        #print(f"n indeed, |{a}-{b}|={abs(a-b)} < {x-y}.")
    else:
        assert (a + b == x+y) and (abs(a-b) == x-y)
        tmpstr=api["ok"]
        print(eval(f"f'{tmpstr}'"))
        #print(f"y indeed, {a}+{b} = {x+y} and |{a}-{b}| = {x-y}.")
        gen_new_pair = True

tmpstr=api["got-bored"]
print(eval(f"f'{tmpstr}'"))
#print("! (I got bored)")
exit(0)
