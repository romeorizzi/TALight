#!/usr/bin/env python3

import random
import itertools
import copy


P = []
S = []
prevGuesses = []
numPegs = 4
numColours = 6
firstGuess = [1, 1, 2, 2]
recentGuess = firstGuess
guessCount = 1


def setup(): 
    global P
    global S
    r = []

    for i in range(1, numColours + 1):
        r.append(i)
    comb = itertools.product(r, repeat=numPegs)
    for i in comb:
        P.append(list(i))
    S = copy.deepcopy(P)


def doAttempt(value):
    print(' '.join(map(str, value)))
    while True:
        spoon = input().strip()
        buffer = spoon.split()
        if len(buffer) > 0 and (buffer[0] == 'b' or buffer[0] == 'w'):
            blackPegs = buffer.count('b')
            whitePegs = buffer.count('w')
            return blackPegs, whitePegs


def countBlackPegs(code, guess):
    blackPegs = 0
    for i in range(len(guess)):
        if (guess[i] == code[i]):
            blackPegs += 1
    
    return blackPegs


def countWhitePegs(code, guess):
    tempCode = code[:]
    whitePegs = 0
    for i in guess:
        if (i in tempCode):
            tempCode.remove(i)
            whitePegs += 1
    
    return whitePegs


def countPegs(code, guess):        
    blackPegs = countBlackPegs(code, guess)
    whitePegs = countWhitePegs(code, guess)
    whitePegs -= blackPegs
    return blackPegs, whitePegs


def removeImpossible(recentBlackPegs, recentWhitePegs):
    global S
    global recentGuess
    tempS = copy.deepcopy(S)
    for code in tempS:
        blackCount, whiteCount = countPegs(code, recentGuess)
        if (blackCount != recentBlackPegs or whiteCount != recentWhitePegs):
            S.remove(code)


def findMaxHitCount(groups):
    grpHitCount = 0
    maxHitCount = 0
    for key, group in groups:
        grpHitCount = len(list(group))
        if (grpHitCount > maxHitCount):
            maxHitCount = grpHitCount
    return maxHitCount


def startAlgo():
    setup()
    global P
    global S
    global prevGuesses
    global firstGuess
    global recentGuess
    global guessCount

    recentBlackPegs, recentWhitePegs = doAttempt(firstGuess)
    removeImpossible(recentBlackPegs, recentWhitePegs)
    prevGuesses.append(firstGuess)
    while recentBlackPegs != 4:
        groups = []
        bestMinEliminated = []
        bestGuesses = []
        for guess in P:
            if (not guess in prevGuesses):
                data = sorted(S, key=lambda x: (countPegs(guess, x)))
                groups = itertools.groupby(data, lambda x: (countPegs(guess, x)))
                maxHitCount = findMaxHitCount(groups)
                minEliminated = len(S) - maxHitCount
                bestMinEliminated.append(minEliminated)
                bestGuesses.append(guess)
        maxMinEliminated = max(bestMinEliminated)
        indices = [index for index, value in enumerate(bestMinEliminated) if value == maxMinEliminated]
        nextGuess = []
        flagFirstGuess = True
        for i in indices:
            if (bestGuesses[i] in S):
                nextGuess = bestGuesses[i]
                break
            elif (flagFirstGuess):
                nextGuess = bestGuesses[i]
                flagFirstGuess = False
        guessCount +=1
        recentGuess = nextGuess
        recentBlackPegs, recentWhitePegs = doAttempt(nextGuess)
        removeImpossible(recentBlackPegs, recentWhitePegs)
        prevGuesses.append(recentGuess)

    print('#end')
    spoon = input().strip()


spoon = input().strip()
while spoon[:len("#? waiting for ")] != "#? waiting for ":
    spoon = input().strip()
    assert spoon[0] == "#"
startAlgo()