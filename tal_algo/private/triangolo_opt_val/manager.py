#!/usr/bin/env python3

from functools import lru_cache
from os import environ
from random import randrange, randint
from tc import TC
from sol import max_val

DATA = ((10, (10,)), (10, (20,)), (80, (100,)))

TL = 1

MAPPER = {"small": 1, "medium": 2, "big": 3}


def triangle_as_str(Tr):
    n = len(Tr)
    risp = str(Tr[0][0])
    for i in range(1,n):
        risp += "\n" + " ".join(map(str,Tr[i]))
    return risp

def display_triangle(Tr):
    print(triangle_as_str(Tr))
        
def gen_tc(maxn):
    n = randint(1, maxn)
    Tr = [[randint(0, 9) for j in range(i+1)] for i in range(n)]
    print(n)
    display_triangle(Tr)
    return (Tr,)


def check_tc(Tr):
    risp = int(input().strip())
    corr_answ = max_val(Tr)
    if risp != corr_answ:
        return False, f"On input:\n{triangle_as_str(Tr)}\nyou answered:\n{risp}\nwhile the correct answer was:\n{corr_answ}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
