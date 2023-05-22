#!/usr/bin/env python3
from sys import stderr, stdout
from os import environ
import random

from tc import TC

from interval_sum_lib import Array

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

HARDCODED = (
             (
              [3, 1, 2, 1, 1, 1, 2],
              [
                 (0, 1),
                 (0, 2),
                 (0, 2),
                 (6, 7),
                 (2, 7),
                 (2, 6)
              ]
             ),
             (
              [1, 1, 1, 1, 1, 1, 1],
              [
                 (0, 1),
                 (0, 2),
                 (0, 3),
                 (0, 4),
                 (0, 5),
                 (0, 6),
                 (0, 7)
              ]
             ),
            )
DATA = tuple((1, ("hardcoded", vec, Q)) for vec, Q in HARDCODED)
DATA = DATA + (
               (8, ("rand_gen",   10,   20)),
               (10, ("rand_gen",  1000,   1000)),
               (30, ("rand_gen",   10000,   10000))
              )
MAPPER = {"esempi_testo": 2, "small": 3, "medium": 4, "big": 5}




#################################################################


def gen_tc(*args):
    gen_type = args[0]
    if gen_type == "hardcoded":
        vec, Q = args[1:]
    else:
        n, q = args[1:]
        vec = [ random.randint(10, 99) for _ in range(n) ]
        Q = []
        for i in range(q):
            size = random.randint(1, n)
            a = random.randint(0, n - size)
            Q.append( (a, a + size) )
    A = Array(vec)
    return (A, Q)

def check_tc(A, Q):
    A.display(out = stdout)
    print(len(Q))
    #A.display(out = stderr)
    #print(len(Q), file = stderr)
    #print(Q, file = stderr)
    wrongs = ""
    for q in range(len(Q)):
        print(Q[q][0], Q[q][1], flush=True)
    for q in range(len(Q)):
        #print(Q[q][0], Q[q][1], file = stderr)
        risp_val = int(input())
        corr_val = A.sum(Q[q][0], Q[q][1])
        #print(f"{corr_val=}, {risp_val=}", file=stderr)
        if risp_val != corr_val:
            if len(wrongs) == 0:
                wrongs = f"With reference to the array:\n{A.as_str(with_n = False)}\nyou stated that:\n"
            wrongs += f"   sum{Q[q]} = {risp_val} (whereas sum{Q[q]} = {corr_val})\n"
    if len(wrongs) == 0:
        return True
    else:
        return False, wrongs

if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
