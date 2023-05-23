#!/usr/bin/env python3
from sys import stderr, stdout, argv
import os
stderr = open(os.devnull, 'w') # comment this line to print-debug
import random

from interval_sum_dyn_lib import Fenwick, display_matrix

if __name__ == "__main__":
    erratic = len(argv) > 1
    T = int(input())
    for t in range(T):
        print(f"testcase {t}:", file = stderr)
        n1, n2 = map(int, input().strip().split())
        print(f"{n1=} {n2=}", file = stderr)
        F = Fenwick(n1, n2)
        r = int(input())
        print(f"{r=}", file = stderr)
        for i in range(1, 1 + r):
            request = list(map(int, input().strip().split()))
            print(f"{request=}", file = stderr)
            if len(request) == 4:
                a1, b1, a2, b2 = request
                answ = corr_answ = F.sum(a1, b1, a2, b2)
                if erratic and random.randrange(3) == 0:
                    answ += random.randint(-1,1)
                print(answ)
                print(f"corr_answ = F.sum({a1}, {b1}, {a2}, {b2}) = {corr_answ}, answered={answ}", file = stderr)
            else:
                assert len(request) == 3
                a, b, delta = request
                F.update(a, b, delta)    
            display_matrix(F.M, stderr)
            display_matrix(F.Fenwick, stderr)
            print(file = stderr)
        stdout.flush()

