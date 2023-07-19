#!/usr/bin/env python3
from sys import stdout, stderr
from random import randint

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
            if me_to_move == 2:
                m, n = map(int, input().strip().split())
            else:
                if m > n:
                    m = n
                elif m < n:
                    n = m
                else:
                    m = m // 2
                if m > 1 and randint(1, m) == 1:
                    m -= 1
                print(f"{m} {n}", flush=True)
            me_to_move = 3 - me_to_move
