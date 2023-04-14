#!/usr/bin/env python3
import sys


NONE = 0
LEFT = -1
RIGHT = 1



def makeWeighWithFalseLighter(leftScale, rightScale, falseCoinPos):
    if len(leftScale) > len(rightScale):
        return LEFT
    elif len(leftScale) < len(rightScale):
        return RIGHT
    else:
        if falseCoinPos in leftScale:
            return RIGHT
        elif falseCoinPos in rightScale:
            return LEFT
        else:
            return NONE


def makeWeighWithFalseHeavier(leftScale, rightScale, falseCoinPos):
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


def findMissing(a, b):
    notPresent = []
    s = dict()
    if type(b) == set:
        b = list(b)
    for i in range(len(b)):
        s[b[i]] = 1
    for i in range(len(a)):
        if a[i] not in s.keys():
            notPresent.append(a[i])
    return notPresent


def findThirdScale(leftScale, rightScale, coinsNum, trueCoins):
    thirdScale = []
    for i in range(1, coinsNum + 1):
        if i not in leftScale and i not in rightScale and i not in trueCoins:
            thirdScale.append(i)
    return thirdScale


def makeDynamicWeighWithFalseLighter(leftScale, rightScale, trueCoins, coinsNum):
    if len(leftScale) > len(rightScale):
        return LEFT, trueCoins
    elif len(leftScale) < len(rightScale):
        return RIGHT, trueCoins
    else:
        thirdScale = findThirdScale(leftScale, rightScale, coinsNum, trueCoins)
        leftFalse = findMissing(leftScale, trueCoins)
        rightFalse = findMissing(rightScale, trueCoins)
        if len(leftFalse) == 0 and len(rightFalse) == 0:
            trueCoins.update(leftFalse)
            trueCoins.update(rightFalse)
            return NONE, trueCoins
        elif len(leftFalse) == 0 and len(rightFalse) > 0 and len(thirdScale) == 0:
            trueCoins.update(leftFalse)
            trueCoins.update(thirdScale)
            return LEFT, trueCoins
        elif len(leftFalse) == 0 and len(rightFalse) > 0 and len(thirdScale) > 0:
            if len(rightFalse) >= len(thirdScale):
                trueCoins.update(leftFalse)
                trueCoins.update(thirdScale)
                return LEFT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(rightFalse)
                return NONE, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) == 0 and len(thirdScale) == 0:
            trueCoins.update(rightFalse)
            trueCoins.update(thirdScale)
            return RIGHT, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) == 0 and len(thirdScale) > 0:
            if len(leftFalse) >= len(thirdScale):
                trueCoins.update(rightFalse)
                trueCoins.update(thirdScale)
                return RIGHT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(rightFalse)
                return NONE, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) > 0 and len(thirdScale) == 0:
            if len(leftFalse) >= len(rightFalse):
                trueCoins.update(rightFalse)
                trueCoins.update(thirdScale)
                return RIGHT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(thirdScale)
                return LEFT, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) > 0 and len(thirdScale) > 0:
            if len(leftFalse) >= len(rightFalse):
                if len(leftFalse) >= len(thirdScale):
                    trueCoins.update(rightFalse)
                    trueCoins.update(thirdScale)
                    return RIGHT, trueCoins
                else:
                    trueCoins.update(leftFalse)
                    trueCoins.update(rightFalse)
                    return NONE, trueCoins    
            else:
                if len(rightFalse) >= len(thirdScale):
                    trueCoins.update(leftFalse)
                    trueCoins.update(thirdScale)
                    return LEFT, trueCoins
                else:
                    trueCoins.update(leftFalse)
                    trueCoins.update(rightFalse)
                    return NONE, trueCoins


