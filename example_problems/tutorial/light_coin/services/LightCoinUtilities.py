import sys
import random


NONE = 0
LEFT = -1
RIGHT = 1


def getRandomFalseCoinPosition(coinsNum, seed="any"):
    if seed=="any":
        random.seed()
        seed = random.randrange(0,1000000)
    else:
        seed = int(seed)
    random.seed(seed)
    falseCoinPosition = random.randrange(1, coinsNum + 1)
    return falseCoinPosition, seed

def getInputScale(inputMsg, erroMsg, TAc):
    while True:
        try:
            TAc.print(inputMsg, "yellow", ["bold"])
            tmpInput = input()
            coinsInScale = [int(part) for part in tmpInput.split()]
            return coinsInScale
        except ValueError:
            TAc.print(erroMsg, "red", ["bold"])

def getHeavierScale(leftScale, rightScale, falseCoinPos):
    if len(leftScale) > len(rightScale):
        return LEFT
    elif len(leftScale) < len(rightScale):
        return RIGHT
    else:
        if falseCoinPos in leftScale:
            return LEFT
        elif falseCoinPos in rightScale:
            return RIGHT
        else:
            return NONE

def getLighterScale(leftScale, rightScale, falseCoinPos):
    if len(leftScale) > len(rightScale):
        return RIGHT
    elif len(leftScale) < len(rightScale):
        return LEFT
    else:
        if falseCoinPos in leftScale:
            return LEFT
        elif falseCoinPos in rightScale:
            return RIGHT
        else:
            return NONE