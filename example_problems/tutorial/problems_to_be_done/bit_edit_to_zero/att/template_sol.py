#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Soluzione di bit_edit_to_zero

from __future__ import print_function
import sys

if sys.version_info < (3, 0):
    input = raw_input # in python2, l'equivalente di input è raw_input

#################################################
# BEGIN: parte di tua competenza

def num_mosse(n):
    return 43

def mossa(n):
    assert n > 0
    return 1

# END: parte di tua competenza
#################################################
    
    
p, n = map(int, input().strip().split())
assert 1 <= p <= 2
assert n >= 0
if p  == 1:
    print(num_mosse(n))
if p  == 2:
    print(mossa(n))
    
