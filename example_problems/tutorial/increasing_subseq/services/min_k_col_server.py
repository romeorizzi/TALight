#!/usr/bin/env python3
from sys import stderr, exit
import re
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="min_k_col"
args_list = [
    ('coloring', str),
    ('lang', str),
    ('seed', str),
    ('goal', str),
    ('input_type', str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

seed = ENV['seed']
input_type = ENV['input_type']
n_seed = None
if re.match(r"^[1-9]|[0-9]{2,5}$", seed):
    n_seed = int(seed)

'''
#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")
TAc.print("\nYou will be given a sequence of numbers, and you have to enter a minimum coloring, where all elements of the same color represent a non-increasing sequence.", "green")
T = generate_random_seq(10,100)
string_T = list_to_string(T)
TAc.print("T: "+string_T+"\n\n","green")


mdc = min_decreasing_col(T)

n_col = n_coloring(mdc)


TAc.print("Insert your coloring (example: 1 3 1 ... where 1 = color_1):\n","green")
k = input()
ok = bool(re.match(r"^((([1-9][0-9]{0,9} *){9}[1-9][0-9]{0,9}))$", k))
if ok:
    color = parse_input(k)
else:
    TAc.print("\n\nWRONG INPUT FORMAT: this is not a sequence of color (example: 1 3 1 ... where 1 = color_1).\n", "red")
    exit(0)


n_col_user = n_coloring(color)

if n_col == n_col_user:
    TAc.print("\n\nYES, it's the minimum coloring of T\n", "red")
else:
    TAc.print("\n\nNO, it isn't the minimum coloring of T\n", "red")
'''

growth = []
n_instances = 10
T_length = 10
timing = 0
previous = 0
correct = True
seed, seeds = list_of_seed(n_seed, n_instances)
for i in range(0, n_instances ):
    if not correct:
        break
    T = generate_random_seq(T_length, 100, seeds[i + 1])
    print("\n#Sequence:")
    print(list_to_string(T[0]))
    T_length *= 2
    mdc = min_decreasing_col(T[0])
    n_col = n_coloring(mdc)

    res = input()
    if input_type == 'sequence':
        if not is_subseq_with_position(parse_input(res), T[0])[0]:
            TAc.print("\n#NO, it isn't the maximum increasing subsequence of T\n", "red")
            print("#Seed of this test: " + str(seed))
            break
        else:
            res = len(parse_input(res))

    if n_col == int(res):
        TAc.print("\n#YES, it's the length of the maximum increasing subsequence of T\n", "red")
    else:
        TAc.print("\n#NO, it isn't the  maximum increasing subsequence of T\n", "red")
        print("#Seed of this test: " + str(seed))
        correct = False

    
    if i != 0 and ENV['goal'] == 'efficient':        
        growth.append(get_growth_rate(previous,timing))


if ENV['goal'] == 'efficient' and correct:
    linear = True
    for i in growth:
        if i > 2:
            linear = False
    
    if linear == True:
        print("Linear")
    else:
        print("Not linear")


    