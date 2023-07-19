#!/usr/bin/env python3
from os import environ
from sys import stderr, stdout
from random import randrange, randint

from tc import TC

from connected_components_lib import CC_Graph

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

HARDCODED = (
             (5, [ (0, 1), (2, 4), (3, 4), (2, 3), (0, 2), (1, 3) ]),
             (7, [ (0, 1), (4, 6), (2, 3), (0, 2), (4, 5), (5, 6), (1, 3) ]),
            )
DATA = tuple((1, ("hardcoded", n, E)) for n, E in HARDCODED) + (
            (12, ("rand_gen", 10, 20)),
            (18, ("rand_gen", 100, 500)),
            (18, ("rand_gen", 5000, 20000)),
        ) 
MAPPER = {"esempi_testo": 2, "small": 3, "medium": 4, "big": 5}
#################################################################


def gen_tc(*args):
    gen_type = args[0]
    G = CC_Graph()
    if gen_type != "rand_gen":
        n, E = args[1:]
        G.set_up(n, E)
    else:
        n, m = args[1:]
        #print(f"calling rand_gen({n=}, {m=})", file=stderr)
        G.rand_gen(n, m)
    if gen_type != "hardcoded":
        G.shuffle()
    G.set_up_star_representation()
    G.display(out = stdout)
    return (G,)


def check_tc(G):
    #G.display(out = stderr)
    risp_CC = []
    c = int(input())
    for k in range(1, 1 + c):
        #print(f"checker is waiting for connected component {k}", file = stderr)
        risp_CC.append(list(map(int, input().strip().split())))
    ok, feedback = G.check_connected_components(risp_CC)
    if not ok:
        return False, feedback
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
