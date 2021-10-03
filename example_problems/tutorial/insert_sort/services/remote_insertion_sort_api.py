#!/usr/bin/env python3
from sys import exit
import re
import random
from itertools import zip_longest

import insert_sort_lib
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from sys import stdout, stderr, exit, argv

# METADATA OF THIS TAL_SERVICE:
problem = "insert_sort"
service = "log_debug_your_insertion_sort_bot_server"
args_list = [
    ('feedback', str),
    ('lang', str),
]


#ENV = Env(problem, service, args_list)
#TAc = TALcolors(ENV)
#LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
