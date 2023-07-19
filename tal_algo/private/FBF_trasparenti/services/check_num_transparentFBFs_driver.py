#!/usr/bin/env python3
from sys import stderr, exit
from os import environ
import time

from FBF_trasparenti_lib import Par

time.sleep(5)

n_pairs = int(environ["TAL_n_pairs"])
risp = int(environ["TAL_risp"])
p = Par(n_pairs)
risp_correct = p.num_twffs[n_pairs]

if risp == risp_correct:
    if risp_correct < 1000000007:
        print(f'♥  We agree. The number of well-formed formulas with {n_pairs} pairs of open-closed parentheses is precisely {risp}.')
    else:
        print(f'♥  We agree. The number of well-formed formulas with {n_pairs} pairs of open-closed parentheses is congruent to {risp} modulo 1000000007.')
    exit(0)

if risp >= 1000000007:
    print(f'No. The well-formed formulas with {n_pairs} pairs of open-closed parentheses are not {risp}.')
elif risp_correct % 1000000007 == risp:
    print(f'♥  We agree. The number of well-formed formulas with {n_pairs} pairs of open-closed parentheses is congruent to {risp} modulo 1000000007.')    
else:
    print(f'No. The number of well-formed formulas with {n_pairs} pairs of open-closed parentheses is NOT congruent to {risp} modulo 1000000007.')
