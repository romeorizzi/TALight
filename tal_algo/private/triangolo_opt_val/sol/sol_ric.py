#!/usr/bin/env python3
from sys import stderr

def display_triangle(Tr,out=stderr):
    n = len(Tr)
    for i in range(n):
        print(" ".join(map(str,Tr[i])), file=out)

def max_val_ric(r,c):
    assert 0 <= c <= r < n
    if r == n-1:
        #print(f"called with {r=},{c=} returns {Tr[r][c]=}")
        return Tr[r][c]
    risp = Tr[r][c] + max(max_val_ric(r+1,c),max_val_ric(r+1,c+1))
    #print(f"called with {r=},{c=} returns {risp=}")
    return risp



def max_val(Tr):
    n = len(Tr)
    return max_val_ric(0,0)

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr,stderr)
        print(max_val(Tr))
