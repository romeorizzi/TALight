#!/usr/bin/env python3
from sys import stderr
from functools import lru_cache

def display_triangle(Tr,out=stderr):
    n = len(Tr)
    for i in range(n):
        print(" ".join(map(str,Tr[i])), file=out)


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

def num_opt_sols(Tr, r=0,c=0):
    @lru_cache(maxsize=None)
    def num_opt_sols_ric_memo(r,c):
        assert 0 <= c <= r < n
        if r == n-1:
            return 1
        risp = 0
        if max_val(Tr, r,c) == Tr[r][c] + max_val(Tr, r+1,c):
            risp += num_opt_sols_ric_memo(r+1,c)
        if max_val(Tr, r,c) == Tr[r][c] + max_val(Tr, r+1,c+1):
            risp += num_opt_sols_ric_memo(r+1,c+1)
        return risp
    n = len(Tr)
    return num_opt_sols_ric_memo(r,c)

def opt_sol(Tr):
    n = len(Tr)
    sol = ""; r = 0; c = 0
    while r+1 < n:
        if max_val(Tr,r+1,c) >= max_val(Tr,r+1,c+1):
            sol += "L"; r += 1
        else:
            sol += "R"; r += 1; c += 1
    return sol

def unrank(Tr,rnk):
    n = len(Tr)
    sol = ""; c = 0
    for r in range(n-1):
        #print(f"{r=}, {c=}, {rnk=}, {num_opt_sols(Tr,r,c)=}",file=stderr)
        assert 0 <= rnk < num_opt_sols(Tr,r,c)
        if max_val(Tr, r,c) > Tr[r][c] + max_val(Tr,r+1,c):
            sol += "R"; c += 1
        else:
            assert max_val(Tr, r,c) == Tr[r][c]+max_val(Tr,r+1,c)
            if rnk < num_opt_sols(Tr,r+1,c):
                sol += "L"
            else:
                rnk -= num_opt_sols(Tr,r+1,c); sol += "R"; c += 1
    assert rnk == 0
    return sol

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        #print(f"testcase {t}",file=stderr)
        n,rnk = map(int,input().strip().split())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr,stderr)
        print(max_val(Tr))
        print(unrank(Tr,rnk))
