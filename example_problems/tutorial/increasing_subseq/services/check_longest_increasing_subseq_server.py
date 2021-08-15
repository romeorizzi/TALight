#!/usr/bin/env python3
from sys import stderr, exit
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="check_longest_increasing_subseq"
args_list = [
    ('T',str),
    ('max_len_min_k',str),
    ('feas_subseq',str),
    ('feedback_level',str),
    ('coloring',str),
    ('more_or_less_hint_if_wrong_max_len_min_k',bool),
    ('silent',bool),
    ('lang',str),
    ('seed', str)
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
seed = ENV['seed']
print(seed, type(seed))
string_T = ""
string_s = ""

feedback = ENV['feedback_level']

T_length  = 100

n_seed = None
if re.match(r"^[0-9]{2,}$", seed):
    n_seed = int(seed)

print(feedback)

if ENV['T'] == 'lazy_input' and n_seed != None:

    T = generate_random_seq(T_length, 100, seed) 
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

TAc.print("\nInsert s:", "green")
string_s = input()
ok = bool(re.match(r"^((([1-9][0-9]{0,9} *)*))$", string_s))
if ok:
    s = parse_input(string_s)
else:
    TAc.print("\n\nWRONG INPUT FORMAT: this is not a sequence of numbers (example: 12 34 56 ...).\n", "red")
    exit(0)

ret = LS(T, "increasing")
longest = find_ls(ret)

if s in longest:
    TAc.print("\n\nYES, s is a maximum length increasing subsequence of T.\n", "red")
else:
    TAc.print("\n\nNO, s isn't a maximum length increasing subsequence of T.\n", "red")
    if feedback == 'complete_subseq':
        print("The longest increasing subsequence is... ")
        ret = is_subseq_with_position(longest[0],T)
        print(remove_duplicate_spaces(list_to_string(T)))
        print(get_yes_certificate(T, ret[1]))

    elif feedback == 'subseq_prefix':
        print("The longest increasing subsequence start with...")
        pref = get_prefix(longest[0])
        ret = is_subseq_with_position(pref, T)
        print(remove_duplicate_spaces(list_to_string(T)))
        print(get_yes_certificate(T, ret[1]))

        



