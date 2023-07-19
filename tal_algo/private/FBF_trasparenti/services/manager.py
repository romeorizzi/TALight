#!/usr/bin/env python3
from os import environ
from sys import stderr, stdout
import random

from tc import TC

from FBF_trasparenti_lib import recognize, Par

############## TESTCASES' PARAMETERS ############################
TL = 2   # the time limit for each testcase

HARDCODED = (
             (4, 1, [], []),
             (4, 0, ["(((())))", "(()(()))", "()(()())"], []),
             (4, 0, [], [0, 3, 7]),
            )
DATA = tuple((1, ("hardcoded", n, c, len(t_FBFs), len(Ranks), t_FBFs, R)) for n, c, t_FBFs, Ranks in HARDCODED) + (
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
        n, c, r, u, FBFs_given, Ranks_given = args[1:]
        p = Par(n)
        num_tot_transparentFBFs = p.num_twffs[n]
        corr_ranks = [p.rankFBF_t(fbf) for fbf in FBFs_given]
    else:
        n, c, r, u = args[1:]
        p = Par(n)
        num_tot_transparentFBFs = p.num_twffs[n]
        print(f"{num_tot_transparentFBFs=}, {r=}", file=stderr)
        corr_ranks = list( random.sample(range(min(num_tot_transparentFBFs, 1000000006) ), r) )
        FBFs_given = [ p.unrankFBF_t(n, rnk) for rnk in corr_ranks ]
        print(f"{num_tot_transparentFBFs=}, {u=}", file=stderr)
        Ranks_given = list( random.sample(range(min(num_tot_transparentFBFs, 1000000006)), u) )
    corr_FBFs = [ p.unrankFBF_t(n, rnk) for rnk in Ranks_given ]
    print(n, c, r, u)
    for fbf in FBFs_given:
        print(fbf)
    print(" ".join(str(rnk) for rnk in Ranks_given))
    stdout.flush()
    return (n, c, r, u, num_tot_transparentFBFs, FBFs_given, corr_ranks, Ranks_given, corr_FBFs)


def check_tc(n, c, r, u, num_tot_transparentFBFs, FBFs_given, corr_ranks, Ranks_given, corr_FBFs):
    print(f"{n=}, {c=}, {r=}, {u=}, {num_tot_transparentFBFs=}, {FBFs_given=}, {corr_ranks=}, {Ranks_given=}, {corr_FBFs=}", file=stderr)

    feedback = None
    risp_c = input()
    if c > 0:
        risp_c = int(risp_c)
        if risp_c != num_tot_transparentFBFs and risp_c != num_tot_transparentFBFs % 1000000007:
            feedback = f"The number of transparent FBFs on {n} pairs of parentheses is not {risp_c}."
    risp_r = input()
    if r > 0:
        risp_ranks = list( map(int, risp_r.strip().split()) )
        if len(risp_ranks) != r:
            feedback = f"I have given you {r} transparente formulas and so I was expacting your line to contain {r} ranks (integers separated by spaces) rather than {len(risp_ranks)}."
        for fbf, corr_r, risp_r in zip(FBFs_given, corr_ranks, risp_ranks):
            if risp_r != corr_r:
                feedback = f"No. The number {risp_r} you have returned is NOT the correct rank of the following transparent FBF:\n{fbf}"
    if u > 0:
        for rnk, corr_fbf in zip(Ranks_given, corr_FBFs):
            risp_fbf = input().strip()
            if risp_fbf != corr_fbf:
                feedback = f"No. The correct transparent FBF of rank {rnk} is NOT:\n{risp_fbf}"

    if feedback is None:
        return True
    else:
        return False, feedback


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
