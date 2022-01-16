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
        s,d = map(int, line.split() )
        x1 = (s + d) // 2
        x2 = (s - d) // 2
        print(f"{x1} {x2}")
