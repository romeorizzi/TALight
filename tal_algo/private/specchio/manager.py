#!/usr/bin/env python3
from os import environ
from sys import stderr, setrecursionlimit
from random import randrange, randint
from functools import lru_cache

from tc import TC

from rand_trees import random_tree_any_degree, random_tree_at_most_2_children, random_binary_tree

setrecursionlimit(100000)

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

HARDCODED = (
             [4, 2, 0, 3, 0, 0, 1, 0, 0, 0, 0],
             [4, 0, 0, 0, 2, 3, 1, 0, 0, 0, 0]
            )
DATA = tuple((1, (lambda x : x, h)) for h in HARDCODED)
DATA = DATA + (
               (21, (random_tree_any_degree,  8, 10)),
               (22, (random_tree_any_degree, 95, 100)),
               (16, (random_binary_tree, 95000, 100000)),
               (16, (random_tree_at_most_2_children, 95000, 100000)),
               (23, (random_tree_any_degree, 95000, 100000))
              ) 
MAPPER = {"esempi_testo": 2, "small": len(HARDCODED) +1, "medium": len(HARDCODED) +2, "big_binary": len(HARDCODED) +3, "big_max_2_children": len(HARDCODED) +4, "big": len(HARDCODED) +5}
#################################################################

def as_str(tree):
    return " ".join(map(str, tree))

def specchia(input_tree):
    pos_Read = 0
    mirrored_tree_reversed = []

    def reverso_write_mirrored_tree():
        nonlocal pos_Read
        n_figli = input_tree[pos_Read]
        pos_Read += 1
        for _ in range(n_figli):
            reverso_write_mirrored_tree()
        mirrored_tree_reversed.append(n_figli)

    reverso_write_mirrored_tree()
    return list(reversed(mirrored_tree_reversed))

def gen_tc(*args):
    tree = args[0](*args[1:])
    print(" ".join(map(str, tree)))
    #print(f'PRINTED: {" ".join(map(str, tree))}', file=stderr)
    return (tree,)


def check_tc(input_tree):
    #print(f"{input_tree=}", file=stderr)
    risp_tree = list(map(int, input().strip().split()))
    #print(f"{risp_tree=}", file=stderr)
    corr_tree = specchia(input_tree)
    #print(f"{corr_tree=}", file=stderr)
    if risp_tree != corr_tree:
        return False, f"On input:\n{as_str(input_tree)}\nyou answered:\n{as_str(risp_tree)}\nwhile the correct answer was:\n{as_str(corr_tree)}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
