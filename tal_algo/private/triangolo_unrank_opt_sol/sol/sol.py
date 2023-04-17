#!/usr/bin/env python3
from sys import stderr
from functools import lru_cache

def display_triangle(Tr,out=stderr):
    for i in range(n):
        print(" ".join(map(str, Tr[i])), file=out)


@lru_cache(maxsize=None)
def max_val_ric_memo(r=0, c=0):
    assert 0 <= c <= r <= n
    if r == n:
        return 0
    return Tr[r][c] + max(max_val_ric_memo(r+1, c), max_val_ric_memo(r+1, c+1))

@lru_cache(maxsize=None)
def num_opt_sols_ric_memo(r=0, c=0):
    assert 0 <= c <= r < n
    if r == n-1:
        return 1
    risp = 0
    if max_val_ric_memo(r, c) == Tr[r][c] + max_val_ric_memo(r+1, c):
        risp += num_opt_sols_ric_memo(r+1,c)
    if max_val_ric_memo(r, c) == Tr[r][c] + max_val_ric_memo(r+1, c+1):
        risp += num_opt_sols_ric_memo(r+1, c+1)
    return risp

def unrank(rnk):
    sol = ""; c = 0
    for r in range(n-1):
        #print(f"{r=}, {c=}, {rnk=}, {num_opt_sols_ric_memo(r,c)=}",file=stderr)
        assert 0 <= rnk < num_opt_sols_ric_memo(r, c)
        if max_val_ric_memo(r, c) > Tr[r][c] + max_val_ric_memo(r+1, c):
            sol += "R"; c += 1
        else:
            assert max_val_ric_memo(r, c) == Tr[r][c] + max_val_ric_memo(r+1, c)
            if rnk < num_opt_sols_ric_memo(r+1, c):
                sol += "L"
            else:
                rnk -= num_opt_sols_ric_memo(r+1, c); sol += "R"; c += 1
    assert rnk == 0
    return sol

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        #print(f"testcase {t}", file=stderr)
        n,rnk = map(int,input().strip().split())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int, input().strip().split())))
        #display_triangle(Tr, stderr)
        print(max_val_ric_memo())
        print(unrank(rnk))
        max_val_ric_memo.cache_clear()
        num_opt_sols_ric_memo.cache_clear()
