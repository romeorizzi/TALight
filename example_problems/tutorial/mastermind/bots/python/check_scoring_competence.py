#!/usr/bin/env python3


def calculateScore(secretCode: list, guessedCode: list):
    assert len(secretCode) == len(guessedCode)
    rightPositonAndColor = 0
    for i in range(len(secretCode)):
        if guessedCode[i] == secretCode[i]:
            rightPositonAndColor += 1
    rightColor = 0
    for col in guessedCode:
        if col in secretCode:
            rightColor += 1
    rightColor -= rightPositonAndColor
    return rightColor, rightPositonAndColor


def startAlgo(spoon):
    while spoon[:len("secret code:")] != "secret code:":
        spoon = input().strip()
    secretCode = [int(s) for s in (spoon.split(':')[1]).split()]
    while spoon[:len("guessed code:")] != "guessed code:":
        spoon = input().strip()
    guessedCode = [int(s) for s in (spoon.split(':')[1]).split()]
    spoon = input().strip()
    while spoon[:len("# ")] == "# ":
        spoon = input().strip()
    rightColor, rightPositonAndColor = calculateScore(secretCode, guessedCode)
    result = []
    for i in range(0, rightPositonAndColor):
        result.append('b')
    for i in range(0, rightColor):
        result.append('w')
    print(*result)
    spoon = input().strip()


def main():
    spoon = input().strip()
    while spoon[:len("# ")] == "# ":
        spoon = input().strip()
    startAlgo(spoon)


if __name__ == "__main__":
    main()