#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from pills_lib import recognize

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_one_sol_server"
args_list = [
    ('input_treatment',str),
    ('n',str),
    ('silent',bool),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 
n=ENV['n']
len_input = len(ENV["input_treatment"])//2
def answer():
    if recognize(ENV["input_treatment"], TAc, LANG) and not ENV["silent"]:
        TAc.OK()
        TAc.print(LANG.render_feedback("ok", f'Your string is a feasible treatment with {len_input} pills.'), "yellow", ["bold"])
if n=='free':
    answer()
else:
    if len_input==int(n):
        answer()
    elif recognize(ENV["input_treatment"], TAc, LANG):
        TAc.print(LANG.render_feedback("different_lengths", f"No! Your string represents a feasible treatment but not of {n} pills."), "red", ["bold"])
exit(0)
