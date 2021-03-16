#!/usr/bin/env python3
from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import parse_input, is_subseq

# METADATA OF THIS TAL_SERVICE:
problem="increasing_subsequcence"
service="is_subseq_server"
args_list = [
    ('T',str),
    ('s',str),
    ('lang',str),
    ('YES_cert',bool),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")


if (ENV['T'] == 'lazy_input'):
    TAc.print("\nInsert T:", "green")
    string = input()
    ok = bool(re.match(r"^((([1-9][0-9]{0,9} )*[1-9][0-9]{0,9}))$", string))
    if ok:
        T = parse_input(string)
    else:
        TAc.print("\n\nWRONG INPUT FORMAT\n", "red")
        exit(0)
else:
    T = parse_input(ENV['T'])

if (ENV['s'] == 'lazy_input'):
    TAc.print("\nInsert s:", "green")
    string = input()
    ok = bool(re.match(r"^((([1-9][0-9]{0,9} )*[1-9][0-9]{0,9}))$", string))
    if ok:
        s = parse_input(string)
    else:
        TAc.print("\n\nWRONG INPUT FORMAT\n", "red")
        exit(0)
else:
    s = parse_input(ENV['s'])

valid = is_subseq(s,T)

if valid:
    TAc.print("\n\nYES, s is substring of T\n", "red")
else:
    TAc.print("\n\nNO, s isn't substring of T\n", "red")


