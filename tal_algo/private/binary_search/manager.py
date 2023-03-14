#!/usr/bin/env python3

from tc import TC
from os import environ
from random import randrange
from sys import stderr

#DATA = ((60, (100,)), (20, (2**15,)), (20, (10**18,)))
DATA = ((2, (100,)), (1, (2**15,)), (1, (10**18,)))

TL = 3

MAPPER = {"small": 1, "big": 2, "huge": 3}

MAX_QUERY = 61


def gen_tc(N):
    s = randrange(N)
    print(f"# Guess an integer secret number s in the interval [1,{N}]")
    print(N, flush=True)
    return (N,s)


def check_tc(N, s):
    q = MAX_QUERY
    while True:
        qs = input().strip().split(" ")
        assert len(qs) == 2
        assert qs[0] in ("?", "!")
        guess = int(qs[1])
        if qs[0] == "?":
            if q == 0:
                print("-1", flush=True)
                break
            q -= 1
            if s > guess:
                print(f"# s > {guess}")
                print(">", flush=True)
            elif s < guess:
                print(f"# s < {guess}")
                print("<", flush=True)
            else:
                print(f"# s = {guess}. You should now submit your definitive answer (use '!' rather than '?')")
                print("=", flush=True)
        else:
            if s == guess:
                print("# Ok, correct!", flush=True)
                return True
            else:
                print(f"# No. You submitted {guess} while the correct secret number was {s}", flush=True)
                return False
    return False


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
