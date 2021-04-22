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
    print(T[0])


if (ENV['T'] == 'lazy_input' and ENV['seed'] == 's_and_T_proposed_by_problem_solver'):
    TAc.print("\n#In this problem you are asked to enter a sequence T of numbers with a blank space between each number (example: 12 34 56 ...) and a sequence s. You will be told if s is a sub-sequence of T.", "green")
    TAc.print("\n#Insert the sequence T:", "green")
    string_T = input()
    ok = bool(re.match(r"^((([1-9][0-9]{0,9} *)*))$", string_T))
    if ok:
        T = parse_input(string_T)
    else:
        TAc.print("\n\n#WRONG INPUT FORMAT: this is not a sequence of numbers (example: 12 34 56 ...).\n", "red")
        exit(0)
elif ENV['T'] != 'lazy_input':
    string_T = ENV['T']
    T = parse_input(string_T)

if (ENV['s'] == 'lazy_input'):
    TAc.print("\n#Insert the subsequence s:", "green")
    string_s = input()
    ok = bool(re.match(r"^((([1-9][0-9]{0,9} *)*))$", string_s))
    if ok:
        s = parse_input(string_s)
    else:
        TAc.print("\n\n#WRONG INPUT FORMAT: this is not a sequence of numbers (example: 12 34 56 ...).\n", "red")
        exit(0)
else:
    string_s = ENV['s']
    s = parse_input(string_s)


print(s, T[0])
ret = is_subseq_with_position(s,T[0])
print(ret)

if ret[0]:
    TAc.print("\n\n#YES, s is subsequence of T\n", "red")
else:
    TAc.print("\n\n#NO, s is not a subsequence of T\n", "red")

if(ENV['YES_cert'] == 1 and ret[0]):
    print("#YES CERTIFICATE")
    if ENV['seed'] != 's_and_T_proposed_by_problem_solver':
        string_T = list_to_string(T[0])
    print(remove_duplicate_spaces(string_T))
    print(get_yes_certificate(T[0], ret[1]))


