#!/usr/bin/env python3

WARNING = """this library is common to a few problems:
../triangolo_opt_val
../triangolo_opt_sol
../triangolo_count_opt_sol
../triangolo_rank_opt_sol
../triangolo_unrank_opt_sol
Please, keep this in mind in case you want to modify it."""

from sys import stderr, stdout
from random import randrange, randint

from functools import lru_cache

def triangle_as_str(Tr):
    n = len(Tr)
    risp = str(Tr[0][0])
    for i in range(1,n):
        risp += "\n" + " ".join(map(str, Tr[i]))
    return risp

def display_triangle(Tr, out=stderr):
    print(triangle_as_str(Tr), file=out)
        
def max_val(Tr, r=0,c=0):
    #display_triangle(Tr, stderr)
    
    @lru_cache(maxsize=None)
    def max_val_ric_memo(r,c):
        assert 0 <= c <= r < n
        if r == n-1:
            #print(f"called with {r=},{c=} returns {Tr[r][c]=}", file=stderr)
            return Tr[r][c]
        risp = Tr[r][c] + max(max_val_ric_memo(r+1,c), max_val_ric_memo(r+1,c+1))
        #print(f"called with {r=},{c=} returns {risp=}", file=stderr)
        return risp

    n = len(Tr)
    return max_val_ric_memo(r,c)

def num_opt_sols(Tr, r=0,c=0):
    @lru_cache(maxsize=None)
    def num_opt_sols_ric_memo(r,c):
        assert 0 <= c <= r < n
        if r == n-1:
            return 1
        risp = 0
        if max_val(Tr, r, c) == Tr[r][c] + max_val(Tr, r+1, c):
            risp += num_opt_sols_ric_memo(r+1,c)
        if max_val(Tr, r, c) == Tr[r][c] + max_val(Tr, r+1, c+1):
            risp += num_opt_sols_ric_memo(r+1, c+1)
        return risp
    n = len(Tr)
    return num_opt_sols_ric_memo(r, c)

def opt_sol(Tr):
    n = len(Tr)
    sol = ""; r = 0; c = 0
    while r+1 < n:
        if max_val(Tr,r+1,c) >= max_val(Tr, r+1, c+1):
            sol += "L"; r += 1
        else:
            sol += "R"; r += 1; c += 1
    return sol

def unrank_safe(Tr, rnk):
    n = len(Tr)
    path = ""; c = 0
    for r in range(n-1):
        #print(f"{r=}, {c=}, {rnk=}, num_opt_sols(Tr,r,c)",file=stderr)
        assert 0 <= rnk < num_opt_sols(Tr, r, c)
        if max_val(Tr, r, c) > Tr[r][c] + max_val(Tr, r+1, c):
            path += "R"; c += 1
        else:
            assert max_val(Tr, r, c) == Tr[r][c]+max_val(Tr, r+1, c)
            if rnk < num_opt_sols(Tr, r+1, c):
                path += "L"
            else:
                rnk -= num_opt_sols(Tr, r+1, c); path += "R"; c += 1
    assert rnk == 0
    return path

def rank_safe(Tr, opt_path):
    n = len(Tr)
    rnk = 0; c = 0
    for r in range(n-1):
        if opt_path[r] == "R":
            if max_val(Tr, r, c) == Tr[r][c] + max_val(Tr, r+1, c):
                rnk += num_opt_sols(Tr, r+1, c)
            c += 1
    return rnk

def rank_unsafe(Tr, path, stated_opt_val):
    ok,val_of_path = eval_sol_unsafe(Tr, path)
    if not ok:
        return False, val_of_sol
    if stated_opt_val != val_of_path:
        return False, f"On input:\n{triangle_as_str(Tr)}\nyou claimed that {stated_opt_val} is the optimum value of a solution. However, you then provided a solution whose value is {val_of_path} rather then {stated_opt_val}.\nThe solution you have provided is:\n{path}"
    opt_val = max_val(Tr)
    assert val_of_path <= opt_val
    if val_of_path < opt_val:
        return False, f"On input:\n{triangle_as_str(Tr)}\nyou claimed that {val_of_path} is the optimal value. However, the optimal value is {opt_val}.\nIndeed, consider the following descending path:\n{opt_sol(Tr)}"
    n = len(Tr)
    rnk = 0; c = 0
    for r in range(n-1):
        if path[r] == "R":
            if max_val(Tr, r, c) == Tr[r][c] + max_val(Tr, r+1, c):
                rnk += num_opt_sols(Tr, r+1, c)
            c += 1
    return True, rnk

def eval_sol_unsafe(Tr, sol):
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


if __name__ == "__main__":
    print(WARNING)    
    
