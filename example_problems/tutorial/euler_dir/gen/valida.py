#!/usr/bin/env python

from limiti import *

from sys import argv, exit, stderr
import os

def usage():
    print >> stderr, "Usage: %s file_input.txt" % \
        os.path.basename(argv[0])
    exit(1)

def run(f):
    prima = [int(x) for x in f[0].split()]
    assert(len(prima) == 2)
    N,M = prima
    assert(1 <= N <= MAXN) 
    assert(1 <= M <= MAXM)
    degree=[0]*N
    for i in range(M):
        arco = [int(x) for x in f[i+1].split()]
        assert(len(arco)==2)
        u,v = arco
        assert(0 <= u < N)
        assert(0 <= v < N)
        assert(u != v)
        degree[u]+=1
        degree[v]-=1
    for i in range(N):
        assert(degree[i]==0)
    return 0 # Input corretto

if __name__ == "__main__":
    if len(argv) < 2:
        usage()

    f = open(argv[1]).readlines()
    exit(run(f))


