#!/usr/bin/env python3
from sys import stderr, exit
from os import environ
import time

from quanti_poldo_lib import recognize, IncrSubseqs

S = list(map(int, environ["TAL_S"].split()))
rank = int(environ["TAL_input_rank"])
your_conj_shadow = list(map(int, environ["TAL_right_shadow"].split()))

if not recognize(S,your_conj_shadow):
    exit(0)

poldo = IncrSubseqs(S)

time.sleep(2)

if your_conj_shadow == poldo.unrankShadow(rank):
    print(f'♥  We agree.  It is indeed this one the increasing shadow of {rank=} for S.')
else:
    print(f"No. While you have indeed submitted a valid shadow of S, its rank is {poldo.rankShadow(your_conj_shadow)} and NOT {rank}. The true shadow of S with rank {rank} is:\n{poldo.unrankShadow(rank)}")
