#!/usr/bin/env python3
from sys import stderr, stdout
from os import environ
from random import randrange, randint

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
    rnk = randrange(Tr.num_opt_sols_ric_memo())
    print(rnk)
    return (Tr, rnk)

def check_tc(Tr, rnk):
    risp_val = int(input())
    risp_sol = input().strip()
    ok, rank_of_risp = Tr.rank_unsafe(risp_sol, risp_val)
    if not ok:
        return False, rank_of_risp
    if rank_of_risp != rnk:
        return False, f"On input:\n{Tr.n} {rnk}\n{Tr.as_str(with_n = False)}\nyou were right in stating that the optimum value of a solution is {risp_val}. However, you then returned the optimal solution:\n{risp_sol}\nwhich is of rank {rank_of_risp}. Instead, the optimal solution of rank {rnk}, as required, was:\n{Tr.unrank_safe(rnk)}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
