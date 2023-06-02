#!/usr/bin/env python3
from os import environ
from sys import stderr
from random import randrange, randint

from tc import TC

from game_eat_left_or_right_lib import sol

TL = 1

DATA = ((10, (6,)), (10, (20,)), (20, (100,)))

MAPPER = {"small": 1, "medium": 2, "big": 3}


def gen_tc(n):
    V = [randrange(0, 10**5) for i in range(n)]
    if sum(V) % 2:
        V[randrange(0, n)] += 1
    print(n)
    print(*V)
    print(n, file = stderr)
    print(*V, file = stderr)
    return (V,)


def check_tc(V):
    f = sol(V)
    my_turn = (int(input()) == 2)
    i = 0
    j = len(V)
    score_mine = 0
    score_bot = 0
    while i < j:
        if my_turn:
            if f(i, j)[1] == "L":
                print("L", flush=True)
                score_mine += V[i]
                i += 1
            else:
                print("R", flush=True)
                j -= 1
                score_mine += V[j]
        else:
            if input().strip() == "L":
                score_bot += V[i]
                i += 1
            else:
                j -= 1
                score_bot += V[j]
        my_turn = not my_turn
    if score_bot <= score_mine:
        return False, f"You collected only {score_bot} while I have collected {score_mine}, which is more. This is not good enough for a victory!"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
