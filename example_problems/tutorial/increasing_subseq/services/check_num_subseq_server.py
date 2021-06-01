#!/usr/bin/env python3
from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="check_num_occurrences_of_s_in_T"
args_list = [
    ('T',str),
    ('s',str),
    ('lang',str),
    ('seed', str)
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
seed = ENV['seed']

string_T = ""
string_s = ""

feedback = ENV['feedback_level']

T_length  = 10

n_seed = None
if re.match(r"^[0-9]{2,}$", seed):
    n_seed = int(seed)

seeds = list_of_seed(n_seed, 2)

if ENV['T'] == 'lazy_input' and n_seed != None:
    T = generate_random_seq(T_length, 100, seeds[1][0]) 
    T = T[0]
    print(list_to_string(T))
elif ENV['T'] == 'lazy_input':
    TAc.print("\nIn this problem you are asked to enter a increasing senquence of numbers T with a blank space between each number (example: 12 34 56 ...). Then you have to find the longest sub-sequence s of numbers. You will be told if s is the longest sub-sequence of T.", "green")
    TAc.print("\nInsert T:", "green")
    string_T = input()
    ok = bool(re.match(r"^((([1-9][0-9]{0,9} *)*))$", string_T))
    if ok:
        T = parse_input(string_T)
    else:
        TAc.print("\n\nWRONG INPUT FORMAT: this is not a sequence of numbers (example: 12 34 56 ...).\n", "red")
        exit(0)
else:
    string_T = ENV['T']
    T = parse_input(string_T)

if ENV['s'] == 'lazy_input' and n_seed != None:
    s = get_random_subseq(T, seeds[1][1], math.log(len(T))) 
    s = s[0]
    print(list_to_string(s))

elif ENV['T'] == 'lazy_input':
    TAc.print("\nInsert s:", "green")
    string_s = input()
    ok = bool(re.match(r"^((([1-9][0-9]{0,9} *)*))$", string_s))
    if ok:
        s = parse_input(string_s)
    else:
        TAc.print("\n\nWRONG INPUT FORMAT: this is not a sequence of numbers (example: 12 34 56 ...).\n", "red")
        exit(0)
else:
    string_s = ENV['s']
    s = parse_input(string_s)

all_subseq_with_pos = sub_lists_with_pos(T)
position = get_position_from_subseq(s, all_subseq_with_pos)

for i in position:
    print(list_to_string(T))
    print(get_yes_certificate(T,i))

