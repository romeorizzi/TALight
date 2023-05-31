#!/usr/bin/env python3

from sys import stderr, stdout
from os import environ
from random import randrange, randint

from tc import TC

from campo_minato_lib import CampoMinato

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "big": 4}
DATA = ((10, (5,6)), (10, (8,10)), (10, (18,20)), (70, (25,30)))
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
#################################################################
def campo_rank_display(campo, k):
    ret = f"{str(campo.m)} {str(campo.n)} {str(k)}\n"
    ret += "".join(map(lambda x: "." if x else "#", campo.M[0]))
    for i in range(1, campo.m):
        ret += "\n" + "".join(map(lambda x: "." if x else "#", campo.M[i]))
    return ret

def gen_tc(minn, maxn):
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
    campo = CampoMinato(M)
    routes = campo.num_paths_from_ric_memo(0, 0)
    k = randint(0, routes-1)
    print(campo_rank_display(campo, k), file=stdout, flush=True)
    return (campo, k)


def check_tc(campo, k):
    print()
    risp = input().strip()
    corr_answ = campo.rank_safe(k)
    if risp != corr_answ:
        return False, f"On input:\n{campo_rank_display(campo, k)}\nyou answered:\n{risp}\nwhile the correct answer was:\n{corr_answ}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)