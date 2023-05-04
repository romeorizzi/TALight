#!/usr/bin/env python3

WARNING = """this library is common to a few problems:
../interval_sum
../interval_sum_dyn
Please, keep this in mind in case you want to modify it."""

from sys import stdin, stdout, stderr
from random import randrange, randint

class Field:
    
    def __init__(self, M = None):
        if M == None:
            self.n1, self.n2 = map(int, input().strip().split())
            self.M = []
            for _ in range(self.n1):
                self.M.append(list(map(int, input().strip().split())))
        else:
            self.M = M
            self.n1 = len(M)
            self.n2 = len(M[0])
        self.sum_from_O = [ [0] * (1 + self.n2) for _ in range(1 + self.n1) ]
        for i in range(1, 1 + self.n1):
            for j in range(1, 1 + self.n2):
                self.sum_from_O[i][j] = self.sum_from_O[i - 1][j] + self.sum_from_O[i][j - 1] + self.M[i -1][j -1] - self.sum_from_O[i - 1][j - 1]
                #print(self.sum_from_O[i][j], end = " ", file = stderr)
            #print(file = stderr)

    def sum(self, a1, b1, a2, b2):
        assert 0 <= a1 < b1 <= self.n1
        assert 0 <= a2 < b2 <= self.n2
        return self.sum_from_O[b1][b2] - self.sum_from_O[b1][a2] - self.sum_from_O[a1][b2] +  self.sum_from_O[a1][a2]
            
    def as_str(self, with_n1_n2 = True):
        ret = f"{str(self.n1)} {str(self.n2)}\n" if with_n1_n2 else ""
        ret +=  " ".join(map(str, self.M[0]))
        for i in range(1, self.n1):
            ret += "\n" + " ".join(map(str, self.M[i]))
        return ret

    def display(self, out=stderr, with_n1_n2 = True):
        print(self.as_str(with_n1_n2), file=out, flush=True)




if __name__ == "__main__":
    print(WARNING)    
    
