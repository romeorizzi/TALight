#!/usr/bin/env python3
import math
from sys import stderr, exit, argv

while True:
    spoon = input()
    if not 'WE HAVE FINISHED' in spoon:
        if spoon[0] != '#':
            s,d = map(int, spoon.split() )
            x1 = (s + d) // 2
            x2 = (s - d) // 2
            print(f"{x1} {x2}")
    else:
        exit(0)
