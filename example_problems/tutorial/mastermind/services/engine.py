#!/usr/bin/env python3
from random import seed, randint

def check(sol: str, mine: str):
    solarray = sol.split(" ")
    minearray = mine.split(" ")

    pos = 0
    col = 0

    for x in range(0, len(solarray)):
        if (solarray[x] == minearray[x]):
            pos = pos + 1
            solarray[x] = "0"
            minearray[x] = "0"

    for x in range(0, len(solarray)):
        f = False

        for y in range(0, len(solarray)):
            if not x == y and not solarray[x] == "0" and not minearray[y] == "0" and not f:
                if (solarray[x] == minearray[y]):
                    col = col + 1
                    solarray[x] = "0"
                    minearray[y] = "0"
                    f = True
                    
    return pos, col

def generatesol(lensol: int, numchar: int):
    s = ""
    for i in range(0, lensol):
        s = s + " " + chr(65 + randint(0, numchar - 1))

    return s.strip()

def isCorrect(lensol: int, numchar: int, step: int):
    """
    False Wrong
    True Correct
    """

    t = 0
    
    while t < step:
        mysol = generatesol(lensol, numchar)
        myprob = generatesol(lensol, numchar)

        pos, col = check(mysol, myprob)

        otherpos = input()
        othercol = input()

        if (otherpos != pos or othercol != col):
            return False

        t = t + 1

    return True

def play(lensol: int, numchar: int, step: int):
    """
    True WIN
    False LOST
    """

    sol = generatesol(lensol, numchar)

    t = 0
    while t < step:
        line = input()
        pos, col = check(sol, line)

        print(pos, col, sep=" ")
        if (pos == numchar):
            return True

        t = t + 1

    print(sol)
    return False
    