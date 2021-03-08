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

from recognize import recognize

risp = recognize(ENV["input_formula"], TAc, LANG)

if risp and not ENV['silent']:
    TAc.OK()
    TAc.print(LANG.render_feedback("ok", f"Your string is a well-formed formula of parentheses."), "yellow", ["bold"])
exit(0)
