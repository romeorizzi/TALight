#!/usr/bin/env python3
from sys import stderr
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
        Tr = []
        for i in range(n):
            Tr.append(list(map(int, input().strip().split())))
        chooser = list(map(int, input().strip().split()))
        #display_triangle(Tr, stderr)
        #print(f"{chooser=}", file=stderr)
        #print(f"{game_val_ric_memo()=}", file=stderr)
        print(game_val_ric_memo(), flush=True)
        r = 0; c = 0; path = ""; path_val = Tr[r][c]
        while r < n-1:
            if chooser[r] == 0:
                next_move = input().strip()
                #print(f"server move = {next_move}", file=stderr)
            else:
                if Tr[r][c] == game_val_ric_memo(r, c) - game_val_ric_memo(r+1, c):
                    next_move = 'L'
                else:
                    next_move = 'R'
                print(next_move, flush=True)
                #print(f"our move = {next_move}", file=stderr)
            r += 1; c += 1 if next_move == 'R' else 0; path += next_move; path_val += Tr[r][c]
        print(path)
        print(path_val, flush=True)
        #print(f"{path=}, {path_val=}", file=stderr)
        game_val_ric_memo.cache_clear()
