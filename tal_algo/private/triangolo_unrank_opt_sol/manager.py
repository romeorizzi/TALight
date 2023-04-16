#!/usr/bin/env python3
from sys import stderr, stdout
from os import environ
from random import randrange, randint

from tc import TC

from triangolo_lib import triangle_as_str, display_triangle, max_val, opt_sol, eval_sol_unsafe, num_opt_sols, rank_unsafe, unrank_safe

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "big": 4}
DATA = ((10, (5,6)), (10, (8,10)), (10, (18,20)), (70, (30,40)))
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
#################################################################


def gen_tc(min_n,max_n):
    n = randint(min_n, max_n)
    Tr = [[randint(0, 9) for j in range(i+1)] for i in range(n)]
    rnk = randrange(num_opt_sols(Tr))
    print(n,rnk)
    display_triangle(Tr,stdout)
    return (Tr,rnk)

def check_tc(Tr,rnk):
    risp_val = int(input())
    risp_sol = input().strip()
    ok, rank_of_risp = rank_unsafe(Tr,risp_sol,risp_val)
    if not ok:
        return False,rank_of_risp
    if rank_of_risp != rnk:
        return False, f"On input:\n{len(Tr)} {rnk}\n{triangle_as_str(Tr)}\nyou were right in stating that the optimum value of a solution is {risp_val}. However, you then returned the optimal solution:\n{risp_sol}\nwhich is of rank {rank_of_risp}. Instead, the optimal solution of rank {rnk}, as required, was:\n{unrank_safe(Tr,rnk)}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
