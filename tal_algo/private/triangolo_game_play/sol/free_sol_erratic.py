#!/usr/bin/env python3
from sys import stderr
import random

from triangolo_lib import Triangolo

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        Tr = Triangolo(game = True) # loads the triangle game instance from stdin
        #Tr.display(stderr)
        #print(f"{Tr.game_val_ric_memo()=}", file=stderr)
        dice = random.randrange(0,6)
        if dice == 0:
            print(Tr.game_val_ric_memo() + random.randint(-1, 1), flush=True)
        else:
            print(Tr.game_val_ric_memo(), flush=True)
        r = 0; c = 0; path = ""; path_val = Tr.T[r][c]
        while r < n-1:
            if chooser[r] == 0:
                next_move = input().strip()
                #print(f"server move = {next_move}", file=stderr)
            else:
                if Tr.T[r][c] == Tr.game_val_ric_memo(r, c) - Tr.game_val_ric_memo(r+1, c):
                    next_move = 'L'
                else:
                    next_move = 'R'
                next_move = random.choice(next_move * (4*n) + "LR")
                print(next_move, flush=True)
                #print(f"our move = {next_move}", file=stderr)
            r += 1; c += 1 if next_move == 'R' else 0; path += next_move; path_val += Tr.T[r][c]
        print(path)
        print(path_val, flush=True)
        #print(f"{path=}, {path_val=}", file=stderr)
