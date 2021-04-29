#!/usr/bin/env python3
from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="eval_num_occurrences_of_s_in_T"
args_list = [
    ('lang',str),
    ('seed', str)
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
cert = ENV['cert']
seed = ENV['seed']

n_seed = None
if re.match(r"^[1-9]|[0-9]{2,5}$", seed):
    n_seed = int(seed)
growth = []
n_instances = 10
T_length = 10
timing = 0
previous = 0
correct = True
seed, seeds = list_of_seed(n_seed, 2 * n_instances)
for i in range(0, n_instances * 2 ,2):
    if not correct:
        break
    T = generate_random_seq(T_length, 100, seeds[i])
    T = T[0]
    print(list_to_string(T))
    T_length *= 2
    s = get_rand_subseq(T, seeds[i + 1])
    s = s[0]
    print(list_to_string(s))
    if i != 0:
        previous = timing

    all_subseq_with_pos = sub_lists_with_pos(T)
    position = get_position_from_subseq(s, all_subseq_with_pos)
    
    risp = []
    start = time.time()
    limit = int(input())
    for c in range(limit):
        risp.append(list(parse_input(input())))
    end = time.time()
    timing = end - start
    print(position, risp)
    if position == risp:
        print("correct")


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