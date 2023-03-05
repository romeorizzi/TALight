#!/usr/bin/env python3

from functools import lru_cache
from os import environ
from random import randrange, randint
from tc import TC

DATA = ((10, (10,)), (90, (250,)))

TL = 2

MAPPER = {"small": 1, "big": 2}


def sol(M):
    n = len(M)
    m = len(M[0])
    MOD = 10**9 + 7
    V = [[0] * (m + 1) for i in range(n + 1)]
    V[n - 1][m - 1] = int(M[n - 1][m - 1])
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if i == n - 1 and j == m - 1:
                continue
            if M[i][j]:
                V[i][j] = (V[i + 1][j] + V[i][j + 1]) % MOD
    return V[0][0]


def gen_tc(maxn):
    n, m = randint(1, maxn), randint(1, maxn)
    M = [[bool(randrange(0, 10)) for j in range(m)] for i in range(n)]
    print(n, m)
    for i in range(n):
        print("".join(map(lambda x: "." if x else "#", M[i])))
    return (M,)


def check_tc(M):
    return sol(M) == int(input())


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
