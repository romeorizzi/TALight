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


def eval_sol_unsafe(sol):
    assert len(sol) == n-1
    r = 0; c = 0
    val_sol = Tr[r][c]
    while r+1 < n:
        assert sol[r] in {'L','R'}
        if sol[r] == 'R':
            c += 1
        r += 1
        val_sol += Tr[r][c]
    return val_sol


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        #print(f"testcase {t}",file=stderr)
        n = int(input())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int, input().strip().split())))
        #display_triangle(Tr,stderr)
        opt_val = max_val_ric_memo()
        opt_sol = opt_sol()
        dice = randrange(0, 6)
        if dice == 0:
            opt_sol = opt_sol[1:] + ('L' if opt_sol[0]=='R' else 'R')
            opt_val = eval_sol_unsafe(opt_sol)
        elif dice == 1:
            opt_sol = opt_sol[:-1] + ('L' if opt_sol[-1]=='R' else 'R')
            opt_val = eval_sol_unsafe(opt_sol)
        print(opt_val)
        print(opt_sol)
        max_val_ric_memo.cache_clear()
