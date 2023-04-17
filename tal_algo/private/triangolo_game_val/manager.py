#!/usr/bin/env python3
from sys import stderr, stdout
from os import environ
from random import randrange, randint
from functools import lru_cache

from tc import TC

from triangolo_lib import Triangolo

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "big": 4}
DATA = ((10, (5, 7)), (10, (8, 10)), (10, (25, 28)), (70, (30, 40)))
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
#################################################################


def gen_tc(min_n, max_n):
    n = randint(min_n, max_n)
    Tr = Triangolo(T = [[randint(0, 9) for j in range(i+1)] for i in range(n)], chooser = [randint(0, 1) for _ in range(n-1)], game = True)
    Tr.display(stdout)
    return (Tr,)

def check_tc(Tr):
    risp_val = int(input())
    corr_val = Tr.game_val_ric_memo()
    #print(f"{corr_val=}, {risp_val=}", file=stderr)
    if risp_val != corr_val:
        return False, f"On input:\n{Tr.as_str()}\nyou answered:\n{risp_val}\nwhile the correct answer for the value of the game was:\n{corr_val}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
