#!/usr/bin/env python3

from os import environ
from random import randrange

ENV_num_rounds = int(environ["TAL_num_rounds"])

print(f"# I will serve: problem=infinity_of_N, service=bigger_and_bigger, num_rounds={ENV_num_rounds}.")

my_n = randrange(20)
for _ in range(ENV_num_rounds):
    print(my_n)
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    your_n = int(spoon)
    if your_n <= my_n:
        print(f"You just replied with {your_n} to {my_n}. Since {your_n} <= {my_n} I assume you have given up. I won!")
        exit(0)
    my_n = your_n + 1 + randrange(3+ your_n//3)    
    while randrange(6) == 0:
        my_n = my_n ** (1+randrange(6)) 

print(f"! I give up. You won!")    
exit(0)
