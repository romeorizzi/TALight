#!/usr/bin/env python3
from os import environ
from sys import stderr, stdout
import random

from tc import TC

from quanti_poldo_lib import IncrSubseqs

############## TESTCASES' PARAMETERS ############################
TL = 2   # the time limit for each testcase

HARDCODED = (
             ([1, 6, 2, 5, 3, 4], 1, [], []),
             ([1, 6, 2, 5, 3, 4], 0, [
                  [0, 1],
                  [0, 2, 3],
                  [0, 2, 4],
                  [0, 4, 5],
                  [0, 5],
                  []
                 ], []),
             ([1, 6, 2, 5, 3, 4], 0, [], [0, 1, 3, 21, 7, 9]),
            )
DATA = tuple((1, ("hardcoded", len(S), S, c, len(Shadows), len(Ranks), Shadows, Ranks)) for S, c, Shadows, Ranks in HARDCODED) + (
            ( 9, ("rand_gen",  10, 1,   0,   0)),
            (11, ("rand_gen",  10, 0,  20,   0)),
            (11, ("rand_gen",  10, 0,   0,  20)),
            (11, ("rand_gen",  20, 1,   0,   0)),
            (11, ("rand_gen",  20, 0,  50,   0)),
            (11, ("rand_gen",  20, 0,   0,  50)),
            (11, ("rand_gen", 200, 1,   0,   0)),
            (11, ("rand_gen", 200, 0, 200,   0)),
            (11, ("rand_gen", 200, 0,   0, 500)),
        )
MAPPER = {"esempi_testo": 3, "small_c": 4, "small_r": 5, "small_u": 6, "medium_c": 7, "medium_r": 8, "medium_u": 9, "big_c": 10, "big_r": 11, "big_u": 12}
#################################################################


def gen_tc(*args):
    gen_type = args[0]
    if gen_type != "rand_gen":
        n, S, c, r, u, Shadows_given, Ranks_given = args[1:]
        poldo = IncrSubseqs(S)
        num_tot_shadows = poldo.num_nonleft[0]
        corr_ranks = [poldo.rankShadow(sub) for sub in Shadows_given]
    else:
        n, c, r, u = args[1:]
        num_tot_shadows = -1
        while num_tot_shadows < max(r, u):
            print(f"Gen: num_tot_shadows < max(r, u) ({num_tot_shadows} < {max(r, u)}) ", file=stderr)
            S = [ random.randint(1, 9) for _ in range(n)]
            poldo = IncrSubseqs(S)
            num_tot_shadows = poldo.num_nonleft[0]
        print(f"{num_tot_shadows=}, {r=}", file=stderr)
        corr_ranks = list( random.sample(range(min(num_tot_shadows, 1000000006) ), r) )
        Shadows_given = [ poldo.unrankShadow(rnk) for rnk in corr_ranks ]
        print(f"{num_tot_shadows=}, {u=}", file=stderr)
        Ranks_given = list( random.sample(range(min(num_tot_shadows, 1000000006)), u) )
    corr_Shadows = [ poldo.unrankShadow(rnk) for rnk in Ranks_given ]
    print(n, c, r, u)
    print(" ".join(map(str, S)))
    for shadow in Shadows_given:
        print(" ".join(map(str, shadow)))
    print(" ".join(str(rnk) for rnk in Ranks_given))
    stdout.flush()
    return (S, c, r, u, num_tot_shadows, Shadows_given, corr_ranks, Ranks_given, corr_Shadows)


def check_tc(S, c, r, u, num_tot_shadows, Shadows_given, corr_ranks, Ranks_given, corr_Shadows):
    print(f"{S=}, {c=}, {r=}, {u=}, {num_tot_shadows=}, {Shadows_given=}, {corr_ranks=}, {Ranks_given=}, {corr_Shadows=}", file=stderr)

    feedback = None
    risp_c = input()
    if c > 0:
        risp_c = int(risp_c)
        if risp_c != num_tot_shadows and risp_c != num_tot_shadows % 1000000007:
            feedback = f"The number of shadows of S is not {risp_c}. Here {S=}."
    risp_r = input()
    if r > 0:
        risp_ranks = list( map(int, risp_r.strip().split()) )
        if len(risp_ranks) != r:
            feedback = f"I have given you {r} shadows of S and so I was expacting your line to contain {r} ranks (integers separated by spaces) rather than {len(risp_ranks)}."
        for shadow, corr_r, risp_r in zip(Shadows_given, corr_ranks, risp_ranks):
            if risp_r != corr_r:
                feedback = f"No. The correct rank is {corr_r} and NOT the number {risp_r} you have returned as the rank of\n increasing {shadow=}\n of {S=}."
    if u > 0:
        for rnk, corr_shadow in zip(Ranks_given, corr_Shadows):
            risp_shadow =  list( map(int, input().strip().split()) )
            if risp_shadow != corr_shadow:
                feedback = f"No. The correct increasing shadow for S of rank {rnk} is NOT:\n {risp_shadow}\nbut {corr_shadow}\nHere {S=}."

    if feedback is None:
        return True
    else:
        return False, feedback


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
