#!/usr/bin/env python3

from tc import TC
from random import choice, randint
from math import gcd
from os import environ
from functools import lru_cache
from sys import stderr

DATA = ((1, (None, None)), (9, (5, 50)), (90, (250, 1000)))

TL = 1

MAPPER = {"small": 2, "big": 3}


def sol(v):
    @lru_cache(maxsize=None)
    def f(n):
        if n < 0:
            return False
        if n == 0:
            return True
        return any(f(n - x) for x in v)

    m = min(v)
    i = 0
    last_nope = float("inf")
    while i - last_nope <= m:
        if not f(i):
            last_nope = i
        i += 1
    return last_nope


def gen_tc(n, k):
    if n is None:
        v = [4, 6, 9, 20]
        print(len(v))
        print(*v)
        return (v,)
    while True:
        numbers = [randint(2, k) for _ in range(n)]
        if gcd(*numbers) == 1:
            break
    print(len(numbers))
    print(*numbers)
    return (numbers,)


def check_tc(v):
    return sol(v) == int(input())


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
