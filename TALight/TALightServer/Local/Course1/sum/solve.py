#!/usr/bin/env python3

from os import environ
from sys import exit
from random import randrange

TC = 100

small = environ["TAL_subtask"] == "small"

for _ in range(TC):
    if small:
        n = randrange(10**2)
    else:
        n = randrange(2**64)
    
    print("?", n)
    
    a, b = map(int, input().strip().split(" "))

    if a + b != n:
        exit(1)

print("!")
