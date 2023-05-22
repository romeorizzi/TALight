#!/usr/bin/env python3
from sys import stderr
import random

from interval_sum_lib import Array

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        A = Array() # loads the interval_sum instance from stdin
        #A.display(stderr)
        q = int(input())
        for i in range(1, 1 + q):
            a, b = map(int, input().strip().split() )
            risp = A.sum(a, b)
            if random.randrange(q) < 2:
                risp += random.randint(-1, 1)
            print(risp, flush=True)
