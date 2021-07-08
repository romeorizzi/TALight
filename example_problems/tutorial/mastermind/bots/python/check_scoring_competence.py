#!/usr/bin/env python3


def checkAttempt(key: list, attempt: list):
    rightColor = len(key) - len(list(set(key) - set(attempt)))
    rightPositonAndColor = 0
    for i in range(0, len(key)):
        if key[i] == attempt[i]:
            rightPositonAndColor += 1
            rightColor -= 1
    return rightColor, rightPositonAndColor


def startAlgo():
    spoon = input().strip()
    while spoon[:len("key: ")] != "key: ":
        spoon = input().strip()
    key = [int(s) for s in (spoon.split(':')[1]).split()]
    while spoon[:len("attempt: ")] != "attempt: ":
        spoon = input().strip()
    attempt = [int(s) for s in (spoon.split(':')[1]).split()]
    rightColor, rightPositonAndColor = checkAttempt(key, attempt)
    result = []
    for i in range(0, rightColor):
        result.append('w')
    for i in range(0, rightPositonAndColor):
        result.append('b')
    print(*result)


def main():
    spoon = input().strip()
    while spoon[:len("# After ")] != "# After ":
        spoon = input().strip()
        assert spoon[0] == "#"
    startAlgo()
    spoon = input().strip()


if __name__ == "__main__":
    main()