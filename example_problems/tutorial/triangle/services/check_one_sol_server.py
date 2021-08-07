#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from piastrelle_lib import recognize

# METADATA OF THIS TAL_SERVICE:
problem="piastrelle"
service="check_one_sol_server"
args_list = [
    ('input_formula',str),
    ('n',str),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 
n=ENV['n']
len_input = len(ENV["input_formula"])//2
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")
def answer():
    if recognize(ENV["input_formula"], TAc, LANG) and not ENV['silent']:
        TAc.OK()
        TAc.print(LANG.render_feedback("ok", f"Your string represents a valid tiling of a corridor 1x{len_input}."), "yellow", ["bold"])

if n=='free':
    answer()
else:
    if len_input==int(n):
        answer()
    elif recognize(ENV["input_formula"], TAc, LANG) and not ENV['silent']:
        TAc.print(LANG.render_feedback("different_lengths", f"No! Your string represents a valid tiling but not of a corridor of dimension 1x{n}."), "red", ["bold"])
exit(0)