#!/usr/bin/env python3

while True:
    spoon = input().strip()
    while spoon[0] != '?':
        spoon = input().strip()
    n = int(spoon[1:])
    print(f"{n} 0")
