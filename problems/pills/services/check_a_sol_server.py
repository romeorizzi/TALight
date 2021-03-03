#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_a_sol"
args_list = [
    ('one_solution',str),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

num_H_pills = 0
for day, i in zip(ENV['one_solution'],range(1,len(ENV['one_solution'])+1)):
    if day == 'I':
        num_H_pills += 1
    else:
        if num_H_pills == 0:
            TAc.print(ENV['one_solution'], "yellow", ["underline"])
            TAc.print(LANG.render_feedback("unfeasible", f"No. On the evening of day {i} there in no single half pill left in the bottle. Are you sure you have not swallowed a rat?"), "red", ["bold"])
            exit(0)
        num_H_pills -= 1

if num_H_pills > 0:
    TAc.print(ENV['one_solution'], "yellow", ["underline"])
    TAc.print(LANG.render_feedback("unfinished", f"No. You have not finished the treatment. When following your prescription string there are some half pills left in the bottle."), "red", ["bold"])
    exit(0)
if not ENV['silent']:
    TAc.OK()
    TAc.print(LANG.render_feedback("ok", f"Your solution is a valid treatment."), "yellow", ["bold"])
exit(0)
