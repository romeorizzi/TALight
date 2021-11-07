#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('n',int),
    ('sorting_criterion',str),
]
 
from sys import stderr, exit
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from piastrelle_lib import Par, recognize
import random

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
n_tiles=ENV['n']
p=Par(n_tiles)
pos=random.randint(1,p.num_sol(n_tiles))
print('What is the tiling for n = '+str(n_tiles)+' in position '+str(pos)+' ? \nWrite it here: ')
stopping_command_set={'#end'}

line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\[|\]|-)+$", regex_explained="any string of '[' , ']' and '-' characters.", TAc=TAc)
if not recognize(line, TAc, LANG):
    TAc.print(LANG.render_feedback("first-line-not-well-formed", f"No. Your very first tailing is not well formed."), "red", ["bold"])
    exit(0)
if not len(line)//2 == n_tiles:
    TAc.print(LANG.render_feedback("different_lengths", f"No. The tiling you just introduced is not of length {n_tiles}."), "red", ["bold"])
    exit(0)


# if ENV['sorting_criterion']=='loves_long_tiles':
#     new=p.unrank(n_tiles)[::-1]
    # if not line==new[pos-1]:
    #     TAc.print(LANG.render_feedback("answer-no", f"No. The tiling you introduced is not at the position {pos}."), "red", ["bold"])
    #     exit(0)
elif not line==p.unrank(n_tiles,pos,ENV['sorting_criterion']):
        TAc.print(LANG.render_feedback("answer-no", f"No. The tiling you introduced is not at the position {pos}."), "red", ["bold"])
        exit(0)
TAc.print(LANG.render_feedback("answer-yes", f"Yes! The tiling introduced is right."), "green", ["bold"])
exit(0)