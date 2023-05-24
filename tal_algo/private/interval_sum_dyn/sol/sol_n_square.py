#!/usr/bin/env python3
from sys import stderr, stdout
import os
stderr = open(os.devnull, 'w') # comment this line to print-debug

from interval_sum_dyn_lib import display_array


def interval_sum(a, b):
    print(f"called interval_sum({a=}, {b=})", file = stderr)
    assert 0 <= a < b <= n
    risp = 0
    for i in range(a, b):
        risp += A[i]
    print(f"interval_sum returning {risp=}", file = stderr)
    return risp


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        print(f"testcase {t}:", file = stderr)
        n, r = map(int, input().strip().split())
        print(f"{n=} {r=}", file = stderr)
        A = [0] * n
        print(f"{r=}", file = stderr)
        for i in range(1, 1 + r):
            request = list(map(int, input().strip().split()))
            print(f"{request=}", file = stderr)
            if request[0] == 1:
                a, b = request[1:]
                corr_answ = interval_sum(a, b)
                print(corr_answ)
                print(f"corr_answ = interval_sum({a}, {b}) = {corr_answ}", file = stderr)
            else:
                i, delta = request[1:]
                A[i] += delta    
            print(file = stderr)
            display_array(A, stderr)
            print(file = stderr)
        stdout.flush()
