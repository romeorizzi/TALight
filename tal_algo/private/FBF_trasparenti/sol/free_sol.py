#!/usr/bin/env python3
from sys import stderr

from FBF_trasparenti_lib import recognize, Par

if __name__ == "__main__":
    T = int(input())
    for t in range(1, 1+T):
        print(f"Testcase {t}:", file=stderr)
        n_pairs, c, r, u = map(int, input().strip().split())
        p = Par(n_pairs)
        print(p.num_twffs[n_pairs])
        for _ in range(r):
            fbf = input().strip()
            print(p.rankFBF_t(fbf), end=" ")
        print()
        R = list( map(int, input().strip().split()) )
        for rank in R:
            print(p.unrankFBF_t(n_pairs, rank))
