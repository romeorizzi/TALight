#!/usr/bin/env python3

from functools import lru_cache
from os import environ
from random import randrange, randint
from tc import TC
from sys import setrecursionlimit, stderr

DATA = ((10, (8, 20)), (30, (24, 10**6)), (10, (50, 10**6)))

TL = 5

MAPPER = {"small": 1, "big": 3}


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


def gen_tc(n, maxv):
    V = [randrange(0, maxv) for i in range(n)]
    if sum(V) % 2:
        V[randrange(0, n)] += 1
    print(n)
    print(*V)
    return (V,)


def check_tc(V):
    p = 1 - int(input())
    assert p in (0, 1)
    t = 0
    i = 0
    j = len(V)
    f = sol(V)
    score = [0, 0]
    while i < j:
        if p == t:
            if f(i, j)[1] == "L":
                print("L", flush=True)
                score[t] += V[i]
                i += 1
            else:
                print("R", flush=True)
                j -= 1
                score[t] += V[j]
        else:
            if input().strip() == "L":
                score[t] += V[i]
                i += 1
            else:
                j -= 1
                score[t] += V[j]
        t = 1 - t
    return score[1 - p] > score[p]


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
