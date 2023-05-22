#!/usr/bin/env python3
from sys import stderr

from interval_sum_lib import Array

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        A = Array() # loads the interval_sum instance from stdin
        #A.display(stderr)
        q = int(input())
        for i in range(1, 1 + q):
            a, b = map(int, input().strip().split() )
            print(A.sum(a, b), flush=True)

