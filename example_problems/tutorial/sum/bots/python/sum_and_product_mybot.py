#!/usr/bin/env python3
import math

while True:
    spoon = input()
    if spoon[0] != '#':
        s,p = map(int, spoon.split() )
        Δ = int(math.sqrt(s*s-4*p))
        x1 = (s - Δ)//2
        x2 = s - x1
        print(f"{x1} {x2}")
