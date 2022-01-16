#!/usr/bin/env python3
from sys import exit
import re
import numpy as np
from itertools import zip_longest
import insert_sort_lib
import log_debug_your_insertion_sort_bot_server
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from sys import stdout, stderr, exit, argv

# METADATA OF THIS TAL_SERVICE:
problem = "bubble_sort"
service = "log_debug_your_bubble_sort_bot_server"
args_list = [
    ('feedback', str),
    ('lang', str),
    ('goal', str)
]


# ENV = Env(problem, service, args_list)
# TAc = TALcolors(ENV)
# LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:


