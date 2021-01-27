#!/usr/bin/env python3
import math

while True:
    spoon = input().strip()
    while spoon[0] != '?':
        spoon = input().strip()
    s,p = map(int, spoon[1:].split() )
    x1 = int((s - math.sqrt(s*s-4*p))//2)
    x2 = s - x1
    print(f"{x1} {x2}")
