#!/usr/bin/env python3
from sys import stderr, exit
from os import environ
import time

from FBF_trasparenti_lib import recognize, Par

rank = int(environ["TAL_input_rank"])
FBF = environ["TAL_right_FBF"]

if not recognize(FBF):
    exit(0)

time.sleep(5)

n_pairs = len(FBF)//2
p = Par(n_pairs)
if FBF == p.unrankFBF_t(n_pairs, rank):
    print(f'♥  We agree.  It is indeed this one the formula of {rank=} among the well formed formulas on {n_pairs} pairs of parentheses.')
else:
    print(f"No. Your formula does not rank {rank} among those with {n_pairs} pairs of parentheses.")
