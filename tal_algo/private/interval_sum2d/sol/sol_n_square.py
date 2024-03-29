#!/usr/bin/env python3
from sys import stderr, stdout
import os
stderr = open(os.devnull, 'w') # comment this line to print-debug

def interval_sum(a1, b1, a2, b2):
    print(f"called interval_sum({a1=}, {b1=}, {a2=}, {b2=})", file = stderr)
    assert 0 <= a1 < b1 <= n1
    assert 0 <= a2 < b2 <= n2
    risp = 0
    for i in range(a1, b1):
        for j in range(a2, b2):
            risp += M[i][j]
    print(f"interval_sum returning {risp=}", file = stderr)
    return risp


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n1, n2 = map(int, input().strip().split())
        print(f"{n1=} {n2=}", file = stderr)
        M = []
        for _ in range(n1):
            M.append(list(map(int, input().strip().split())))
        print(f"{n1=}, {n2=}, {M=}", file = stderr)
        q = int(input())
        print(f"{q=}", file = stderr)
        for i in range(1, 1 + q):
            a1, b1, a2, b2 = map(int, input().strip().split() )
            corr_answ = interval_sum(a1, b1, a2, b2)
            print(corr_answ)
            print(f"corr_answ = interval_sum({a1}, {b1}, {a2}, {b2}) = {corr_answ}", file = stderr)
        stdout.flush()

