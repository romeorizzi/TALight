#!/usr/bin/env python3
import math
from sys import stderr, argv

while True:
    line = input()
    #print(f"# BOT: line={line}", file = stderr)
    if line[0] == '#':   # this is a commented line (sent by the service server)
        if '# WE HAVE FINISHED' == line:
            exit(0)   # exit upon termination of the service server
    else:
        s,p = map(int, line.split() )
        Δ = int(math.sqrt(s*s-4*p))
        x1 = (s - Δ)//2
        x2 = s - x1
        print(f"{x1} {x2}")
