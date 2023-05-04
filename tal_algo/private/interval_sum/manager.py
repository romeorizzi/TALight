#!/usr/bin/env python3
from sys import stderr, stdout
from os import environ
import random
from functools import lru_cache

from tc import TC

from interval_sum_lib import Field

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

HARDCODED = (
             (
              [ [3, 1, 2, 1, 1, 1, 2] ],
              [
                 (0, 1, 0, 1),
                 (0, 1, 0, 2),
                 (0, 1, 0, 2),
                 (0, 1, 6, 7),
                 (0, 1, 2, 7),
                 (0, 1, 2, 6)
              ]
             ),
             (
              [ [3, 1, 2, 1, 1, 1, 2],
                [1, 1, 1, 1, 1, 1, 1],
                [3, 1, 2, 1, 1, 1, 2],
                [0, 0, 0, 0, 0, 0, 0],
                [3, 1, 2, 1, 1, 1, 2]    
               ],
               [
                 (0, 1, 0, 1),
                 (0, 1, 0, 7),
                 (2, 3, 2, 7),
                 (0, 5, 0, 7),
                 (1, 2, 1, 2),
                 (1, 2, 1, 3)
                ]
             ),
            )
DATA = tuple((1, ("hardcoded", M, Q)) for M, Q in HARDCODED)
DATA = DATA + (( 8, ("rand_gen",   1,    10,    20)),
               (10, ("rand_gen",   1,   100,   100)),
               (10, ("rand_gen",  10,    10,    20)),
               (10, ("rand_gen",  20,    20,   100)),
               (30, ("rand_gen",   1, 10000, 200)),
               (30, ("rand_gen", 100,   100, 200))
              )
MAPPER = {"esempi_testo": 2, "array_small": 3, "array_medium": 4, "mat_small": 5, "mat_medium": 6, "array_big": 7, "mat_big": 8}




#################################################################


def gen_tc(*args):
    gen_type = args[0]
    if gen_type == "hardcoded":
        M, Q = args[1:]
    else:
        n1, n2, q = args[1:]
        M = []
        for i in range(n1):
            M.append( [ random.randint(10, 99) for _ in range(n2) ] )
        Q = []
        for i in range(q):
            a1 = random.randrange(n1)
            b1 = random.randint(a1 + 1, n1)
            a2 = random.randrange(n2)
            b2 = random.randint(a2 + 1, n2)
            Q.append( (a1, b1, a2, b2) )
    F = Field(M)
    return (F, Q)

def check_tc(F, Q):
    F.display(out = stdout)
    print(len(Q))
    #F.display(out = stderr)
    #print(len(Q), file = stderr)
    #print(Q, file = stderr)
    wrongs = ""
    for q in range(len(Q)):
        print(Q[q][0], Q[q][1], Q[q][2], Q[q][3], flush=True)
        #print(Q[q][0], Q[q][1], Q[q][2], Q[q][3], file = stderr)
        risp_val = int(input())
        corr_val = F.sum(Q[q][0], Q[q][1], Q[q][2], Q[q][3])
        #print(f"{corr_val=}, {risp_val=}", file=stderr)
        if risp_val != corr_val:
            if len(wrongs) == 0:
                wrongs = f"With reference to the matrix/array:\n{F.as_str(with_n1_n2 = False)}\nyou stated that:\n"
            wrongs += f"   sum{Q[q]} = {risp_val} (whereas sum{Q[q]} = {corr_val})\n"
    if len(wrongs) == 0:
        return True
    else:
        return False, wrongs


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
