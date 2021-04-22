#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="is_subseq_server"
args_list = [
    ('goal',str),
    ('code_lang',str),
    ('NO_cert',bool),
    ('lang',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
inst_correct = [(5,2), ]
inst_efficint = []


times = 20
#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")

string_T = ""
type_seq = [1,2,3,4]

TAc.print("\nIn this problem you are given a sequence of numbers T. You are asked to evaluate whether T is a strictly increasing/decreasing or non increasing/decreasing sequence "+str(times)+" times. \nAnswer \"y\" if you think the answer is correct, \"n\" otherwise.\n", "green")


for i in range(0, times):
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
        ordering = "increasing"
    elif res == 2: 
        TAc.print("The sequence is strictly decreasing.\n","green")
        r = strictly_decreasing(string_T)
        ordering = "decreasing"
    elif res == 3:
        TAc.print("The sequence is non-increasing.\n","green")
        r = non_increasing(string_T)
        ordering = "not_increasing"
    else: 
        TAc.print("The sequence is non-decreasing.\n","green")
        r = non_decreasing(string_T)
        ordering = "not_decreasing"

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
        if ENV['NO_cert'] == True: 
            TAc.print("Now insert your NO certificate: digit two indexes in the range (1, 10) of the sequence that breaks the statement given (example: \"1 2\").\nInsert: \n\n", "green")
            cert = input()
            ok = bool(re.match(r"^((([1-9][0-9]{0,9} *)[1-9][0-9]{0,9}))$", cert))
            if ok:
                cert = parse_input(cert)
            else: 
                TAc.print("WRONG INPUT FORMAT: only a pair of number in the senquence times is allowed as answer.\n","red")
                exit(0)
            ok = check_no_ordered_list_cert(string_T, int(cert[0])-1, int(cert[1])-1, ordering)

            if ok:
                TAc.print("Valid certificate!\n\n","green")
            else:
                TAc.print("Wrong certificate.\n\n","red")
    else:
        TAc.print("NO, your answer isn't correct.\n\n","red")
