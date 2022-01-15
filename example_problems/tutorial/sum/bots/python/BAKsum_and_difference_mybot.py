#!/usr/bin/env python3
import math
from sys import stderr, exit, argv

while True:
    print(f"BOT: waiting for input", file=stderr)
    spoon = input()
    print(f"BOT: spoon={spoon}", file=stderr)
    if spoon[0] == '#':
        if '#    Correct answers:' == spoon[:len('#    Correct answers:')]:
            exit(0)
    else:
        s,d = map(int, spoon.split() )
        x1 = (s + d) // 2
        x2 = (s - d) // 2
        print(f"{x1} {x2}")
        print(f"BOT: {x1} {x2}", file=stderr)
