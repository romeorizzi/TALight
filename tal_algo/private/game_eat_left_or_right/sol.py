#!/usr/bin/env python3

from manager import sol
from sys import stdout

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        V = list(map(int, input().strip().split()))
        f = sol(V)
        fullscore = sum(V)
        i, j = 0, n
        if f(i, j)[0] > fullscore / 2:
            p = 1
        else:
            p = 2
        print(p)
        stdout.flush()
        t = 1
        while i < j:
            if p == t:
                if f(i, j)[1] == "L":
                    print("L", flush=True)
                    i += 1
                else:
                    print("R", flush=True)
                    j -= 1
            else:
                if input().strip() == "L":
                    i += 1
                else:
                    j -= 1
            t = 3 - t
