#!/usr/bin/env python3
from sys import stderr, stdout
from os import environ
from random import randrange, randint
from functools import lru_cache

from tc import TC

from triangolo_lib import triangle_as_str, display_triangle, game_val

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "big": 4}
DATA = ((10, (5, 7)), (10, (8, 10)), (10, (25, 28)), (70, (30, 40)))
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
#################################################################


def gen_tc(min_n, max_n):
    n = randint(min_n, max_n)
    Tr = [[randint(0, 9) for j in range(i+1)] for i in range(n)]
    print(n)
    chooser = [randint(0,1) for _ in range(n-1)]
    print(" ".join(map(str, chooser)))
    display_triangle(Tr, stdout)
    return (Tr, chooser)

def check_tc(Tr, chooser):
    risp = int(input())
    corr_answ = game_val(Tr, chooser)
    if risp != corr_answ:
        return False, f"On input:\n{len(Tr)}\n{chooser}\n{triangle_as_str(Tr)}\nyou answered:\n{risp}\nwhile the correct answer for the value of the game was:\n{corr_answ}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
