#!/usr/bin/env python3

while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    if spoon[0] == '!':
        exit(0)
    n = int(spoon)
    print(n+1)
exit(0)
