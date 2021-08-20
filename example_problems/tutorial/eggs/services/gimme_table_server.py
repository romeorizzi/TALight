#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="eggs"
service="gimme_table"
args_list = [
    ('n_eggs',int),
    ('n_floors',int),
    ('eggs_from_zero',bool),
    ('floors_from_zero',bool),
    ('lang',str),
]

from sys import stderr, exit
from random import randrange
from math import inf as IMPOSSIBLE

from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:


# INITIALIZATON: allocation, base cases, sentinels
table = [ [0] + [IMPOSSIBLE] * ENV['n_floors'] ]
for u in range(ENV['n_eggs']):
    table.append([0] + [None] * ENV['n_floors'])

# INDUCTTVE STEP: the min-max recursion with nature playing against
for u in range(1,1+ENV['n_eggs']):
    for f in range(1,1+ENV['n_floors']):
        table[u][f] = IMPOSSIBLE
        for first_launch_floor in range(1,1+f):
            table[u][f] = min(table[u][f],1+max(table[u][f-first_launch_floor],table[u-1][first_launch_floor-1]))

# PRINTING OUT THE TABLE:
width=max(4,1+len(str(table[1][-1]))) if ENV['eggs_from_zero'] else 1+len(str(table[0][-1]))
fmt = f"%{width}d"
if ENV['eggs_from_zero']:
    print(fmt % 0, end=" "*(width-3)) if ENV['floors_from_zero'] else print("", end=(" "*(width-3)))
    for _ in range(1,len(table[0])): print("inf", end=(" "*(width-3)))
    print()
for row in table[1:]:
    for ele in row if ENV['floors_from_zero'] else row[1:]:
        print(fmt % ele, end="")
    print()    
exit(0)
