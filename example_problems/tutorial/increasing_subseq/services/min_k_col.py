#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import parse_input, lis, get_min_coloring, n_coloring, is_subseq_with_position, get_yes_certificate, remove_duplicate_spaces, generate_random_seq, list_to_string

# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="is_subseq_server"
args_list = [
    ('coloring',str),
    ('lang',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")
TAc.print("\nIn this problem you are asked to enter a sequence T of numbers with a blank space between each number (example: 12 34 56 ...) and a sequence s. You will be told if s is a sub-sequence of T.", "green")
T = generate_random_seq(10,100)
string_T = list_to_string(T)
TAc.print("T: "+string_T+"\n\n","green")

inc_seq = lis(T)
print(inc_seq)
coloring = get_min_coloring(inc_seq)

print(coloring)
n_col = n_coloring(coloring)

TAc.print("Insert your coloring:\n","green")
k = input()
ok = bool(re.match(r"^((([1-9][0-9]{0,9} *){9}[1-9][0-9]{0,9}))$", k))
if ok:
    color = parse_input(k)
else:
    TAc.print("\n\nWRONG INPUT FORMAT: this is not a sequence of numbers (example: 12 34 56 ...).\n", "red")
    exit(0)


n_col_user = n_coloring(color)

if n_col == n_col_user:
    TAc.print("\n\nYES, it's the minimum coloring of T\n", "red")
else:
    TAc.print("\n\nNO, it isn't the minimum coloring of T\n", "red")



