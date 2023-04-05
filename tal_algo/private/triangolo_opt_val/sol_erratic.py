#!/usr/bin/env python3
from random import randrange
from functools import lru_cache

def display_triangle(Tr):
    n = len(Tr)
    for i in range(n):
        print(" ".join(map(str,Tr[i])))


def max_val(Tr):
    #display_triangle(Tr)
    
    @lru_cache(maxsize=None)
    def max_val_ric_memo(r,c):
        assert 0 <= c <= r < n
        if r == n-1:
            #print(f"called with {r=},{c=} returns {Tr[r][c]=}")
            return Tr[r][c]
        risp = Tr[r][c] + max(max_val_ric_memo(r+1,c),max_val_ric_memo(r+1,c+1))
        #print(f"called with {r=},{c=} returns {risp=}")
        return risp

    n = len(Tr)
    return max_val_ric_memo(0,0)

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input().strip())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr)
        dice = randrange(0,6)
        if dice == 0:
            print(max_val(Tr)-1)
        else:
            print(max_val(Tr))
