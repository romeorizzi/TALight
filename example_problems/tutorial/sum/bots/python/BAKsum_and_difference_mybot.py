#!/usr/bin/env python3
import math
from sys import stderr, exit, argv

while True:
    spoon = input()
    if spoon[0] == '#':
        if 'WE HAVE FINISHED' in spoon:
            exit(0)
    else:
        s,d = map(int, spoon.split() )
        x1 = (s + d) // 2
        x2 = (s - d) // 2
        print(f"{x1} {x2}")
