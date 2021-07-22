#!/usr/bin/env python3
import random


def generateRandomPegsList(len: int, diffPegsNum: int):
    pegsList = random.sample(range(1, diffPegsNum), len)
    return pegsList

def blackScore(secret_code: list, guessed_code: list):
    assert len(secret_code) == len(guessed_code)
    risp = 0
    for i in range(len(secret_code)):
        if guessed_code[i] == secret_code[i]:
            risp += 1
    return risp

def whiteScore(secret_code: list, guessed_code: list):
    assert len(secret_code) == len(guessed_code)
    risp = 0
    secret_code_occur = {}
    for col in secret_code:
        if col in secret_code_occur.keys():
            secret_code_occur[col] += 1
        else:
            secret_code_occur[col] = 1
    for col in guessed_code:
        if col in secret_code_occur.keys() and secret_code_occur[col] > 0:
            secret_code_occur[col] -= 1
            risp += 1
    return risp - blackScore(secret_code, guessed_code)

def checkAttempt(secret_code: list, guessed_code: list):
    numB = 0
    numW = 0
    
    rightColor = len(secret_code) - len(list(set(secret_code) - set(guessed_code)))
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
