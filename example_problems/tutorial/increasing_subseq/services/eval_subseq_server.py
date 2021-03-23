#!/usr/bin/env python3
from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import parse_input, generate_random_seq, get_rand_subseq, get_not_subseq, is_subseq_with_position, remove_duplicate_spaces

# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="is_subseq_server"
args_list = [
    ('len',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")

string_T = ""
string_s = ""

TAc.print("\nIn this problem you are given a sequence of numbers T. You are asked to evaluate whether a sub-sequence s is part of T 10 times. \nAnswer \"y\" if you think s is a subsequence you T, \"n\" otherwise.", "green")
string_T = generate_random_seq(10, 100)
TAc.print(string_T)

length = int(ENV[len])

for i in range(0, length):
    if i < 8:
        string_s = get_rand_subseq(string_T)
    else:
        string_s = get_not_subseq(string_T, string_s, 100)
    TAc.print(string_s)
    res = input()

    if res == "y" or res == "Y": 
        res = true
    elif res =="n" or res == "N":
        res = false
    else: 
        TAc.print("WRONG INPUT FORMAT: only \"y\" or \"n\" are allowed as answer.")
        exit(0)
    ret = is_subseq_with_position(s,T)
    if ret[0] == res:
        TAc.print("OK\n")
    else:
        TAc.print("NO\n")

if ret[0]:
    TAc.print("\n\nYES, s is subsequence of T\n", "red")
else:
    TAc.print("\n\nNO, s isn't subsequence of T\n", "red")



