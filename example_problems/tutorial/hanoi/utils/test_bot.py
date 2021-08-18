#!/usr/bin/env python3
import sys, os
sys.setrecursionlimit(1000000)
from time import monotonic

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../services")))
from hanoi_lib import HanoiTowerProblem





if len(sys.argv) == 3:
    v = sys.argv[1]
    be_efficient = (sys.argv[2] == 'yes')
    h = HanoiTowerProblem(v)

    while True:
        start = input()
        if start[0] == '#':
            continue
        if start == 'Finish Tests':
            break
        final = input()
        t_start = monotonic()
        res = h.getMinMoves(start, final, be_efficient)
        t_end = monotonic()
        time = t_end - t_start # seconds in float

        print(res)
        # print(f'T:{time}')
