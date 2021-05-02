#!/usr/bin/python
from sys import stderr, exit, argv

usage=f"""I am an efficient (linear time) bot that always answers yes (y) to every instance (in an infinite loop)."""

if len(argv) != 1:
    print(f"ERROR from bot {argv[0]}:\n\n   called with the wrong number of parameters.\n")
    print(usage)
    exit(1)

while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    # T = spoon.split()
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    # S = spoon.split()
    print('y')
exit(0)
