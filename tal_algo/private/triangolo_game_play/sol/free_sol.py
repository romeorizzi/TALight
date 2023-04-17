#!/usr/bin/env python3
from sys import stderr

from triangolo_lib import game_val, display_triangle

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        chooser = list(map(int,input().strip().split()))
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #print(f"{chooser=}", file=stderr)
        #display_triangle(Tr, stderr)
        #print(f"{game_val(Tr, chooser)=}", file=stderr)
        print(game_val(Tr, chooser), flush=True)
        r = 0; c = 0; path = ""; path_val = Tr[r][c]
        while r < n-1:
            if chooser[r] == 0:
                next_move = input().strip()
                #print(f"server move = {next_move}", file=stderr)
            else:
                if Tr[r][c] == game_val(Tr, chooser, r, c) - game_val(Tr, chooser, r+1, c):
                    next_move = 'L'
                else:
                    next_move = 'R'
                print(next_move, flush=True)
                #print(f"our move = {next_move}", file=stderr)
            r += 1; c += 1 if next_move == 'R' else 0; path += next_move; path_val += Tr[r][c]
        print(path)
        print(path_val, flush=True)
        #print(f"{path=}, {path_val=}", file=stderr)

