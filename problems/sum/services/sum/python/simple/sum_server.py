#!/usr/bin/env python3

from os import environ
from sys import exit
from random import randrange

ENV.numbers = environ["TAL_numbers"]
ENV.obj = environ["TAL_obj"]
ENV.num_questions = int(environ["TAL_num_questions"])

print(f"# I will serve: problem=sum, service=sum, numbers={ENV.numbers}, obj={ENV.obj}, num_questions={ENV.num_questions}.")

gen_new_s = True    
for _ in range(ENV.num_questions):
    if gen_new_s:
        if ENV.numbers == "onedigit":
            s = randrange(10)
        elif ENV.numbers == "twodigits":
            s = randrange(100)
        else:
            s = randrange(2**64)
    print(f"? {s}")
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_s = False
    if a+b > s:
        print(f"No! indeed, {a}+{b}={a+b} > {s}.")
    elif a+b < s:
        print(f"No! indeed, {a}+{b}={a+b} < {s}.")
    else: # a + b == n
        if ENV.obj == "max_product":
            if a < b:
                a,b = b,a
            if a-b > 1:
                print(f"No! indeed, {a-1}+{b+1}={s} and {a-1}*{b+1}={(a-1)*(b+1)} > {a*b}={a}*{b}.")
            else:
                gen_new_s = True
                print(f"Ok! indeed, x={a} and y={b} have maximum product among the integer numbers with x+y={s}. Do you know why? Do you have a proof for your intuition?")
        else:
            print(f"Ok! indeed, {a}+{b}={s}")
            gen_new_s = True
            
exit(0)
