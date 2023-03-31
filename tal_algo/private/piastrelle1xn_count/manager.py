#!/usr/bin/env python3

import numpy as np
from os import environ
from os.path import join
from random import randrange
from sys import stderr
from time import time
from tc import TC

DATA = ((10, (0, 10)), (90, (10**5, 10**6)), (100, (10**17, 10**18)))

TL = 1

MAPPER = {"small": 1, "big": 2, "huge": 3}


def mexp(b, e, m):
    if e == 0:
        return np.identity(b.shape[0], dtype=object)
    elif e % 2 == 0:
        tmp = mexp(b, e // 2, m)
        return (tmp @ tmp) % m
    else:
        return (mexp(b, e - 1, m) @ b) % m


def sol(n):
    M = 10**9 + 7
    A = np.array([[0, 1], [1, 1]], dtype=object)
    return mexp(A, n + 1, M)[1, 0]


def gen_tc(a, b):
    n = randrange(a, b)
    print(n)
    return (n,)


def check_tc(n):
    risp = int(input())
    corr_answ = sol(n)
    if risp != corr_answ:
        return False, f"On input:\n{n}\nyou answered:\n{risp}\nwhile the correct answer was:\n{corr_answ}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
