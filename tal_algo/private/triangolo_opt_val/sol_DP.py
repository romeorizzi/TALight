#!/usr/bin/env python3
from functools import lru_cache

def display_triangle(Tr):
    n = len(Tr)
    for i in range(n):
        print(" ".join(map(str,Tr[i])))

def max_val(Tr):
    display_triangle(Tr)
    n = len(Tr)
    if n > 1:
        for r in reversed(range(n-1)):
             for c in range(r+1):
                  Tr[r][c] += max(Tr[r+1][c],Tr[r+1][c+1])
    display_triangle(Tr)
    return Tr[0][0]

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input().strip())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr)
        print(max_val(Tr))
