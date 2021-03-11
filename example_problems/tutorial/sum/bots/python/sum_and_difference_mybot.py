#!/usr/bin/env python3
import math

while True:
    spoon = input().strip()
    while spoon[0] != '?':
        spoon = input().strip()
    s,d = map(int, spoon[1:].split() )
    x1 = (s + d) // 2
    x2 = (s - d) // 2
    print(f"{x1} {x2}")
