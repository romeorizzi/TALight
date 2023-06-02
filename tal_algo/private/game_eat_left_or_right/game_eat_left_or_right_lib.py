#!/usr/bin/env python3
from sys import setrecursionlimit, stderr
from functools import lru_cache

def sol(V):
    setrecursionlimit(10**6)
    n = len(V)
    p = [0] * (n + 1)
    for i in range(n):
        p[i + 1] = p[i] + V[i]

    @lru_cache(maxsize=None)
    def f(i, j):
        if i == j:
            return (0, None)
        l = f(i + 1, j)
        r = f(i, j - 1)
        if l[0] < r[0]:
            return (p[j] - p[i] - l[0], "L")
        else:
            return (p[j] - p[i] - r[0], "R")

    return f


