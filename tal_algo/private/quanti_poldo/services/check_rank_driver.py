#!/usr/bin/env python3
from sys import stderr, exit
from os import environ
import time

from quanti_poldo_lib import recognize, IncrSubseqs

S = list(map(int, environ["TAL_S"].split()))
shadow = list(map(int, environ["TAL_input_shadow"].split()))
conj_rank = int(environ["TAL_right_rank"])

if not recognize(S,shadow):
    exit(0)

poldo = IncrSubseqs(S)

time.sleep(2)

if conj_rank == poldo.rankShadow(shadow):
    print(f'♥  We agree. You correctly ranked that shadow of S among the increasing shadows of S.')
else:
    print(f"No. While you have indeed submitted a valid shadow of S, its rank is {poldo.rankShadow(shadow)} and NOT {conj_rank}.")

