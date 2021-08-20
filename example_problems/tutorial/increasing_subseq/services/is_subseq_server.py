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
    ('S',str),
    ('lang',str),
    ('YES_cert',bool),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if ENV['T'] == 'lazy_input' or ENV['S'] == 'lazy_input':
    TAc.print("\n#Given two sequences S and T of positive integers, this service tells whether S is a subsquence of T.", "green")
if ENV['T'] == 'lazy_input':
    TAc.print("\n#Insert T (a sequence of positive integers separated by spaces. Example: 12 34 56):", "green")
    string_T = TALinput(str, regex="^[1-9][0-9]{0,9}$", regex_explained="a positive integer. Example: 31423.", TAc=TAc, LANG=LANG)
else:
    string_T = ENV['T']
    
if ENV['S'] == 'lazy_input':
    TAc.print("\n#Insert S (a sequence of positive integers separated by spaces. Example: 12 34 56):", "green")
    string_S = TALinput(str, regex="^[1-9][0-9]{0,9}$", regex_explained="a positive integer. Example: 31423.", TAc=TAc, LANG=LANG)
else:
    string_S = ENV['S']

S = list(map(int,string_S))
T = list(map(int,string_T))

ret = is_subseq_with_position(S,T)

if ret[0]:
    TAc.print("\n\n#YES, S is subsequence of T\n", "red")
else:
    TAc.print("\n\n#NO, S is not a subsequence of T\n", "red")

if(ENV['YES_cert'] == 1 and ret[0]):
    print("#YES CERTIFICATE:")
    if ENV['seed'] != 's_and_T_proposed_by_problem_solver':
        string_T = list_to_string(T)
    print(remove_duplicate_spaces(string_T))
    print(get_yes_certificate(T, ret[1]))


