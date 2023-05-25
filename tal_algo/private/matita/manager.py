#!/usr/bin/env python3
from os import environ
from sys import stderr, stdout
from random import randrange, randint
from functools import lru_cache

from tc import TC

from matita_lib import Matita_Graph


############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

HARDCODED_1 = (
             (5, [ (1, 4), (2, 3), (5, 4), (2, 1), (2, 4), (3, 4), (1, 5), (5, 2) ], 1, 5),
             (6, [ (2, 1), (2, 3), (2, 5), (2, 6), (4, 3), (4, 5) ], 1, 6),
            )
HARDCODED_2 = (
             (2, [ (1, 2) ], 1, 2),
             (3, [ (1, 2), (2, 3) ], 1, 3),
             (3, [ (1, 2), (2, 3), (3, 1) ], 1, 1),
             (4, [ (1, 2), (2, 3), (3, 4) ], 1, 4),
             (4, [ (1, 2), (2, 3), (3, 4), (4, 1) ], 1, 1),
             (4, [ (1, 2), (2, 3), (3, 4), (4, 1), (1, 3) ], 1, 3),
             (4, [ (1, 2), (2, 3), (3, 4), (4, 2) ], 1, 2),
             (4, [ (1, 2), (2, 3), (3, 1), (1,4) ], 1, 4),
            )
DATA_1 = tuple((1, ("hardcoded_rigid", n, E, s, t)) for n, E, s, t in HARDCODED_1)
DATA_2 = tuple((1, ("hardcoded", n, E, s, t)) for n, E, s, t in HARDCODED_2)
DATA = DATA_1 + DATA_2 + (
               (4, ("rand_gen",     5,    7)),
               (6, ("rand_gen",     6,    10)),
               (30, ("rand_gen",   100,   500)),
               (20, ("rand_gen",  1000,  5000)),
               (30, ("rand_gen", 10000, 50000))
              ) 
MAPPER = {"esempi_testo": 2, "smallest":
          2 + 8, "small": 2 + 8 + 2, "medium": 12 + 1, "big": 12 + 1 + 2, "huge": 12 + 3}
#################################################################


def gen_tc(*args):
    gen_type = args[0]
    G = Matita_Graph()
    if gen_type != "rand_gen":
        n, E, start, stop = args[1:]
        G.set_up(n, E, start, stop, input_node_names_start_from = 1)
    else:
        n, m = args[1:]
        G.init_Euler_path_simple(n, m, allow_less_edges = True)
    if gen_type != "hardcoded_rigid":
        G.shuffle()
    G.display(node_names_starting_from = 1, out = stdout)
    return (G,)


def check_tc(G):
    #G.display(node_names_starting_from = 1, out = stderr)
    risp_path = []
    for i in range(1, 1 + G.m):
        #print(f"checker is waiting for next edge", file = stderr)
        u, v = map(int, input().strip().split())
        #print(f"checker received the edge {i=}: {(u, v)=}", file = stderr)
        risp_path.append( (u, v) )    
    ok, feedback = G.check_Eulerian_path(risp_path, path_node_names_start_from = 1)
    if not ok:
        return False, feedback
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
