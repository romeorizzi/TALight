#!/usr/bin/env python3
from sys import stderr, stdout
from os import environ
from random import randrange, randint
from functools import lru_cache

from tc import TC

from triangolo_lib import triangle_as_str, display_triangle, game_val

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "big": 4}
DATA = ((10, (5, 7)), (10, (8, 10)), (10, (25, 28)), (70, (30, 40)))
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
#################################################################


def gen_tc(min_n, max_n):
    n = randint(min_n, max_n)
    Tr = [[randint(0, 9) for j in range(i+1)] for i in range(n)]
    print(n)
    chooser = [randint(0,1) for _ in range(n-1)]
    print(" ".join(map(str, chooser)))
    print(triangle_as_str(Tr), flush=True)
    #print(f"{chooser=}", file=stderr)
    #display_triangle(Tr, stdout)
    return (Tr, chooser)

def check_tc(Tr, chooser):
    n = len(Tr)
    risp_val = int(input())
    corr_val = game_val(Tr, chooser)
    #print(f"{chooser=}", file=stderr)
    #display_triangle(Tr, stderr)
    #print(f"{corr_val=}, {risp_val=}", file=stderr)
    if risp_val != corr_val:
        return False, f"On input:\n{n}\n{chooser}\n{triangle_as_str(Tr)}\nyou stated that the value of the game is {risp_val} while the correct value is {corr_val}"
    r = 0; c = 0; path = ""; path_val = Tr[0][0]
    while r < n-1:
        if chooser[r] == 1:
            next_move = input().strip()
        else:
            if Tr[r][c] == game_val(Tr, chooser, r, c) - game_val(Tr, chooser, r+1, c):
                next_move = 'L'
            else:
                next_move = 'R'
            print(next_move, flush=True);
        r += 1; c += 1 if next_move == 'R' else 0;
        path += next_move; path_val += Tr[r][c]
    assert path_val <= risp_val
    if path_val < risp_val:
        return False, f"On input:\n{n}\n{chooser}\n{triangle_as_str(Tr)}\nyou stated that the value of the game is {risp_val}. This is correct. However, your play produced the path:\n{path}\nwhose value is only {path_val}"
    risp_path = input().strip()
    if risp_path != path:
        return False, f"On input:\n{n}\n{chooser}\n{triangle_as_str(Tr)}\nyou stated that the value of the game is {risp_val}. This is correct. Moreover, your play resulted in the path:\n{path}\nwhose value is {path_val} >= {risp_val}. However, you finally reported the path:\n{path}\ninstead of the actual path that was formed during the game."
    risp_path_val = int(input())
    if risp_path_val != path_val:
        return False, f"On input:\n{n}\n{chooser}\n{triangle_as_str(Tr)}\nyou stated that the value of the game is {risp_val}. This is correct. Moreover, we agree that, thanks to your smart play, the  actual path that was formed during the game was:\n{path}\n. Also, the value of this path is {path_val} >= {risp_val}, as required! However, in the very end you stated that the value of this path is {risp_path_val} instead of {path_val}. Please, correct this inconsistency!"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
