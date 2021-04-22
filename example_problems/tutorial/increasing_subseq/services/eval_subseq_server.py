#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="eval_subseq_server"
args_list = [
    ('seed',str),
    ('goal',str),
    ('code_lang',str),
    ('cert', bool),
    ('lang',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")

string_T = ""
string_s = ""
length = int(ENV["times"])
TAc.print("\nIn this problem you are given a sequence of numbers T. You are asked to evaluate whether a sub-sequence s is part of T "+str(length)+" times. \nAnswer \"y\" if you think s is a subsequence of T, \"n\" otherwise.", "green")
string_T = generate_random_seq(10, 100)
TAc.print(list_to_string(string_T), "green")
cert = ENV['cert']

seed = ENV['seed']
n_seed = None

if re.match(r"^[1-9]|[0-9]{2,5}$", seed):
    n_seed = int(seed)

for i in range(0, length):
    x = random.randint(1,10)
    if i == 0 or x % 2 == 0:
        string_s = get_rand_subseq(string_T, n_seed)
    else:
        string_s = get_not_subseq(string_T, 100)
    TAc.print(list_to_string(string_s),"green")
    res = input()

    if res == "y" or res == "Y": 
        res = True
    elif res =="n" or res == "N":
        res = False
    else: 
        TAc.print("WRONG INPUT FORMAT: only \"y\" or \"n\" are allowed as answer.","red")
        exit(0)
    ret = is_subseq_with_position(string_s,string_T)
    if ret[0] == res:
        TAc.print("OK, your answer is correct!\n","green")
    else:
        TAc.print("NO, your answer isn't correct.\n","red")
        
        if cert:
            if ret[0]:
                print(remove_duplicate_spaces(list_to_string(string_T)))
                print(get_yes_certificate(string_T, ret[1]))
            else:
                if not ret[1]:
                    print("T doesn't contains s")
                else:
                    print("T contains only these elements of s")
                    print(remove_duplicate_spaces(list_to_string(string_T)))
                    print(get_yes_certificate(string_T, ret[1]))
        print("\n")           
                    




