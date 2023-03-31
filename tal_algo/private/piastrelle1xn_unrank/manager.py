#!/usr/bin/env python3

import numpy as np
from os import environ
from random import randrange
from sys import stderr
from time import time
from tc import TC
from sol import unrank

DATA = ((10, (0, 10)), (10, (0, 10)), (80, (10**2, 10**3)))

TL = 1

MAPPER = {"small": 1, "medium": 1, "big": 2}


def mexp(b, e):
    if e == 0:
        return np.identity(b.shape[0], dtype=object)
    elif e % 2 == 0:
        tmp = mexp(b, e // 2)
        return tmp @ tmp
    else:
        return mexp(b, e - 1) @ b


def num_piastrellature(n):
    A = np.array([[0, 1], [1, 1]], dtype=object)
    return mexp(A, n + 1)[1, 0]

def gen_tc(a, b):
    n = randrange(a, b)
    rank = randrange(0, num_piastrellature(n))
    print(n, rank)
    return (n, rank)


def check_tc(n, rank):
    risp = input().strip()
    corr_answ = unrank(n,rank)
    if risp != corr_answ:
        return False, f"On input:\n{n} {rank}\nyou answered:\n{risp}\nwhile the correct answer was:\n{corr_answ}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
