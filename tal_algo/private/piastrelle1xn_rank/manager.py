#!/usr/bin/env python3

from os import environ
from random import randrange
from sys import stderr
from time import time
from tc import TC
from sol import rank
from functools import lru_cache
from sys import setrecursionlimit
setrecursionlimit(10000)

DATA = ((10, (0, 10)), (10, (0, 10)), (80, (10**2, 10**3)))

TL = 1

MAPPER = {"small": 1, "medium": 2, "big": 3}


@lru_cache(maxsize=None)
def num_piastrellature(n):
    assert n >= 0
    if n <= 1:
        return 1
    return num_piastrellature(n-1) + num_piastrellature(n-2)

def unrank(n, rank):
    if n == 0:
        return ""
    if rank < num_piastrellature(n-1):
        return "[-]"+unrank(n-1, rank)
    return "[----]"+unrank(n-2, rank-num_piastrellature(n-1))

def gen_tc(a, b):
    n = randrange(a, b)
    rank = randrange(0, num_piastrellature(n))
    piast = unrank(n, rank)
    print(piast)
    return (piast,rank)


def check_tc(piast,rank):
    #print(f"Within check_tc: {rank=}, {piast=}",file=stderr)
    risp = int(input())
    if risp != rank:
        return False, f"On input:\n{piast}\nyou answered:\n{risp}\nwhile the correct answer was:\n{rank}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
