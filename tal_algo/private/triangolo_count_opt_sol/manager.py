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
    risp_num_opt_sols = int(input())
    opt_val = Tr.max_val_ric_memo()
    if risp_val < opt_val:
        return False, f"On input:\n{Tr.as_str()}\nyou claimed that {risp_val} is the optimal value. However, the optimal value is {opt_val}.\nIndeed, consider the following descending path:\n{opt_sol(Tr)}"
    if risp_val != opt_val:
        return False, f"On input:\n{Tr.as_str()}\nyou claimed that {risp_val} is the optimal value. However, the optimal value is {opt_val}."
    corr_num_opt_sols = Tr.num_opt_sols_ric_memo()
    if risp_num_opt_sols != corr_num_opt_sols:
        return False, f"On input:\n{Tr.as_str()}\nyou claimed that the number of optimal solutions (of value {risp_val}) is {risp_num_opt_sols}. However, the correct number of optimal solutions is {corr_num_opt_sols}."
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
