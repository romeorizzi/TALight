#!/usr/bin/env python3

from sys import stdin, stdout, stderr
from random import randrange, randint

class Array:
    
    def __init__(self, A = None):
        if A == None:
            self.n = int(input())
            self.A = []
            for _ in range(self.n):
                self.A.append(int(input()))
        else:
            self.A = A
            self.n = len(A)
        self.sum_of_first = [0] * (1 + self.n)
        for i in range(1, 1 + self.n):
            self.sum_of_first[i] = self.sum_of_first[i - 1] + self.A[i - 1]
            #print(self.sum_of_first[i], file = stderr)

    def sum(self, a, b):
        assert 0 <= a < b <= self.n
        return self.sum_of_first[b] - self.sum_of_first[a]
            
    def as_str(self, with_n = True):
        ret = f"{self.n}\n" if with_n else ""
        for i in range(self.n):
            ret +=  f"{self.A[i]}\n"
        return ret

    def display(self, out=stderr, with_n = True):
        print(self.as_str(with_n), file=out, end="", flush=True)
