#!/usr/bin/env python3
from sys import stderr, exit
import re,random

from numpy import single

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('r', str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

r = ENV['r']


# START CODING YOUR SERVICE:
vector_configuration = get_server_vec_representation(r)
know_nothing = True

if '0' not in vector_configuration:
    unknown, optimal_pos = get_positions_f(vector_configuration)
else:
    unknown, optimal_pos = get_positions_g(vector_configuration)
    know_nothing = False

if optimal_pos == None or (not know_nothing and all(v is None for v in optimal_pos)):
    TAc.print(LANG.render_feedback("no optimal pos", f'There is/are not optimal move/s for this configuration! You already know everything...'), "white", ["bold"])
else:
    single_pos = 'is'
    if not know_nothing:
        single_pos = 'is' if None in optimal_pos else 'are'
        try:
            optimal_pos.remove(None)
        except:
            pass
    
    TAc.print(LANG.render_feedback("optimal pos", f'The optimal pos to play given this configuration {single_pos} : {optimal_pos}'), "white", ["bold"])