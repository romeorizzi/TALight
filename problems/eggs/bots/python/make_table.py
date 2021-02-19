#!/usr/bin/env python3

from os import environ
from sys import argv, exit
from math import inf as IMPOSSIBLE

if len(argv) != 3:
    print(f"Usage: {argv[0]} num-eggs num-floors")
    exit(1)

n_eggs, n_floors = map(int, argv[1:])

# INITIALIZATON: allocation, base cases, sentinels
table = [ [0] + [IMPOSSIBLE] * n_floors ]
for u in range(n_eggs):
    table.append([0] + [None] * n_floors)

# INDUCTTVE STEP: the min-max recursion with nature playing against
for u in range(1,1+n_eggs):
    for f in range(1,1+n_floors):
        table[u][f] = IMPOSSIBLE
        for first_launch_floor in range(1,1+f):
            table[u][f] = min(table[u][f],1+max(table[u][f-first_launch_floor],table[u-1][first_launch_floor-1]))

# PRINTING OUT THE TABLE:
fmt = f"%{1+len(str(table[-1][-1]))}d"
for row in table[1:]:
    for ele in row[1:]:
        print(fmt % ele, end=" ")
    print()    
exit(0)