def makeDynamicWeighWithFalseHeavier(leftScale, rightScale, trueCoins, coinsNum):
    if len(leftScale) > len(rightScale):
        return LEFT, trueCoins
    elif len(leftScale) < len(rightScale):
        return RIGHT, trueCoins
    else:
        thirdScale = findThirdScale(leftScale, rightScale, coinsNum, trueCoins)
        leftFalse = findMissing(leftScale, trueCoins)
        rightFalse = findMissing(rightScale, trueCoins)
        if len(leftFalse) == 0 and len(rightFalse) == 0:
            trueCoins.update(leftFalse)
            trueCoins.update(rightFalse)
            return NONE, trueCoins
        elif len(leftFalse) == 0 and len(rightFalse) > 0 and len(thirdScale) == 0:
            trueCoins.update(leftFalse)
            trueCoins.update(thirdScale)
            return RIGHT, trueCoins
        elif len(leftFalse) == 0 and len(rightFalse) > 0 and len(thirdScale) > 0:
            if len(rightFalse) >= len(thirdScale):
                trueCoins.update(leftFalse)
                trueCoins.update(thirdScale)
                return RIGHT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(rightFalse)
                return NONE, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) == 0 and len(thirdScale) == 0:
            trueCoins.update(rightFalse)
            trueCoins.update(thirdScale)
            return LEFT, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) == 0 and len(thirdScale) > 0:
            if len(leftFalse) >= len(thirdScale):
                trueCoins.update(rightFalse)
                trueCoins.update(thirdScale)
                return LEFT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(rightFalse)
                return NONE, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) > 0 and len(thirdScale) == 0:
            if len(leftFalse) >= len(rightFalse):
                trueCoins.update(rightFalse)
                trueCoins.update(thirdScale)
                return LEFT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(thirdScale)
                return RIGHT, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) > 0 and len(thirdScale) > 0:
            if len(leftFalse) >= len(rightFalse):
                if len(leftFalse) >= len(thirdScale):
                    trueCoins.update(rightFalse)
                    trueCoins.update(thirdScale)
                    return LEFT, trueCoins
                else:
                    trueCoins.update(leftFalse)
                    trueCoins.update(rightFalse)
                    return NONE, trueCoins    
            else:
                if len(rightFalse) >= len(thirdScale):
                    trueCoins.update(leftFalse)
                    trueCoins.update(thirdScale)
                    return RIGHT, trueCoins
                else:
                    trueCoins.update(leftFalse)
                    trueCoins.update(rightFalse)
                    return NONE, trueCoins


def makeDynamicWeigh(leftScale, rightScale, trueCoins, coinsNum):
    if len(leftScale) > len(rightScale):
        return LEFT, trueCoins
    elif len(leftScale) < len(rightScale):
        return RIGHT, trueCoins
    else:
        thirdScale = findThirdScale(leftScale, rightScale, coinsNum, trueCoins)
        leftFalse = findMissing(leftScale, trueCoins)
        rightFalse = findMissing(rightScale, trueCoins)
        if len(leftFalse) == 0 and len(rightFalse) == 0:
            trueCoins.update(leftFalse)
            trueCoins.update(rightFalse)
            return NONE, trueCoins
        elif len(leftFalse) == 0 and len(rightFalse) > 0 and len(thirdScale) == 0:
            trueCoins.update(leftFalse)
            trueCoins.update(thirdScale)
            return RIGHT, trueCoins
        elif len(leftFalse) == 0 and len(rightFalse) > 0 and len(thirdScale) > 0:
            if len(rightFalse) >= len(thirdScale):
                trueCoins.update(thirdScale)
                return RIGHT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(rightFalse)
                return NONE, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) == 0 and len(thirdScale) == 0:
            trueCoins.update(rightFalse)
            trueCoins.update(thirdScale)
            return LEFT, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) == 0 and len(thirdScale) > 0:
            if len(leftFalse) >= len(thirdScale):
                trueCoins.update(thirdScale)
                return LEFT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(rightFalse)
                return NONE, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) > 0 and len(thirdScale) == 0:
            if len(leftFalse) >= len(rightFalse):
                trueCoins.update(rightFalse)
                trueCoins.update(thirdScale)
                return LEFT, trueCoins
            else:
                trueCoins.update(leftFalse)
                trueCoins.update(thirdScale)
                return RIGHT, trueCoins
        elif len(leftFalse) > 0 and len(rightFalse) > 0 and len(thirdScale) > 0:
            if len(leftFalse) >= len(rightFalse):
                if len(leftFalse) >= len(thirdScale):
                    trueCoins.update(thirdScale)
                    return LEFT, trueCoins
                else:
                    trueCoins.update(leftFalse)
                    trueCoins.update(rightFalse)
                    return NONE, trueCoins    
            else:
                if len(rightFalse) >= len(thirdScale):
                    trueCoins.update(thirdScale)
                    return RIGHT, trueCoins
                else:
                    trueCoins.update(leftFalse)
                    trueCoins.update(rightFalse)
                    return NONE, trueCoins