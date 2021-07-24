#!/usr/bin/env python3
import random


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
