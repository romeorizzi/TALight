#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Soluzione di bit_edit_to_zero

from __future__ import print_function
import sys

if sys.version_info < (3, 0):
    input = raw_input # in python2, l'equivalente di input è raw_input

#################################################
    
def lsp(n):
    return n & (-n)

def is_power_of_2(n):
    return n == lsp(n)

def num_mosse_for_powers_of_two(n):
    assert is_power_of_2(n)
    return 2*n-1

def num_of_ones_in_binary_rep(n):
    if n == 0:
        return 0
    return 1 + num_of_ones_in_binary_rep(n - lsp(n))

def num_mosse(n):
    if n==0:
        return 0
    if num_of_ones_in_binary_rep(n) % 2 == 1:
        return num_mosse_for_powers_of_two(lsp(n)) + num_mosse(n-lsp(n))
    if lsp(n-lsp(n)) == 2*lsp(n):
        return 1 + num_mosse(n - 2*lsp(n))
    else:
        return 1 + num_mosse(n + 2*lsp(n))


def mossa(n):
    assert n > 0
    if num_of_ones_in_binary_rep(n) % 2 == 1:
        return 1
    else:
        return 2

#    n | num_mosse
#    1 |  1
#   10 |  3 = 1 + 1 + 1
#  100 |  7 = 3 + 1 + 3
# 1000 | 15 = 7 + 1 + 7 

#########################################

    
p, n = map(int, input().strip().split())
assert 1 <= p <= 2
assert n >= 0
if p  == 1:
    print(num_mosse(n))
if p  == 2:
    print(mossa(n))
    
