#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="eggs"
service="confirm_min_throws"
args_list = [
    ('min',int),
    ('n_eggs',int),
    ('n_floors',int),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
from random import randrange
from math import inf as IMPOSSIBLE

from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

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

if table[ENV['n_eggs']][ENV['n_floors']] < ENV['min']:
    print(f"No! When you are given {ENV['n_eggs']} eggs and the floors are {ENV['n_floors']} then there exists a policy that guarantees you to find out the truth in strictly less than {ENV['min']} launches, whatever will happen (worst case).")
    #English:  print("No! When you are given {ENV['n_eggs']} eggs and the floors are {ENV['n_floors']} then there exists a policy that guarantees you to find out the truth in strictly less than {ENV['min']} launches, whatever will happen (worst case).")
if table[ENV['n_eggs']][ENV['n_floors']] > ENV['min']:
    print(f"No! When you are given {ENV['n_eggs']} eggs and the floors are {ENV['n_floors']} then no policy guarantees you to find out the truth within {ENV['min']} launches in every possible scenario (aka, whathever the truth is).")
    #English: 
if table[ENV['n_eggs']][ENV['n_floors']] == ENV['min']:
    print(f"Yes! Indeed, {ENV['min']} is the smallest possible natural B such that, when you are given {ENV['n_eggs']} eggs and the floors are {ENV['n_floors']}, still there exists a policy that guarantees you to find out the truth within B launches in every possible scenario.")
    #English: 
exit(0)
