# -*- coding: utf-8 -*-
# Template di soluzione per bit_edit_to_zero

from __future__ import print_function
import sys

if sys.version_info < (3, 0):
    input = raw_input # in python2, l'equivalente di input è raw_input

#################################################
# INIZIO area entro la quale ti richiediamo/consigliamo di operare.
    
def num_mosse(n):
    return 43

def mossa(n):
    assert n > 0
    return 1

# FINE area entro la quale ti richiediamo/consigliamo di operare.
#################################################
    
    
p, n = map(int, input().strip().split())
assert 1 <= p <= 2
assert n >= 0
if p  == 1:
    print(num_mosse(n))
if p  == 2:
    print(mossa(n))
    
