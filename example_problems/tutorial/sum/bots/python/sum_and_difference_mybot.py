#!/usr/bin/env python3
import math
from signal import SIGINT, SIGKILL, SIGTERM, signal, SIGPIPE, SIG_DFL
from sys import stderr, exit, argv

while True:
    print(f"BOT: waiting for input", file=stderr)
    spoon = input()
    print(f"BOT: spoon={spoon}", file=stderr)
    if not('WE HAVE FINISHED' in spoon) and not('Correct answers:' in spoon) and not('[Press ENTER to exit]' in spoon):
        if spoon[0] != '#':
            s,d = map(int, spoon.split() )
            x1 = (s + d) // 2
            x2 = (s - d) // 2
            print(f"{x1} {x2}")
            print(f"BOT: {x1} {x2}", file=stderr)
    else:
        signal(SIGPIPE,SIG_DFL)
        signal(SIGINT,SIG_DFL) 
        exit(0)
