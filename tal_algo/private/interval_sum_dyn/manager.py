#!/usr/bin/env python3
from sys import stderr, stdout, argv
import os
stderr = open(os.devnull, 'w') # comment this line to print-debug
import random

from tc import TC

from interval_sum_dyn_lib import Fenwick, array_as_str

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

HARDCODED = (
             (7, 14,
              [
                  (1, 0, 7),
                  (0, 0, 3),
                  (0, 1, 1),
                  (0, 2, 2),
                  (0, 3, 1),
                  (0, 4, 1),
                  (0, 5, 1),
                  (0, 6, 2),
                  (1, 0, 2),
                  (1, 0, 3),
                  (1, 0, 4),
                  (1, 0, 5),
                  (1, 0, 6),
                  (1, 0, 7),
              ]
             ),
             (7, 15,
              [
                  (1, 0, 7),
                  (0, 0, 3),
                  (0, 1, 1),
                  (0, 2, 2),
                  (1, 0, 7),
                  (0, 3, 1),
                  (0, 4, 1),
                  (0, 5, 1),
                  (0, 6, 2),
                  (1, 0, 1),
                  (1, 0, 2),
                  (1, 0, 7),
                  (1, 6, 7),
                  (1, 2, 7),
                  (1, 2, 6),
              ]
             ),
            )
DATA = tuple((1, ("hardcoded", n, r, R)) for n, r, R in HARDCODED)
DATA = DATA + (( 8, ("rand_gen",    10,    20)),
               (10, ("rand_gen",  1000,  1000)),
               (30, ("rand_gen",  5000,  1000)),
              )
MAPPER = {"esempi_testo": 2, "small": 3, "medium": 4, "big": 5}




#################################################################


def gen_tc(*args):
    gen_type = args[0]
    if gen_type == "hardcoded":
        n, r, R = args[1:]
    else:
        n, r = args[1:]
        R = []
        for i in range(r):
            if i % 5 == 0:
                pos = random.randrange(n)
                delta = random.randrange(10)
                R.append( (0, pos, delta) )
            else:
                size = random.randint(1, n)
                a = random.randint(0, n - size)
                R.append( (1, a, a + size) )
    return (n, r, R)

def check_tc(n, r, R):
    F = Fenwick(n)
    print(f"{n} {r}")
    print(f"{n} {r}", file = stderr)
    wrongs = ""
    for r in R:
        req_string = " ".join(map(str, r))
        print(req_string)
    stdout.flush()
    for r in R:
        print(req_string, file = stderr)
        if r[0] == 1:
            risp_val = int(input())
            corr_val = F.sum(*r[1:])
            print(f"{corr_val=}, {risp_val=}", file=stderr)
            if risp_val != corr_val:
                if len(wrongs) == 0:
                    wrongs = f"With reference to the array:\n{array_as_str(F.M)}\nyou stated that:\n"
                wrongs += f"   sum({r[1:]}) = {risp_val} (whereas sum{r[1:]} = {corr_val})\n"
        else:
            F.update(*r[1:])
    if len(wrongs) == 0:
        return True
    else:
        return False, wrongs


if __name__ == "__main__":
    size = MAPPER[os.environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
