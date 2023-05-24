#!/usr/bin/env python3

from manager import sol

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        v = [int(x) for x in input().split()]
        print(sol(v))
