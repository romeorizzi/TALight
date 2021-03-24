#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import parse_input, strictly_increasing, strictly_decreasing, non_increasing, non_decreasing, generate_random_inc_seq, generate_random_dec_seq, list_to_string, generate_random_seq, is_subseq_with_position, get_yes_certificate, remove_duplicate_spaces

# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="is_subseq_server"
args_list = [
    ('times',int),
    ('lang',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")

string_T = ""
type_seq = [1,2,3,4]

length = (ENV["times"])
TAc.print("\nIn this problem you are given a sequence of numbers T. You are asked to evaluate whether T is a strictly increasing/decreasing or non increasing/decreasing sequence "+str(length)+" times. \nAnswer \"y\" if you think the answer is correct, \"n\" otherwise.\n", "green")


for i in range(0, length):
    x = random.randint(1,10)
    if x % 2 == 0:
        string_T = generate_random_inc_seq(10, 100)
    else: 
        string_T = generate_random_dec_seq(10, 100)
    TAc.print(list_to_string(string_T), "green")
    res = random.choice(type_seq)
    if res == 1: 
        TAc.print("The sequence is strictly increasing.\n","green")
        r = strictly_increasing(string_T)
    elif res == 2: 
        TAc.print("The sequence is strictly decreasing.\n","green")
        r = strictly_decreasing(string_T)
    elif res == 3:
        TAc.print("The sequence is non-increasing.\n","green")
        r = non_increasing(string_T)
    else: 
        TAc.print("The sequence is non-decreasing.\n","green")
        r = non_decreasing(string_T)

    res = input()

    if res == "y" or res == "Y": 
        res = True
    elif res =="n" or res == "N":
        res = False
    else: 
        TAc.print("WRONG INPUT FORMAT: only \"y\" or \"n\" are allowed as answer.","red")
        exit(0)
    if r == res:
        TAc.print("OK, your answer is correct!\n\n","green")
    else:
        TAc.print("NO, your answer isn't correct.\n\n","red")
