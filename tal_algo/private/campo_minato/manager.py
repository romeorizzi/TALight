#!/usr/bin/env python3

from functools import lru_cache
from os import environ
from random import randrange, randint
from tc import TC

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "big": 4}
DATA = ((10, (5,6)), (10, (8,10)), (10, (18,20)), (70, (25,30)))
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
#################################################################


def sol(M):
    m = len(M)
    n = len(M[0])
    V = [[0] * (n + 1) for i in range(m + 1)]
    V[m - 1][n - 1] = int(M[m - 1][n - 1])
    for i in reversed(range(m)):
        for j in reversed(range(n)):
            if i == m - 1 and j == n - 1:
                continue
            if M[i][j]:
                V[i][j] = (V[i + 1][j] + V[i][j + 1])
    return V[0][0]

def display_griglia(M):
    m = len(M)
    n = len(M[0])
    for i in range(m):
        print("".join(map(lambda x: "." if x else "#", M[i])))

def gen_tc(minn,maxn):
    m, n = randint(minn,maxn), randint(minn,maxn)
    M = [[bool(randrange(0, 10)) for j in range(n)] for i in range(m)]
    M[0][0] = M[m-1][n-1] = True
    r=0; c=0
    while r<m-1 and c<n-1:
        if M[r+1][c]:
            r += 1
        elif M[r][c+1]:
            c += 1
        elif randint(0,1) == 1:
            M[r+1][c] = True
            r += 1
        else:
            M[r][c+1] = True
            c += 1
    while r<m-1:
        M[r+1][c] = True
        r += 1
    while c<n-1:
        M[r][c+1] = True
        c += 1
    print(m, n)
    display_griglia(M)
    return (M,)


def check_tc(M):
    risp = int(input())
    corr_answ = sol(M)
    if risp != corr_answ:
        return False, f"On input:\n{display_griglia(M)}\nyou answered:\n{risp}\nwhile the correct answer was:\n{corr_answ}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
