#!/usr/bin/env python3

from sys import stdout, stderr

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        m, n = map(int, input().strip().split())
        print(f"Testcase {t}: {m=}, {n=}", file=stderr)
        if m == n:
            me_to_move = 2 # preferisco giocare per secondo
        else:
            me_to_move = 1 # preferisco giocare per primo
        print(me_to_move, flush=True)
        while m + n > 2:
            if m == n:
                m, n = map(int, input().strip().split())
            else:
                if m > n:
                    m = n
                else:
                    n = m
                print(f"{m} {n}", flush=True)
