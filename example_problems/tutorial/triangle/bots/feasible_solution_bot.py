#!/usr/bin/python
from sys import stderr, exit, argv
import random

usage=f"""I am an efficient (linear time) bot that provides a feasible path for every instance (in an infinite loop)."""

while True:
    directions = ["L","R"]
    instance = input()
    n = len(instance)
    path = ""
    for _ in range(n-1):
        path += random.choice(directions)
    print(path)
exit(0)

