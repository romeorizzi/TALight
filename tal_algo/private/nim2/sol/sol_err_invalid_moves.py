#!/usr/bin/env python3
from sys import stdout, stderr
from random import randint

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        m, n = map(int, input().strip().split())
        print(f"Testcase {t+1}: {m=}, {n=}", file=stderr)
        if m == n:
            me_to_move = 2 # preferisco giocare per secondo
        else:
            me_to_move = 1 # preferisco giocare per primo
        print(me_to_move, flush=True)
        while m != 1 or n != 1:
            if me_to_move == 2:
                m, n = map(int, input().strip().split())
                # print(f"bot just read {m=} {n=}", file=stderr)
            else:
                # print(f"currently in bot {m=} {n=}", file=stderr)
                dice = randint(0, 6*m)
                if dice == 0:
                    print(f"{m} {n}", flush=True)
                elif dice == 1:
                    print(f"-1 {n}", flush=True)
                elif dice == 2:
                    print(f"{m-1} {n-1}", flush=True)
                elif dice == 3:
                    print(f"{m+1} {n}", flush=True)
                elif dice == 4:
                    print(f"{m} {n+1}", flush=True)
                else:
                    if m > n:
                        m = n
                    elif m < n:
                        n = m
                    else:
                        assert m == n
                        m = m // 2
                    print(f"{m} {n}", flush=True)
            me_to_move = 3 - me_to_move
