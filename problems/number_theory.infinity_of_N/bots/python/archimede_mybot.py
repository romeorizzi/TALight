#!/usr/bin/env python3

while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    if spoon[0] == '!':
        exit(0)
    if len(spoon.split(".")) == 1:
        n = int(spoon)
        assert n > 0 # perchè si assume che il numero reale fornito sia > 0
    else:
        assert len(spoon.split(".")) == 2
        n_str , r_str = spoon.split(".")
        n = int(n_str)
    if n >= 1:
        print(42)
    else:
        assert n==0
        print(10**(1+len(r_str)))
exit(0)
