#!/usr/bin/env python3
from sys import stderr, stdout
from os import environ
from random import randrange, randint

from tc import TC

from triangolo_lib import triangle_as_str, display_triangle, max_val, opt_sol, eval_sol_unsafe, num_opt_sols, rank_unsafe, unrank_safe

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
    rnk_path = randrange(num_opt_sols(Tr))
    one_opt_path = unrank_safe(Tr, rnk_path)
    print(one_opt_path)
    display_triangle(Tr, stdout)
    return (Tr, one_opt_path, rnk_path)

def check_tc(Tr, opt_path_given, rnk_path):
    risp_val = int(input())
    risp_num_opts = int(input())
    risp_rnk = int(input())
    opt_val = max_val(Tr)
    if risp_val > opt_val:
        return False, f"On input:\n{len(Tr)}\n{triangle_as_str(Tr)}\nyou returned {risp_val} instead of {opt_val} as the optimal value of a path."
    if risp_val < opt_val:
        return False, f"On input:\n{len(Tr)}\n{triangle_as_str(Tr)}\nyou returned {risp_val} as the optimal value of a path. However, here is a path of value {opt_val}:\n{opt_sol(Tr)}"
    if risp_num_opts != num_opt_sols(Tr):
        return False, f"On input:\n{len(Tr)}\n{triangle_as_str(Tr)}\nyou were right in stating that the optimum value of a solution is {risp_val}. However, you then returned {risp_num_opts} instead of {num_opt_sols(Tr)} as the number of optimal paths."
    if not 0 <= risp_rnk < risp_num_opts:
        return False, f"On input:\n{len(Tr)}\n{triangle_as_str(Tr)}\nyou were right in stating that the optimum value of a solution is {risp_val}, and also in stating that the number of optimal paths is {risp_num_opts}. However, you then returned {risp_rnk} as the rank of the optimal descending path path:\n{opt_path_given}\nClearly, this is an inconsistency since the rank should have then been an integer in the semi-closed interval [0,{risp_num_opts})."
    if risp_rnk != rnk_path:
        return False, f"On input:\n{len(Tr)} {rnk_path}\n{triangle_as_str(Tr)}\nyou were right in stating that the optimum value of a solution is {risp_val}, and also in stating that the number of optimal paths is {risp_num_opts}. However, you then returned {risp_rnk} as the rank of the optimal descending path path:\n{opt_path_given}\nHowever, the correct rank of this optimal path is {rnk_path}."
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
