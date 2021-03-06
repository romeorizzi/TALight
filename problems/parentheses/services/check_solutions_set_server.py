#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="check_solutions_set"
args_list = [
    ('feedback',str),   # regex: ^(yes_no|tell_a_minimal_missing_prefix|give_one_missing)$
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
from random import randrange

from get_lines import get_lines_from_stream
from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

# def check_entry_integer(row_index_name,col_index_name,entry_val):
#    if type(entry_val) != int:
#        print(f"# Error (in the table format): the entry ({row_index_name},{col_index_name}) in your table represents the floor from which to throw the first of {row_index_name} eggs when the floors are {col_index_name} (numbered from 1 to {col_index_name}). As such entry ({row_index_name},{col_index_name}) should be a natural number. However, the value {entry_val} is a non integer float with decimal part.")
#        exit(1)        




exit(0)
