#!/usr/bin/env python3

from os import environ
from sys import exit
from random import randrange

TC = 20

small = environ["TAL_numbers"] == "small"
max_product = environ["TAL_obj"] == "max_product"

print(f"# I will serve: problem=sum, service=sum, numbers={environ['TAL_numbers']}, obj={environ['TAL_obj']}")

gen_new_n = True    
for _ in range(TC):
    if gen_new_n:
        if environ["TAL_numbers"] == "onedigit":
            n = randrange(10)
        elif environ["TAL_numbers"] == "twodigits":
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
       print(f"n indeed, {a}+{b}={a+b} > {n}.")
    elif a+b < n:    
       print(f"n indeed, {a}+{b}={a+b} < {n}.")
    else: # a + b == n
        print(f"y indeed, {a}+{b}={n}")
        if max_product:
            if a < b:
                a,b = b,a
            if a-b > 1:
                print(f"n indeed, {a-1}+{b+1}={n} and {a-1}*{b+1}={(a-1)*(b+1)} > {a*b}={a}*{b}.")
            else:
                gen_new_n = True
                print(f"y indeed, x={a} and y={b} have maximum product among the integer numbers with x+y={n}. Do you know why? Do you have a proof for your intuition?")
        else:
            gen_new_n = True
print("! (I got bored)")
exit(1)
