#!/usr/bin/env python3
from sys import stderr
from random import randrange, randint
from functools import lru_cache

def display_triangle(Tr, out=stderr):
    for i in range(n):
        print(" ".join(map(str, Tr[i])), file=out)

@lru_cache(maxsize=None)
def game_val_ric_memo(r=0, c=0):
    assert 0 <= c <= r < n
    if r == n-1:
        return Tr[r][c]
    if chooser[r] == 1:
        return Tr[r][c] + max(game_val_ric_memo(r+1, c), game_val_ric_memo(r+1, c+1))
    return Tr[r][c] + min(game_val_ric_memo(r+1, c), game_val_ric_memo(r+1, c+1))

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        chooser = list(map(int,input().strip().split()))
        Tr = []
        for i in range(n):
            Tr.append(list(map(int, input().strip().split())))
        #display_triangle(Tr, stderr)
        dice = randrange(0,6)
        if dice == 0:
            print(game_val_ric_memo() + randint(-1, 1))
        else:
            print(game_val_ric_memo())
        game_val_ric_memo.cache_clear()
