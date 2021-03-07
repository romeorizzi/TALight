#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem=""
service="parentheses"
args_list = [
    ('input_formula',str),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

num_dangling_open = 0
for day, i in zip(ENV['input_formula'],range(1,len(ENV['input_formula'])+1)):
    if day == '(':
        num_dangling_open += 1
    else:
        if num_dangling_open == 0:
            TAc.print(ENV['input_formula'], "yellow", ["underline"])
            TAc.print(LANG.render_feedback("unfeasible", f"No. On position {i} there is no open parenthsis left to be closed. This formula is not well formed."), "red", ["bold"])
            exit(0)
        num_dangling_open -= 1

if num_dangling_open > 0:
    TAc.print(ENV['input_formula'], "yellow", ["underline"])
    TAc.print(LANG.render_feedback("unfinished", f"No. You have left {num_dangling_open} open parenthesis unclosed. This formula is not well formed. It contains more '(' than ')' characters."), "red", ["bold"])
    exit(0)
if not ENV['silent']:
    TAc.OK()
    TAc.print(LANG.render_feedback("ok", f"Your string is a well-formed formula of parentheses."), "yellow", ["bold"])
exit(0)
