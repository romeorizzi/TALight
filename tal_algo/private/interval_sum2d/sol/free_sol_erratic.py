#!/usr/bin/env python3
from sys import stderr, stdout
import random

from interval_sum_lib import Field

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        F = Field() # loads the interval_sum interactive instance from stdin
        #F.display(stderr)
        q = int(input())
        for i in range(1, 1 + q):
            a1, b1, a2, b2 = map(int, input().strip().split() )
            risp = F.sum(a1, b1, a2, b2)
            if random.randrange(q) < 2:
                risp += random.randint(-1,1)
            print(risp)
        stdout.flush()
