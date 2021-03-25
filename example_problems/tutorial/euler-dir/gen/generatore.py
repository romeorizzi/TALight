#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Generatore per euler-dir:
# Scelgo un nodo a caso come inizio ed ad ogni step scelgo un vicino a caso
# Alla fine riordino gli archi in maniera casuale
# NOTA BENE: c'e la possibilita di finire in un nodo senza uscita! in quel caso il programma va in ciclo infinito. non mi é ancora capitato, in caso diminuire il numero di archi o cambiare il seed

from limiti import *

usage="""Generatore per "euler-dir".

Parametri:
* N (numero di nodi)
* M (numeri di archi)
* S (seed)

Constraint:
* 1 <= N <= %d
* 1 <= M <= %d
""" % (MAXN, MAXM)

from sys import argv, exit, stderr
import os
from numpy.random import random, randint, seed as nseed
from random import choice, sample, shuffle, randrange, seed as rseed

def run(N, M, S):
    nseed(S)
    rseed(S)
    edges = []
    start = 0
    cur = start

    # Inizia con un super-ciclo, tanto per farlo connesso
    for i in xrange(0, N):
        edges.append((i, (i+1)%N))

    # E poi tutto il resto, a caso
    for i in xrange(N, M-1):
        next = randrange(0, N)
        while next == cur:
            next = randrange(0, N)
        edges.append((cur, next))
        cur = next
    edges.append((cur, 0));

    # Genera una permutazione dei vertici
    perm = range(N)
    shuffle(perm)

    print N, M
    for edge in edges:
        print perm[edge[0]], perm[edge[1]]

if __name__ == "__main__":
    if len(argv) != 4:
        print usage
        exit(1)
    N, M, S = [int(x) for x in argv[1:]]
    assert (1 <= N <= MAXN)
    assert (1 <= M <= MAXM)
    run(N, M, S)
