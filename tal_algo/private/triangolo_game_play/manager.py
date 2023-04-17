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
    chooser = [randint(0, 1) for _ in range(n-1)]
    print(Tr.as_str())
    #print(Tr.as_str(), file=stderr)
    return (Tr, chooser)

def check_tc(Tr, chooser):
    risp_val = int(input())
    corr_val = Tr.game_val()
    #print(f"{corr_val=}, {risp_val=}", file=stderr)
    if risp_val != corr_val:
        return False, f"On input:\nTr.as_str()\nyou stated that the value of the game is {risp_val} while the correct value is {corr_val}"
    path, path_val = Tr.play(player = 0)
    assert path_val <= risp_val
    if path_val < risp_val:
        return False, f"On input:\nTr.as_str()\nyou stated that the value of the game is {risp_val}. This is correct. However, your play produced the path:\n{path}\nwhose value is only {path_val}"
    risp_path = input().strip()
    if risp_path != path:
        return False, f"On input:\nTr.as_str()\nyou stated that the value of the game is {risp_val}. This is correct. Moreover, your play resulted in the path:\n{path}\nwhose value is {path_val} >= {risp_val}. However, you finally reported the path:\n{path}\ninstead of the actual path that was formed during the game."
    risp_path_val = int(input())
    if risp_path_val != path_val:
        return False, f"On input:\nTr.as_str()\nyou stated that the value of the game is {risp_val}. This is correct. Moreover, we agree that, thanks to your smart play, the  actual path that was formed during the game was:\n{path}\n. Also, the value of this path is {path_val} >= {risp_val}, as required! However, in the very end you stated that the value of this path is {risp_path_val} instead of {path_val}. Please, correct this inconsistency!"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
