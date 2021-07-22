#!/usr/bin/env python3
import random


def generateRandomPegsList(len: int, diffPegsNum: int):
    pegsList = random.sample(range(1, diffPegsNum), len)
    return pegsList


def checkAttempt(key: list, attempt: list):
    rightColor = len(key) - len(list(set(key) - set(attempt)))
    rightPositonAndColor = 0
    for i in range(0, len(key)):
        if key[i] == attempt[i]:
            rightPositonAndColor += 1
            rightColor -= 1
    return rightColor, rightPositonAndColor

def getStringOfResult(rightColor, rightPositonAndColor):
    result = "b " * rightPositonAndColor
    result += "w " * rightColor
    result = result.rstrip()
    return result