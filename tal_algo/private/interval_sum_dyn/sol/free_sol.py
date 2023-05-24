#!/usr/bin/env python3
from sys import stderr, stdout, argv
import os
stderr = open(os.devnull, 'w') # comment this line to print-debug
import random

from interval_sum_dyn_lib import Fenwick, display_array

if __name__ == "__main__":
    erratic = len(argv) > 1
    T = int(input())
    for t in range(T):
        print(f"testcase {t}:", file = stderr)
        n, r = map(int, input().strip().split())
        print(f"{n=} {r=}", file = stderr)
        F = Fenwick(n)
        for i in range(1, 1 + r):
            request = list(map(int, input().strip().split()))
            print(f"{request=}", file = stderr)
            if request[0] == 1:
                a, b = request[1:]
                answ = corr_answ = F.sum(a, b)
                if erratic and random.randrange(3) == 0:
                    answ += random.randint(-1, 1)
                print(answ)
                print(f"corr_answ = F.sum({a}, {b}) = {corr_answ}, answered={answ}", file = stderr)
            else:
                i, delta = request[1:]
                F.update(i, delta)    
            display_array(F.A, stderr)
            display_array(F.Fenwick, stderr)
            print(file = stderr)
        stdout.flush()

