#!/usr/bin/env python3
from functools import lru_cache
from sys import stderr,setrecursionlimit
setrecursionlimit(10000)

@lru_cache(maxsize=None)
def num_piastrellature(n):
    assert n >= 0
    if n <= 1:
        return 1
    return num_piastrellature(n-1) + num_piastrellature(n-2)

def rank(piast):
    if piast == "":
        return 0
    if piast[:3] == "[-]":
        return rank(piast[3:])
    assert piast[:6] == "[----]"
    n = len(piast)/3
    return num_piastrellature(n-1) + rank(piast[6:])

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        piast = input().strip()
        print(f"{piast=}",file=stderr)
        print(rank(piast))
