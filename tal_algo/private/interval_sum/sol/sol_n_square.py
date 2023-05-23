#!/usr/bin/env python3
from sys import stderr, stdout
import os
stderr = open(os.devnull, 'w') # comment this line to print-debug

def interval_sum(a, b):
    print(f"called interval_sum({a=}, {b=})", file = stderr)
    assert 0 <= a < b <= n
    risp = 0
    for i in range(a, b):
        risp += vec[i]
    print(f"interval_sum returning {risp=}", file = stderr)
    return risp


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        print(f"{n=}", file = stderr)
        vec = []
        for _ in range(n):
            vec.append(int(input()))
        print(f"{n=}, {vec=}", file = stderr)
        q = int(input())
        print(f"{q=}", file = stderr)
        for i in range(1, 1 + q):
            a, b = map(int, input().strip().split() )
            corr_answ = interval_sum(a, b)
            print(corr_answ)
            print(f"corr_answ = interval_sum({a}, {b}) = {corr_answ}", file = stderr)
        stdout.flush()

