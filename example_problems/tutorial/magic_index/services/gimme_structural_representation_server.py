#!/usr/bin/env python3
from sys import stderr, exit
import re,random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('r', str),
    ('representation', str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

initial_representation =ENV['r']

# START CODING YOUR SERVICE:
if ENV['representation']=='simple_structural': 
    new_representation = simple_strucural_rep(initial_representation)
    TAc.print(LANG.render_feedback("game representation", f'The simple structural representation is: {new_representation}\n'), "white", ["bold"], end="")

elif ENV['representation']=='reiforced_structural':
    new_representation =  reinforced_strucural_rep(initial_representation, False, TAc, LANG)
    TAc.print(LANG.render_feedback("game representation", f'The simple structural representation is: {new_representation}\n'), "white", ["bold"], end="")
    
else:
    new_representation = reinforced_strucural_rep(initial_representation, True, TAc, LANG)
    TAc.print(LANG.render_feedback("game representation", f'The simple structural representation is: {new_representation}\n'), "white", ["bold"], end="")
