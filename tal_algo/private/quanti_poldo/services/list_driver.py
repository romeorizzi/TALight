#!/usr/bin/env python3
from sys import stderr, exit
from os import environ
import time

from quanti_poldo_lib import IncrSubseqs

S = list(map(int, environ["TAL_S"].split()))
poldo = IncrSubseqs(S)
for rnk in range(poldo.num_nonleft[0]):
    shadow = poldo.unrankShadow(rnk)
    print(" ".join(map(str, shadow)))
