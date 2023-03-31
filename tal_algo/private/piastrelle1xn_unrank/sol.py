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

def unrank(n, rank):
    if n == 0:
        return ""
    if rank < num_piastrellature(n-1):
        return "[-]"+unrank(n-1, rank)
    return "[----]"+unrank(n-2, rank-num_piastrellature(n-1))

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n, rank = map(int, input().strip().split())
        print(unrank(n, rank))
