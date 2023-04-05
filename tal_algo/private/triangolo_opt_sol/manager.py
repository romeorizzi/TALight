#!/usr/bin/env python3
from sys import stderr,stdout
from os import environ
from random import randrange, randint

from tc import TC

from functools import lru_cache

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "big": 4}
DATA = ((10, (5,6)), (10, (8,10)), (10, (18,20)), (70, (50,100)))
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
#################################################################

def triangle_as_str(Tr):
    n = len(Tr)
    risp = str(Tr[0][0])
    for i in range(1,n):
        risp += "\n" + " ".join(map(str,Tr[i]))
    return risp

def display_triangle(Tr,out=stderr):
    print(triangle_as_str(Tr), file=out)
        
def gen_tc(min_n,max_n):
    n = randint(min_n, max_n)
    Tr = [[randint(0, 9) for j in range(i+1)] for i in range(n)]
    print(n)
    display_triangle(Tr,stdout)
    return (Tr,)

def max_val(Tr, r=0,c=0):
    #display_triangle(Tr,stderr)
    
    @lru_cache(maxsize=None)
    def max_val_ric_memo(r,c):
        assert 0 <= c <= r < n
        if r == n-1:
            #print(f"called with {r=},{c=} returns {Tr[r][c]=}", file=stderr)
            return Tr[r][c]
        risp = Tr[r][c] + max(max_val_ric_memo(r+1,c),max_val_ric_memo(r+1,c+1))
        #print(f"called with {r=},{c=} returns {risp=}", file=stderr)
        return risp

    n = len(Tr)
    return max_val_ric_memo(r,c)

def opt_sol(Tr):
    n = len(Tr)
    sol = ""; r = 0; c = 0
    while r+1 < n:
        if max_val(Tr,r+1,c) >= max_val(Tr,r+1,c+1):
            sol += "L"; r += 1
        else:
            sol += "R"; r += 1; c += 1
    return sol

def eval_sol(Tr,sol):
    n = len(Tr)
    if len(sol) != n-1:
        return False, f"Your solution:\n{sol}\n has length {len(sol)}. We were expecting a string of length {n-1=} over the alphabet {{'L','R'}} as the input triangle had {n=} rows."
    r = 0; c = 0
    val_sol = Tr[r][c]
    while r+1 < n:
        if sol[r] not in {'L','R'}:
            return False, f"Your solution:\n{sol}\n contains the character '{sol[r]}' in position {r} while we were expecting a string over the alphabet {{'L','R'}}."
        if sol[r] == 'R':
            c += 1
        r += 1
        val_sol += Tr[r][c]
    return True, val_sol

def check_tc(Tr):
    risp_val = int(input())
    risp_sol = input().strip()
    ok,val_of_risp_sol = eval_sol(Tr,risp_sol)
    if not ok:
        return False,val_of_risp_sol
    if val_of_risp_sol != risp_val:
        return False, f"On input:\n{triangle_as_str(Tr)}\nyou claimed that {risp_val} is the optimal value. However, you returned a feasible solution of value {val_of_risp_sol}, namely:\n{risp_sol}"
    opt_val = max_val(Tr)
    assert risp_val <= opt_val
    if risp_val < opt_val:
        return False, f"On input:\n{triangle_as_str(Tr)}\nyou claimed that {risp_val} is the optimal value. However, the optimal value is {opt_val}.\nIndeed, consider the following descending path:\n{opt_sol(Tr)}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
