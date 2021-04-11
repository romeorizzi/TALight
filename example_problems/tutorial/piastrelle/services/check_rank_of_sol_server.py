#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="piastrelle"
service="check_rank_of_sol"
args_list = [
    ('n',int),
    ('sorting_criterion',str),
    ('more_or_less_hint_if_wrong',bool),
    ('lang',str),
    ('ISATTY',bool),
]
 
from sys import stderr, exit, argv
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from piastrelle_lib import Par
import random

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
n_tiles=ENV['n']
p = Par(n_tiles)
pos=random.randint(0,p.num_sol(n_tiles)-1)
print('In what position of the tiling does '+ str(p.unrank(n_tiles)[pos]) +' fit? \nWrite it here: ')
risp=int(input())       
if ENV['sorting_criterion']=='loves_long_tiles':
    risp1=p.num_sol(n_tiles)-risp+1
    if risp1-1 == pos:
        TAc.print(LANG.render_feedback("risp-ok", f"Ok! {risp} is the position of {p.unrank(n_tiles)[pos]} in the list of tilings of a corridor of dimension 1x{n_tiles}."), "green", ["bold"])
        exit(0)
    else: 
        TAc.print(LANG.render_feedback("risp-no", f"No, {risp} is not the position of {p.unrank(n_tiles)[pos]} in the list of tilings of a corridor of dimension 1x{n_tiles}."), "red", ["bold"])
        if ENV['more_or_less_hint_if_wrong']:
            if risp1-1 > pos:
                TAc.print(LANG.render_feedback("hint-up", f"The correct position is strictly more than {risp}."), "red", ["bold"])
            elif risp1-1 < pos:
                TAc.print(LANG.render_feedback("hint-down", f"The correct position is strictly less than {risp}."), "red", ["bold"])
        exit(0)
if risp-1 == pos:
        TAc.print(LANG.render_feedback("risp-ok", f"Ok! {risp} is the position of {p.unrank(n_tiles)[pos]} in the list of tilings of a corridor of dimension 1x{n_tiles}."), "green", ["bold"])
        exit(0)
else: 
    TAc.print(LANG.render_feedback("risp-no", f"No, {risp} is not the position of {p.unrank(n_tiles)[pos]} in the list of tilings of a corridor of dimension 1x{n_tiles}."), "red", ["bold"])
    if ENV['more_or_less_hint_if_wrong']:
        if risp-1 < pos:
            TAc.print(LANG.render_feedback("hint-up", f"The correct position is strictly more than {risp}."), "red", ["bold"])
        elif risp-1 > pos:
            TAc.print(LANG.render_feedback("hint-down", f"The correct position is strictly less than {risp}."), "red", ["bold"])
    exit(0)

