#!/usr/bin/env python3
from sys import stderr
from functools import lru_cache

def display_triangle(Tr,out=stderr):
    for i in range(n):
        print(" ".join(map(str, Tr[i])), file=out)

def game_val(Tr, chooser):
    for r in reversed(range(n-1)):
        for c in range(r+1):
            if chooser[r] == 1:
                Tr[r][c] += max(Tr[r+1][c],Tr[r+1][c+1])
            else:
                Tr[r][c] += min(Tr[r+1][c],Tr[r+1][c+1])
    return Tr[0][0]

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        chooser = list(map(int,input().strip().split()))
        #display_triangle(Tr,stderr)
        #print(chooser, file=stderr)
        print(game_val(Tr, chooser))
