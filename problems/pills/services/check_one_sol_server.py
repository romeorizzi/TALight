#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_one_sol_server"
args_list = [
    ('input_sol',str),
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

num_H_pills = 0
for day, i in zip(ENV['input_sol'],range(1,len(ENV['input_sol'])+1)):
    if day == 'I':
        num_H_pills += 1
    else:
        if num_H_pills == 0:
            TAc.print(ENV['input_sol'], "yellow", ["underline"])
            TAc.print(LANG.render_feedback("unfeasible", f"No. On the evening of day {i} there in no single half pill left in the bottle. Are you sure you have not swallowed a rat?"), "red", ["bold"])
            exit(0)
        num_H_pills -= 1

if num_H_pills > 0:
    TAc.print(ENV['input_sol'], "yellow", ["underline"])
    TAc.print(LANG.render_feedback("unfinished", f"No. You have not finished the treatment. When following your prescription string there are some half pills left in the bottle."), "red", ["bold"])
    exit(0)
if not ENV['silent']:
    TAc.OK()
    TAc.print(LANG.render_feedback("ok", f"Your solution is a valid treatment."), "yellow", ["bold"])
exit(0)
