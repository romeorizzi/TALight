#!/usr/bin/env python3
from doctest import OutputChecker
import random, re, copy
from sys import exit

def random_seq(seedParam):
    if seedParam=='random_seed':
        random.seed()
        seed = random.randrange(0,1000000)
        print(seed)
    else:
        seed = int(seedParam)
        print(seed)

    random.seed(seed)
    length = random.randint(1, 20)
    sequence = []
    for i in range(length):
        sequence.append(random.randint(0, 1))
    return sequence