#!/usr/bin/env python3
from sys import stderr, stdout, argv
import os
stderr = open(os.devnull, 'w') # comment this line to print-debug
import random

from tc import TC

from interval_sum_dyn_lib import Fenwick, matrix_as_str

############## TESTCASES' PARAMETERS ############################
TL = 5   # the time limit for each testcase

HARDCODED = (
             (1, 7, 15,
              [
                  (0, 1, 0, 7),
                  (0, 0, 3),
                  (0, 1, 1),
                  (0, 2, 2),
                  (0, 1, 0, 7),
                  (0, 3, 1),
                  (0, 4, 1),
                  (0, 5, 1),
                  (0, 6, 2),
                  (0, 1, 0, 1),
                  (0, 1, 0, 2),
                  (0, 1, 0, 7),
                  (0, 1, 6, 7),
                  (0, 1, 2, 7),
                  (0, 1, 2, 6)
              ]
             ),
             (2, 3, 13,
              [
                  (0, 0, 3),
                  (0, 1, 1),
                  (0, 2, 2),
                  (1, 0, 1),
                  (1, 1, 1),
                  (1, 2, 1),
                  (0, 2, 0, 3),
                  (0, 2, 1, 3),
                  (0, 2, 1),
                  (0, 0, 1),
                  (0, 1, 1),
                  (0, 2, 0, 3),
                  (0, 2, 1, 3)
              ]
             ),
            )
DATA = tuple((1, ("hardcoded", n1, n2, r, R)) for n1, n2, r, R in HARDCODED)
DATA = DATA + (( 8, ("rand_gen",   1,    10,    20)),
               (10, ("rand_gen",   1,   100,   200)),
               (10, ("rand_gen",  10,    10,    30)),
               (10, ("rand_gen",  20,    20,   200)),
               (30, ("rand_gen",   1, 20000,   200)),
               (30, ("rand_gen", 200,   200,   200))
              )
MAPPER = {"esempi_testo": 2, "array_small": 3, "array_medium": 4, "mat_small": 5, "mat_medium": 6, "array_big": 7, "mat_big": 8}




#################################################################


def gen_tc(*args):
    gen_type = args[0]
    if gen_type == "hardcoded":
        n1, n2, r, R = args[1:]
    else:
        n1, n2, r = args[1:]
        R = []
        for i in range(r):
            if i % 5 == 0:
                i = random.randrange(n1)
                j = random.randrange(n2)
                delta = random.randrange(10)
                R.append( (i, j, delta) )
            else:
                size1 = random.randint(1, n1)
                size2 = random.randint(1, n2)
                a1 = random.randint(0, n1 - size1)
                a2 = random.randint(0, n2 - size2)
                R.append( (a1, a1 + size1, a2, a2 + size2) )
    return (n1, n2, r, R)

def check_tc(n1, n2, r, R):
    F = Fenwick(n1, n2)
    print(n1, n2)
    print(r)
    print(n1, n2, file = stderr)
    print(r, file = stderr)
    wrongs = ""
    for r in R:
        req_string = " ".join(map(str, r))
        print(req_string)
    stdout.flush()
    for r in R:
        print(req_string, file = stderr)
        if len(r) == 4:
            risp_val = int(input())
            corr_val = F.sum(*r)
            print(f"{corr_val=}, {risp_val=}", file=stderr)
            if risp_val != corr_val:
                if len(wrongs) == 0:
                    wrongs = f"With reference to the matrix/array:\n{matrix_as_str(F.M)}\nyou stated that:\n"
                wrongs += f"   sum({r}) = {risp_val} (whereas sum{r} = {corr_val})\n"
        else:
            F.update(*r)
    if len(wrongs) == 0:
        return True
    else:
        return False, wrongs


if __name__ == "__main__":
    size = MAPPER[os.environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
