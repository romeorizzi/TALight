#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from pills_lib import recognize

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_one_sol_server"
args_list = [
    ('input_treatment',str),
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

if recognize(ENV["input_treatment"], TAc, LANG) and not ENV["silent"]:
    TAc.OK()
    TAc.print(LANG.render_feedback("ok", f'♥  Your string is a feasible treatment.'), "yellow", ["bold"])
exit(0)
