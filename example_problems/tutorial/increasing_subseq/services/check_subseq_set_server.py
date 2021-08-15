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
    ('feedback',str),
    ('lang',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
level = ENV['feedback']
TAc.print("\nYou will be given a sequence of numbers, and you have to enter all the different subsequences", "green")
T = generate_random_seq(5,100)
string_T = list_to_string(T)
TAc.print("T: "+string_T+"\n\n","green")


TAc.print("Insert your subsequence (example: 1 3 1 ... ):\n","green")
k = input()
ok = bool(re.match(r"^((([1-9][0-9]{0,9} *){0,9}[1-9][0-9]{0,9}))$", k))
if ok:
    sub = parse_input(k)
else:
    TAc.print("\n\nWRONG INPUT FORMAT\n", "red")
    exit(0)

subseq = ordered_sub_sequences(T)
sub = [ int(x) for x in sub ]

if level == 'yes_no':
    if sub in subseq:
        TAc.print("\n\nYES, it's the minimum coloring of T\n", "red")
    else:
        TAc.print("\n\nNO, it isn't the minimum coloring of T\n", "red")
elif level == 'give_one_missing':
    if sub in subseq:
        TAc.print("\n\nYES, it's the minimum coloring of T\n", "red")
    else:
        TAc.print("\n\nNO, it isn't the minimum coloring of T\n", "red")
        missing = get_missing_subsequences(subseq, sub)
        print(list_to_string(random.choice(missing)))
else:
    if sub in subseq:
        TAc.print("\n\nYES, it's the minimum coloring of T\n", "red")
    else:
        TAc.print("\n\nNO, it isn't the minimum coloring of T\n", "red")
        missing = get_missing_subsequences(subseq, sub)
        print(list_to_string(get_prefix(random.choice(missing))))


    



