#!/usr/bin/env python3

WARNING = """this library is common to a few problems:
../interval_sum_dyn
Please, keep this in mind in case you want to modify it."""

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



def matrix_as_str(M):
    ret =  " ".join(map(str, M[0]))
    for i in range(1, len(M)):
        ret += "\n" + " ".join(map(str, M[i]))
    return ret

def display_matrix(M, out=stderr):
    print(matrix_as_str(M), file=out)


class Fenwick:
# Python implementation of BIT (Binary Indexed Tree, also called Fenwick tree)
    
    def __init__(self, n1, n2):
        self.n1, self.n2 = n1, n2
        self.M = [ [0] * self.n2 for _ in range(self.n1) ]
        self.Fenwick = [ [0]*(self.n2+1) for _ in range(1 + self.n1) ]

    def sum_from_00_to(self, i, j):
        """returns the total sum over M[0..i][0..j]"""
        assert i >= -1
        assert j >= -1
        ans = 0
        i += 1; j += 1   # indexes in Fenwick trees start from 1 rather than from 0 like in the represented vector/matrix M
        while i > 0:
            jj = j
            while jj > 0:
                ans += self.Fenwick[i][jj]
                jj -= LSB[jj]  # Move to the parent node of node jj in the Fenwick tree Fenwick[i]
            i -= LSB[i]  # Move to the Fenwick-parent row of row i
        return ans

    def sum(self, a1, b1, a2, b2):
        """returns the total sum over M[a1..b1)[a2..b2)"""
        assert 0 <= a1 < b1 <= self.n1
        assert 0 <= a2 < b2 <= self.n2
        return self.sum_from_00_to(b1-1, b2-1) - self.sum_from_00_to(b1 -1, a2 -1) - self.sum_from_00_to(a1 -1, b2 -1) +  self.sum_from_00_to(a1 -1, a2 -1)

    
    def update(self, i, j, delta):
        """Updates M[i][j] to M[i][j] + delta (Also updates the Fenwick trees structure accordingly)"""
        assert i <= self.n1 
        assert j <= self.n2
        self.M[i][j] += delta
        i += 1; j += 1   # indexes in Fenwick trees start from 1 rather than from 0 like in the represented vector/matrix M
        while i <= self.n1:
            jj = j
            while jj <= self.n2:
                self.Fenwick[i][jj] += delta
                jj += LSB[jj]  # Move to the parent node of node jj in the Fenwick tree Fenwick[i]
            i += LSB[i]  # Move to the Fenwick-parent row of row i



if __name__ == "__main__":
    print(WARNING)    
    
