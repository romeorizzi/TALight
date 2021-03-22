#!/usr/bin/env python3
# problem: lightCoin, Romeo Rizzi Jan 2015

import sys

NONE = 0
LEFT = -1
RIGHT = 1

nMonete = 0
lightCoin = 0
nLeft = 0
nRight = 0
nPesate = 0
maxPesate = 0

subtask = 0
outfile = None
piatto = None

def mylog(b, n):
    risp = 0
    reached = 1
    while reached < n:
        risp += 1
        reached *= b
    return risp


def collocaMoneta(moneta, piatto_target):
    global nLeft, nRight, piatto
    if piatto[moneta] == LEFT:
        nLeft -= 1
    if piatto[moneta] == RIGHT:
        nRight -= 1

    piatto[moneta] = piatto_target

    if piatto[moneta] == LEFT:
        nLeft += 1
    if piatto[moneta] == RIGHT:
        nRight += 1


def piatto_con_peso_maggiore():
    global nLeft, nRight, nPesate, piatto, lightCoin

    nPesate += 1
    if nLeft > nRight:
        return LEFT
    if nRight > nLeft:
        return RIGHT
    if piatto[lightCoin] == NONE:
        return NONE
    if piatto[lightCoin] == LEFT:
        return RIGHT
    if piatto[lightCoin] == RIGHT:
        return LEFT
    assert(False)


def denuncia(risp):
    global outfile
    print("%d %d %d" % (risp, nPesate, maxPesate), file=outfile)
    sys.exit(0)


def ottieni_numero_monete():
    global nLeft, nRight, nPesate, outfile, maxPesate, lightCoin, piatto
    nLeft = nRight = nPesate = 0

    infile = open("input.txt", "r")
    # infile = sys.stdin

    lightCoin, nMonete, subtask = [int(x.strip()) for x in infile.read().split()]
    infile.close()

    piatto = [0] * nMonete

    outfile = open("output.txt", "w")
    # outfile = stdout

    maxPesate = 10 * nMonete
    if subtask == 2:
        assert(nMonete == 7)
        maxPesate = 6
    if subtask == 3:
        assert(nMonete == 7)
        maxPesate = 4
    if subtask == 4:
        assert(nMonete == 7)
        maxPesate = 3
    if subtask == 5:
        assert(nMonete == 8)
        maxPesate = 3
    if subtask == 6:
        maxPesate = nMonete - 1
    if subtask == 7:
        maxPesate = nMonete // 2
    if subtask == 8:
        maxPesate = mylog(2, nMonete)
    if subtask == 9:
        maxPesate = mylog(3, nMonete)

    return nMonete
