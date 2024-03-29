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
    Tr = Triangolo([[randint(0, 9) for j in range(i+1)] for i in range(n)])
    Tr.display(stdout)
    return (Tr,)

def check_tc(Tr):
    risp_val = int(input())
    risp_sol = input().strip()
    ok, val_of_risp_sol = Tr.eval_sol_unsafe(risp_sol)
    if not ok:
        return False, val_of_risp_sol
    if val_of_risp_sol != risp_val:
        return False, f"On input:\n{Tr.as_str()}\nyou claimed that {risp_val} is the optimal value. However, you returned a feasible solution of value {val_of_risp_sol}, namely:\n{risp_sol}"
    opt_val = Tr.max_val_ric_memo()
    assert risp_val <= opt_val
    if risp_val < opt_val:
        return False, f"On input:\n{Tr.as_str()}\nyou claimed that {risp_val} is the optimal value. However, the optimal value is {opt_val}.\nIndeed, consider the following descending path:\n{Tr.opt_sol()}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
