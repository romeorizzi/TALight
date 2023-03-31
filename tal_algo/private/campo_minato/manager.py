#!/usr/bin/env python3

from functools import lru_cache
from os import environ
from random import randrange, randint
from tc import TC

DATA = ((10, (10,)), (90, (250,)))

TL = 2

MAPPER = {"small": 1, "big": 2}


def sol(M):
    m = len(M)
    n = len(M[0])
    MOD = 10**9 + 7
    V = [[0] * (n + 1) for i in range(m + 1)]
    V[m - 1][n - 1] = int(M[m - 1][n - 1])
    for i in reversed(range(m)):
        for j in reversed(range(n)):
            if i == m - 1 and j == n - 1:
                continue
            if M[i][j]:
                V[i][j] = (V[i + 1][j] + V[i][j + 1]) % MOD
    return V[0][0]

def display_griglia(M):
    m = len(M)
    n = len(M[0])
    for i in range(m):
        print("".join(map(lambda x: "." if x else "#", M[i])))

def gen_tc(maxn):
    m, n = randint(1, maxn), randint(1, maxn)
    M = [[bool(randrange(0, 10)) for j in range(n)] for i in range(m)]
    M[0][0] = M[m-1][n-1] = True
    print(m, n)
    display_griglia(M)
    return (M,)


def check_tc(M):
    risp = int(input())
    corr_answ = sol(M)
    if risp != corr_answ:
        return False, f"On input:\n{display_griglia(M)}\nyou answered:\n{risp}\nwhile the correct answer was:\n{corr_answ}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
