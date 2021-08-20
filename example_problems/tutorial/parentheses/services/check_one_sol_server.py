#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from parentheses_lib import recognize

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="check_one_sol_server"
args_list = [
    ('input_formula',str),
    ('n',str),
    ('silent',bool),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 
n=ENV['n']
len_input = len(ENV["input_formula"])//2
def answer():
    if recognize(ENV["input_formula"], TAc, LANG) and not ENV["silent"]:
        TAc.OK()
        TAc.print(LANG.render_feedback("ok", f' Your string is a well-formed formula with {len_input} pairs of parentheses.'), "yellow", ["bold"])

if n=='free':
    answer()
else:
    if len_input==int(n):
        answer()
    elif recognize(ENV["input_formula"], TAc, LANG):
        TAc.print(LANG.render_feedback("different_lengths", f"No! Your string represents a valid formula of parentheses but not of {n} pairs."), "red", ["bold"])
exit(0)
