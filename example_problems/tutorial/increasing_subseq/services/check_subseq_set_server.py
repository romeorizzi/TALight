#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import parse_input, ordered_sub_sequences ,min_decreasing_col, get_min_coloring, n_coloring, is_subseq_with_position, get_yes_certificate, remove_duplicate_spaces, generate_random_seq, list_to_string

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

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")
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
print(sub)
sub = [ int(x) for x in sub ]
print(subseq)

if sub in subseq:
    TAc.print("\n\nYES, it's the minimum coloring of T\n", "red")
else:
    TAc.print("\n\nNO, it isn't the minimum coloring of T\n", "red")



