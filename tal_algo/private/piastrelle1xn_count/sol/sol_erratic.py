#!/usr/bin/env python3
from sys import stderr
from random import randrange
import numpy as np


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


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        print(f"{n=}",file=stderr)
        dice = randrange(0,6)
        if dice == 0:
            print(sol(n)+1)
        else:
            print(sol(n))
