#!/usr/bin/env python3
from sys import stderr, exit
from os import environ
import time

from quanti_poldo_lib import recognize, IncrSubseqs

S = list(map(int, environ["TAL_S"].split()))
risp = int(environ["TAL_risp"])

poldo = IncrSubseqs(S)

time.sleep(2)

risp_correct = poldo.num_nonleft[0]

if risp == risp_correct:
    if risp_correct < 1000000007:
        print(f'♥  We agree. The number of increasing shadows of S is precisely {risp}.')
    else:
        print(f'♥  We agree. The number of increasing shadows of S is congruent to {risp} modulo 1000000007.')
    exit(0)

if risp >= 1000000007:
    print(f'No. The number of increasing shadows of S is not {risp} but {risp_correct}.')
elif risp_correct % 1000000007 == risp:
    print(f'♥  We agree. The number of increasing shadows of S is congruent to {risp} modulo 1000000007.')    
else:
    print(f'No. The number of increasing shadows of S is NOT congruent to {risp} modulo 1000000007. The true number is {risp_correct}.')
