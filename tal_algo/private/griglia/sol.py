#!/usr/bin/env python3

from manager import sol

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n, m = map(int, input().split())
        M = list(map(lambda x: [y == "." for y in x], [input() for i in range(n)]))
        print(sol(M))
