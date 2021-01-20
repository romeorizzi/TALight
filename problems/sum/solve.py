#!/usr/bin/env python3

from os import environ
from sys import exit
from random import randrange

TC = 20

small = environ["TAL_subtask"] == "small"

if small:
    print("I will serve: sum solve small")
else:
    print("I will serve: sum solve big")
gen_new_n = True    
for _ in range(TC):
    if gen_new_n:
        if small:
            n = randrange(10**2)
        else:
            n = randrange(2**64)
    print("?", n)
    spoon = input().strip()
    while spoon[0] == '#':
        print(spoon)
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    if a + b == n:
        print(f"y indeed, {a}+{b}={n}")
        gen_new_n = True
    else:
        gen_new_n = False
        if a+b > n:
           print(f"n indeed, {a}+{b}={a+b} > {n}!")
        else:    
           print(f"n indeed, {a}+{b}={a+b} < {n}!")
print("! (I got bored)")
exit(1)
