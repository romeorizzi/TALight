#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:55:02 2021

@author: Aurora Rossi
"""

def dec_to_bin(n):
    'da decimale a binario'
    b=0
    i=0
    while n>0:
        if n%2==0:
            b+=0*(10**i)
        else:
            b+=1*(10**i)
        i+=1   
        n=int(n/2)
    return b

