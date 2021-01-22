#!/usr/bin/env python3

from os import environ
from sys import exit
from random import randrange

TC = 20

print(f"# I will serve: problem=sum, service=sum_and_product, numbers={environ['TAL_numbers']}")

gen_new_pair = True    
for _ in range(TC):
    if gen_new_pair:
        if environ["TAL_numbers"] == "onedigit":
            x = randrange(10)
            y = randrange(10)
        elif environ["TAL_numbers"] == "twodigits":
            x = randrange(100)
            y = randrange(100)
        else:
            x = randrange(2**32)
            y = randrange(2**32)
    print("?", x+y, x*y)
    spoon = input().strip()
    while spoon[0] == '#':
        print(spoon)
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_pair = False
    if a+b > x+y:
       print(f"n indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:    
       print(f"n indeed, {a}+{b}={a+b} < {x+y}.")
    elif a*b < x*y:    
       print(f"n indeed, {a}*{b}={a*b} < {x*y}.")
    elif a*b > x*y:    
       print(f"n indeed, {a}*{b}={a*b} > {x*y}.")
    else:
        assert (a + b == x+y) and (a * b == x*y)
        print(f"y indeed, {a}+{b}={x+y} and {a}*{b}={x*y}.")
        gen_new_pair = True

print("! (I got bored)")
exit(1)
