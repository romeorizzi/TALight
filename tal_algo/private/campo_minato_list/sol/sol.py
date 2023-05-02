#!/usr/bin/env python3

from campo_minato_lib import num_paths_from

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n, m = map(int, input().strip().split())
        M = list(map(lambda x: [y == "." for y in x], [input() for i in range(n)]))
        print(num_paths_from(M))
