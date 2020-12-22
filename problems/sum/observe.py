#!/usr/bin/env python3

from random import randrange

n = int(input())
if n == 0:
    print(0, 0)
else:
    a = randrange(n)
    b = n - a
    print(a, b)
