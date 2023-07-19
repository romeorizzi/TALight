#!/usr/bin/env python3

from sys import stderr

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        q = 1
        print("?", 0, n, flush=True)
        tot = int(input())
        for i in range(n - tot + 1):
            q += 1
            print("?", i, tot, flush=True)
            r = int(input())
            if r == -1:
                break
            if r == tot:
                print("!", i, tot, flush=True)
                break
        print(f"Case #{t+1:03} q:", q, file=stderr)
