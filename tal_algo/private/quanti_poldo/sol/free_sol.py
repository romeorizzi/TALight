#!/usr/bin/env python3
from sys import stderr

from quanti_poldo_lib import recognize, IncrSubseqs

if __name__ == "__main__":
    T = int(input())
    for t in range(1, 1+T):
        print(f"Testcase {t}:", file=stderr)
        n, c, r, u = map(int, input().strip().split())
        S = list( map(int, input().strip().split()) )
        poldo = IncrSubseqs(S)
        print(poldo.num_nonleft[0])
        for _ in range(r):
            seq_of_indices = list( map(int, input().strip().split()) )
            print(poldo.rankShadow(seq_of_indices), end=" ")
        print()
        R = list( map(int, input().strip().split()) )
        for rank in R:
            print(" ".join(map(str, poldo.unrankShadow(rank))))
