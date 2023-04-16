#!/usr/bin/env python3
from sys import stderr

def display_triangle(Tr,out=stderr):
    n = len(Tr)
    for i in range(n):
        print(" ".join(map(str,Tr[i])), file=out)

def game_val_ric(r=0,c=0):
    assert 0 <= c <= r < n
    if r == n-1:
        #print(f"called with {r=},{c=} returns {Tr[r][c]=}")
        return Tr[r][c]
    if chooser[r] == 1:
        risp = Tr[r][c] + max(game_val_ric(r+1,c),game_val_ric(r+1,c+1))
    else:
        risp = Tr[r][c] + min(game_val_ric(r+1,c),game_val_ric(r+1,c+1))
    #print(f"called with {r=},{c=} returns {risp=}")
    return risp



if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        chooser = list(map(int,input().strip().split()))
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr, stderr)
        print(game_val_ric())
