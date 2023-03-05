#!/usr/bin/env python3

from sys import stdout

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        V = list(map(int, input().split()))
        i, j = 0, n
        p = 0
        print(0, flush=True)
        t = 0
        while i < j:
            if p == t:
                if V[i] > V[j - 1]:
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
            t = 1 - t
