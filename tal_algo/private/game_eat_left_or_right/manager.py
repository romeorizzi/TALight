#!/usr/bin/env python3
from os import environ
from sys import setrecursionlimit, stderr
from random import randrange, randint
from functools import lru_cache

from tc import TC

TL = 1

DATA = ((10, (6,)), (10, (20,)), (20, (100,)))

MAPPER = {"small": 1, "medium": 2, "big": 3}


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


def gen_tc(n):
    V = [randrange(0, 10**5) for i in range(n)]
    if sum(V) % 2:
        V[randrange(0, n)] += 1
    print(n, file = stderr)
    print(n)
    print(*V, file = stderr)
    print(*V)
    return (V,)


def check_tc(V):
    p = 3 - int(input())
    assert p in (1, 2)
    t = 1
    i = 0
    j = len(V)
    f = sol(V)
    score = [None, 0, 0]
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
        t = 3 - t
    if score[3 - p] <= score[p]:
        return False, f"You collected only {score[3 - p]} while your adversary collected {score[p]}. This is not good enough for a victory!"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
