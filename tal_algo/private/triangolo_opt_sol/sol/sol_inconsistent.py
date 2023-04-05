#!/usr/bin/env python3
from sys import stderr
from random import randrange
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

def opt_sol(Tr):
    n = len(Tr)
    sol = ""; r = 0; c = 0
    while r+1 < n:
        if max_val(Tr,r+1,c) >= max_val(Tr,r+1,c+1):
            sol += "L"; r += 1
        else:
            sol += "R"; r += 1; c += 1
    return sol

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        #print(f"testcase {t}",file=stderr)
        n = int(input())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr,stderr)
        optv = max_val(Tr)
        opts = opt_sol(Tr)
        dice = randrange(0,6)
        if dice == 0:
            print(optv-1)
            print(opts)
        elif dice == 1:
            print(optv+1)
            print(opts)
        elif dice == 2:
            print(optv)
            print(opts[1:] + 'L' if opts[0]=='R' else 'R')
        else:
            print(optv)
            print(opts)
