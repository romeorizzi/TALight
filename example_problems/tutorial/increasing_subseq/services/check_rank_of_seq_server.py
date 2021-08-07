#!/usr/bin/env python3
from sys import stderr, exit
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="is_subseq_server"
args_list = [
    ('T',str),
    ('sorting_criterion',str),
    ('lang',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")

string_T = ""

if (ENV['T'] == 'lazy_input'):
    TAc.print("\nIn this problem you are asked to enter a sequence T of numbers with a blank space between each number (example: 12 34 56 ...). You are also asked to tell if T is a strictly increasing/decreasing or non increasing/decreasing sequence.\n", "green")
    TAc.print("\nInsert T:", "green")
    string_T = input()
    ok = bool(re.match(r"^((([1-9][0-9]{0,9} *)*[1-9][0-9]{0,9}))$", string_T))
    if ok:
        T = parse_input(string_T)
    else:
        TAc.print("\n\nWRONG INPUT FORMAT: this is not a sequence of numbers (example: 12 34 56 ...).\n", "red")
        exit(0)
else:
    string_T = ENV['T']
    T = parse_input(string_T)

if ENV["sorting_criterion"] == "lazy_input":
    TAc.print("\nEnter a digit from 1 to 4, where: \n(1) - Strictly increasing\n(2) - Stricly decreasing\n(3) - Non-increasing\n(4) - Non-decreasing\nYour answer:\n", "green")
    order_s = input()
    if order_s == "1":
        if strictly_increasing(T):
            TAc.print("\n\nYES, T is a strictly increasing sequence!\n", "red")
        else:
            TAc.print("\n\nNO, T isn't a strictly increasing sequence.\n", "red")
    elif order_s == "2":
        if strictly_decreasing(T):
            TAc.print("\n\nYES, T is a strictly decreasing sequence!\n", "red")
        else:
            TAc.print("\n\nNO, T isn't a strictly decreasing sequence.\n", "red")
    elif order_s == "3":
        if non_increasing(T):
            TAc.print("\n\nYES, T is a non-increasing sequence!\n", "red")
        else:
            TAc.print("\n\nNO, T isn't a non-increasing sequence.\n", "red")
    elif order_s == "4":
        if non_decreasing(T):
            TAc.print("\n\nYES, T is a non-decreasing sequence!\n", "red")
        else:
            TAc.print("\n\nNO, T isn't a non-decreasing sequence.\n", "red")
    else: 
        TAc.print("\n\nWRONG INPUT FORMAT: only \"1\", \"2\", \"3\" or \"4\" are allowed as answer.\n", "red")