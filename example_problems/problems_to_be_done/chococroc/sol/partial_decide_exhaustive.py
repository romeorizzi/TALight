#!/usr/bin/env python3
import sys
from sys import setrecursionlimit
setrecursionlimit(10**8)

def win_from(n, m):
    assert(1 <= n and 1 <= m)

    if (n == 1 and m == 1):
        return 0

    if (
        any(not win_from(n - s, m) for s in range(1, n // 2 + 1))
        or
        any(not win_from(n, m - s) for s in range(1, m // 2 + 1))
    ):
        return 1
    else:
        return 0

def cut_direction(n, m):
    return 0

def eat_size(n, m):
    return 0


if __name__ == "__main__":
    data = sys.stdin.readlines()
    assert(len(data) >= 3)
    m = int(data[1])
    n = int(data[2])
    print(str(2 - win_from(m,n)))
