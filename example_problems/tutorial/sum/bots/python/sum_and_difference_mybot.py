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
        s,d = map(int, spoon.split() )
        x1 = (s + d) // 2
        x2 = (s - d) // 2
        print(f"{x1} {x2}")
