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
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 
if not ENV["silent"]:
    TAc.print(LANG.opening_msg, "green")

if recognize(ENV["input_formula"], TAc, LANG) and not ENV["silent"]:
    TAc.OK()
    TAc.print(LANG.render_feedback("ok", f'♥  Your string is a well-formed formula of parentheses.'), "yellow", ["bold"])
exit(0)
