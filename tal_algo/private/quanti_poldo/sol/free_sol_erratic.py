#!/usr/bin/env python3
from sys import stderr
from random import randrange, randint

from FBF_trasparenti_lib import recognize, Par

if __name__ == "__main__":
    T = int(input())
    for t in range(1, 1+T):
        print(f"Testcase {t}:", file=stderr)
        n_pairs, c, r, u = map(int, input().strip().split())
        p = Par(n_pairs)
        coin = randrange(2)
        delta = 1 -2*coin
        dice = randrange(6)
        if dice > 0:
            delta = 0
        print(p.num_twffs[n_pairs] + delta)
        for _ in range(r):
            fbf = input().strip()
            print(p.rankFBF_t(fbf) + delta, end=" ")
        print()
        R = list( map(int, input().strip().split()) )
        print(f"{R=}", file=stderr)
        for rank in R:
            print(p.unrankFBF_t(n_pairs, rank + delta))
                
