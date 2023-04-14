#!/usr/bin/env python3
from doctest import OutputChecker
import random, re, copy
from sys import exit

alphabet = '#,-0123456789<>ABCDEFGHIJKLMNOPQRSTUVWXYZ()'


def random_seq(seedParam, maxLengh):
    if seedParam=='random_seed':
        random.seed()
        seed = random.randrange(0,1000000)
        print("seed: " + str(seed))
    else:
        seed = int(seedParam)
        print("seed: " + str(seed))

    random.seed(seed)
    length = random.randint(2, maxLengh)
    sequence = []
    for i in range(length):
        sequence.append(random.randint(0, 1))
    return sequence

def getRules(text):
    text = text.upper()
    rules = {}
    i = 0
    for line in text.splitlines():
        line = line.strip()
        if(line[1] not in rules):
            rules[line[1]] = {}
        if(line[7] != "<" or line[7] != ">" or line[7] != "-"):
            raise TypeError("Movement error")
        rules[line[1]][line[3]] = [line[5], line[7], line[9], i]
        i += 1
        print(rules)
    return rules