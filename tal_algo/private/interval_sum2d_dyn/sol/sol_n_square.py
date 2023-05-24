#!/usr/bin/env python3
from sys import stderr, stdout
import os
stderr = open(os.devnull, 'w') # comment this line to print-debug

from interval_sum_dyn_lib import display_matrix


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
        print(f"testcase {t}:", file = stderr)
        n1, n2 = map(int, input().strip().split())
        print(f"{n1=} {n2=}", file = stderr)
        M = [ [0] * n2 for _ in range(n1) ]
        r = int(input())
        print(f"{r=}", file = stderr)
        for i in range(1, 1 + r):
            request = list(map(int, input().strip().split()))
            print(f"{request=}", file = stderr)
            if len(request) == 4:
                a1, b1, a2, b2 = request
                corr_answ = interval_sum(a1, b1, a2, b2)
                print(corr_answ)
                print(f"corr_answ = interval_sum({a1}, {b1}, {a2}, {b2}) = {corr_answ}", file = stderr)
            else:
                assert len(request) == 3
                a, b, delta = request
                M[a][b] += delta    
            print(file = stderr)
            display_matrix(M, stderr)
            print(file = stderr)
        stdout.flush()
