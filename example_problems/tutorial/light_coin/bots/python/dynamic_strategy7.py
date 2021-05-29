#!/usr/bin/env python3

NONE = 0
LEFT = -1
RIGHT = 1

def doScale(left, right):
    print(*left, sep = " ", end=", ")
    print(*right, sep = " ")
    wait = True
    while True:
        spoon = input().strip()
        possibleResult = spoon.split(',')[0]
        if possibleResult == "NONE":
            return NONE
        if possibleResult == "LEFT":
            return LEFT
        if possibleResult == "RIGHT":
            return RIGHT

def findFalseCoin():
    print('#end')
    spoon = input().strip()

def chunkIt(seq, num):
    out = []
    tmp = []
    for item in seq:
        tmp.append(item)
        if len(tmp) == num:
            out.append(tmp)
            tmp = []
    if len(tmp) != 0:
        out.append(tmp)
    return out

def startAlgo():
    n = 7
    coinsToCheck = list(range(1, n + 1))
    while len(coinsToCheck) != 1:
        dim = len(coinsToCheck) // 3 + len(coinsToCheck) % 3
        chuncks = chunkIt(coinsToCheck, dim)
        left = chuncks[0]
        right = chuncks[1]
        result = doScale(left, right)
        if result == NONE:
            coinsToCheck = chuncks[2]
        elif result == LEFT:
            coinsToCheck = right
        elif result == RIGHT:
            coinsToCheck = left
    findFalseCoin()



spoon = input().strip()
while spoon[:len("#? waiting for ")] != "#? waiting for ":
    spoon = input().strip()
    assert spoon[0] == "#"
startAlgo()