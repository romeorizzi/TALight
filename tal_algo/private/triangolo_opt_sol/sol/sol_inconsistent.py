#!/usr/bin/env python3
from sys import stderr
from random import randrange
from functools import lru_cache

def display_triangle(Tr, out=stderr):
    for i in range(n):
        print(" ".join(map(str, Tr[i])), file=out)


@lru_cache(maxsize=None)
def max_val_ric_memo(r=0, c=0):
    assert 0 <= c <= r <= n
    if r == n:
        return 0
    return Tr[r][c] + max(max_val_ric_memo(r+1, c), max_val_ric_memo(r+1, c+1))


def opt_sol():
    sol = ""; r = 0; c = 0
    while r+1 < n:
        if max_val_ric_memo(r+1, c) >= max_val_ric_memo(r+1, c+1):
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
        optv = max_val_ric_memo()
        opts = opt_sol()
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
