#!/usr/bin/env python3
import random
import itertools


def generateRandomPegsList(len: int, diffPegsNum: int, seed: int):
    random.seed(seed)
    pegsList = random.choices(range(1, diffPegsNum+1), k=len)
    return pegsList


def calculateScore(secretCode: list, guessedCode: list):
    assert len(secretCode) == len(guessedCode)
    rightPositonAndColor = 0
    for i in range(len(secretCode)):
        if guessedCode[i] == secretCode[i]:
            rightPositonAndColor += 1
    rightColor = 0
    secretCode_occur = {}
    for col in secretCode:
        if col in secretCode_occur.keys():
            secretCode_occur[col] += 1
        else:
            secretCode_occur[col] = 1
    for col in guessedCode:
        if col in secretCode_occur.keys() and secretCode_occur[col] > 0:
            secretCode_occur[col] -= 1
            rightColor += 1
    rightColor -= rightPositonAndColor
    return rightColor, rightPositonAndColor


def getStringOfResult(rightColor, rightPositonAndColor):
    result = "b " * rightPositonAndColor
    result += "w " * rightColor
    result = result.rstrip()
    if result == "":
        result = "-"
    return result

def getHardSecretCode(guessedCode, numPegs, numColors, secretCodeAlive = None):
    if secretCodeAlive == None:
        secretCodeAlive = []
        colors = list(range(1, numColors + 1))
        comb = itertools.product(colors, repeat=numPegs)
        for i in comb:
            secretCodeAlive.append(list(i))
    possibilty = {
        (0, 0): [],
        (1, 0): [],
        (2, 0): [],
        (3, 0): [],
        (4, 0): [],
        (0, 1): [],
        (1, 1): [],
        (2, 1): [],
        (3, 1): [],
        (0, 2): [],
        (1, 2): [],
        (2, 2): [],
        (0, 3): [],
        (0, 4): [],
    }
    for secretCode in secretCodeAlive:
        rightColor, rightPositonAndColor = calculateScore(secretCode, guessedCode)
        possibilty[rightColor, rightPositonAndColor].append(secretCode)
    maxKey=max(possibilty, key=lambda k: len(possibilty[k]))
    return maxKey, possibilty[maxKey]