#!/usr/bin/env python3
from os import environ
from sys import stderr
from random import randrange, randint
from functools import lru_cache

from tc import TC

from rand_trees import random_tree_any_degree, random_tree_degree_at_most_2, random_binary_tree

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"esempi_testo": 1, "small": 2, "medium": 3, "big": 4, "huge_binary": 5, "huge_max_2_children": 6, "huge": 7}
DATA = ((2,  (random_tree_any_degree,  5,  6)),
        (20, (random_tree_any_degree,  8, 10)),
        (20, (random_tree_any_degree, 95, 100)),
        (20, (random_tree_any_degree, 9500, 10000)),
        (14, (random_binary_tree, 95000, 100000)),
        (14, (random_tree_degree_at_most_2, 95000, 100000)),
        (20, (random_tree_any_degree, 95000, 100000))
       )
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
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

def gen_tc(randtree_generator, minn, maxn):
    n = randint(minn, maxn)
    tree = randtree_generator(n)
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
