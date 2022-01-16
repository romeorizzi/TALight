#!/usr/bin/env python3
import math
from sys import stderr, exit, argv

while True:
    spoon = input()
    #print(f"# BOT: spoon={spoon}")
    if spoon[0] == '#':   # spoon contains a commented line from the service server
        if '# WE HAVE FINISHED' == spoon:
            exit(0)   # exit upon termination of the service server
    else:
        s,p = map(int, spoon.split() )
        Δ = int(math.sqrt(s*s-4*p))
        x1 = (s - Δ)//2
        x2 = s - x1
        print(f"{x1} {x2}")
