#!/usr/bin/env python3
from random import seed, randint

def evaluate(secret, probe):
    assert len(secret) == len(probe)
    black = 0
    counter = {}
    for a,b in zip(secret, probe):
        if a == b:
            black += 1
        if a in counter:
            counter[a][0] += 1
        else:
            counter[a] = [1,0]
        if b in counter:
            counter[b][1] += 1
        else:
            counter[b] = [0,1]
    print(counter)
    sum_of_mins = 0
    for num1,num2 in counter.values():
        sum_of_mins += min(num1,num2) 
    return black, sum_of_mins - black


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
    
