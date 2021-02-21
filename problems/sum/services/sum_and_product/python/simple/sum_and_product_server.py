#!/usr/bin/env python3

from os import environ
from sys import stderr, exit
from random import randrange

ENV['numbers'] = environ["TAL_numbers"]
ENV['num_questions'] = int(environ["TAL_num_questions"])

print(f"# I will serve: problem=sum, service=sum_and_product, numbers={ENV['numbers']}, num_questions={ENV['num_questions']}.")

gen_new_pair = True    
for _ in range(ENV['num_questions']):
    if gen_new_pair:
        if ENV['numbers'] == "onedigit":
            x = randrange(10)
            y = randrange(10)
        elif ENV['numbers'] == "twodigits":
            x = randrange(100)
            y = randrange(100)
        else:
            x = randrange(2**32)
            y = randrange(2**32)
    print(f"? {x+y} {x*y}")
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_pair = False
    if a+b > x+y:
        print(f"No! indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:    
        print(f"No! indeed, {a}+{b}={a+b} < {x+y}.")
    elif a*b > x*y:    
        print(f"No! indeed, {a}*{b}={a*b} > {x*y}.")
    elif a*b < x*y:    
        print(f"No! indeed, {a}*{b}={a*b} < {x*y}.")
    else:
        assert (a + b == x+y) and (a * b == x*y)
        print(f"Ok! indeed, {a}+{b}={x+y} and {a}*{b}={x*y}.")
        gen_new_pair = True

exit(0)
