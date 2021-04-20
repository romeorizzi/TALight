#!/usr/bin/env python3
from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="is_subseq_server"
args_list = [
    ('T',str),
    ('s',str),
    ('lang',str),
    ('YES_cert',bool),
    ('seed', str)
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
seed = ENV['seed']

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")

string_T = ""
string_s = ""

if re.match(r"^[1-9]|[0-9]{2,5}$", seed):
    n_seed = int(seed)
    T = generate_random_seq(10,100,n_seed)
    


if (ENV['T'] == 'lazy_input' and ENV['seed'] == 's_and_T_proposed_by_problem_solver'):
    TAc.print("\nIn this problem you are asked to enter a sequence T of numbers with a blank space between each number (example: 12 34 56 ...) and a sequence s. You will be told if s is a sub-sequence of T.", "green")
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

if (ENV['s'] == 'lazy_input' and ENV['seed'] == 's_and_T_proposed_by_problem_solver'):
    TAc.print("\nInsert s:", "green")
    string_s = input()
    ok = bool(re.match(r"^((([1-9][0-9]{0,9} *)*[1-9][0-9]{0,9}))$", string_s))
    if ok:
        s = parse_input(string_s)
    else:
        TAc.print("\n\nWRONG INPUT FORMAT: this is not a sequence of numbers (example: 12 34 56 ...).\n", "red")
        exit(0)
else:
    string_s = ENV['s']
    s = parse_input(string_s)

ret = is_subseq_with_position(s,T)

if ret[0]:
    TAc.print("\n\nYES, s is subsequence of T\n", "red")
else:
    TAc.print("\n\nNO, s isn't subsequence of T\n", "red")

if(ENV['YES_cert'] == 1 and ret[0]):
    print("YES CERTIFICATE")
    print(remove_duplicate_spaces(string_T))
    print(get_yes_certificate(T, ret[1]))


