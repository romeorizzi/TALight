#!/usr/bin/env python3

from sys import stdin, stdout, stderr
from random import randrange, randint


MAXN = 100000
LSB = [ None ] * (MAXN + 1)   # meant to store the least significant bit of n
for n in range(1, MAXN + 1): 
    if n % 2 == 1:
        LSB[n] = 1
    else:
        LSB[n] = 2*LSB[n//2]
# now LSB[n] = the smallest power of 2 in the unique decomposition of n as a sum of _different_ powers of 2
        
        
#the following implementation is unfortunately slow in python:
#def lsb(n):   # the least significant bit of n
#    """returns the smallest power of 2 in the unique decomposition of n as a sum of _different_ powers of 2"""
#    assert n > 0
#    return n & (-n)



def array_as_str(A):
    return " ".join(map(str, A))

def display_array(A, out=stderr):
    print(array_as_str(A), file=out)


class Fenwick:
# Python implementation of BIT (Binary Indexed Tree, also called Fenwick tree)
    
    def __init__(self, n):
        self.n = n
        self.A = [0] * self.n
        self.Fenwick = [0]*(self.n+1)

    def sum_from_00_to(self, i):
        """returns the total sum over A[0..i]"""
        assert i >= -1
        ans = 0
        i += 1   # indexes in Fenwick trees start from 1 rather than from 0 like in the represented array A
        while i > 0:
            ans += self.Fenwick[i]
            i -= LSB[i]
        return ans

    def sum(self, a, b):
        """returns the total sum over A[a..b)"""
        assert 0 <= a < b <= self.n
        return self.sum_from_00_to(b - 1) - self.sum_from_00_to(a - 1)

    
    def update(self, i, delta):
        """Updates A[i] to A[i] + delta (Also updates the Fenwick trees structure accordingly)"""
        assert i <= self.n
        self.A[i] += delta
        i += 1   # indexes in Fenwick trees start from 1 rather than from 0 like in the represented array A
        while i <= self.n:
            self.Fenwick[i] += delta
            i += LSB[i]


