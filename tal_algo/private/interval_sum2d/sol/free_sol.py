#!/usr/bin/env python3
from sys import stderr, stdout

from interval_sum_lib import Field

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        F = Field() # loads the interval_sum interactive instance from stdin
        #F.display(stderr)
        q = int(input())
        for i in range(1, 1 + q):
            a1, b1, a2, b2 = map(int, input().strip().split() )
            print(F.sum(a1, b1, a2, b2))
        stdout.flush()

