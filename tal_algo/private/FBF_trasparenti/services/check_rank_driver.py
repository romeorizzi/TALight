#!/usr/bin/env python3
from sys import stderr, exit
from os import environ
import time

from FBF_trasparenti_lib import recognize, Par

FBF = environ["TAL_input_FBF"]
rank = int(environ["TAL_right_rank"])

if not recognize(FBF):
    exit(0)

time.sleep(5)

n_pairs = len(FBF)//2 
p = Par(n_pairs)

if rank == p.rankFBF_t(FBF):
    print(f'♥  We agree. You correctly ranked that formula among those on {n_pairs} pairs of parentheses.')
else:
    print(f'No. The rank of that formula among the other formulas on {n_pairs} pairs of parentheses is not {rank}.')
    
