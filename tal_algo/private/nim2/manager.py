#!/usr/bin/env python3
from os import environ
from sys import setrecursionlimit, stderr
from random import randrange, randint

from tc import TC

TL = 1

DATA = ((12, (6, 6)), (12, (10, 10)), (12, (100, 100)), (12, (3, 10**9)), (12, (10**9, 10**9)), )

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "skewed": 4, "big": 5}

def gen_tc(max_m, max_n):
    m = randint(max_m//2, max_m)
    n = randint(max_n//2, max_n)
    print(m, n)
    return (m, n)


def check_tc(m, n):
    first_turn_of_problem_solver = int(input())
    assert first_turn_of_problem_solver in (1, 2)
    server_to_move = ( first_turn_of_problem_solver == 2 )
    list_of_conf = [ (m, n, "server to move" if server_to_move else "problem solver to move") ]
    invalid_move_spotted = False
    while m + n > 2:
        if server_to_move:
            if m == n:
                if randint(0, 1) == 1:
                    m = m // 2
                else:
                    n = n // 2
            else:
                if m > n:
                    m = n
                else:
                    n = m
            # print(f"the server is submitting: {m=} {n=}", file=stderr)
            print(f"{m} {n}", flush=True)
        else:
            new_m, new_n = map(int, input().strip().split())
            # print(f"the server just received: {m=} {n=}", file=stderr)
            if new_m > m or new_n > n or new_m < 1 or new_n < 1 or new_m + new_n == m + n or (new_m < m and new_n < n):
                invalid_move_spotted = True
            m, n = new_m, new_n
        server_to_move = not server_to_move
        list_of_conf.append( (m, n, "server to move" if server_to_move else "problem solver to move") )
        if invalid_move_spotted:
            print("1 1", flush=True)
            m, n = 1, 1
            return False, f"You have lost this game because your last move has violated the rules. Up to that point, the game has traversed the following configurations:\n" + "\n".join([f"({str(m)}, {str(n)}, {turn})" for m, n, turn in list_of_conf])
    if not server_to_move:
        return False, f"You have lost this game. The game has traversed the following configurations:\n" + "\n".join([f"({str(m)}, {str(n)}, {turn})" for m, n, turn in list_of_conf])
    return True, f"You have won this game." # + " The game has traversed the following configurations:\n" + "\n".join([f"({str(m)}, {str(n)}, {turn})" for m, n, turn in list_of_conf])


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
