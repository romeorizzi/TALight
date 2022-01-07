#!/usr/bin/env python3

"""SERVICE YET TO BE IMPLEMENTED. THIS FILE IS JUST A PLACEHOLDER."""

print("Sorry! This service has not yet been implemented\n(will you be the one to take care of it?\n --- RIGHT NOW THIS FILE IS JUST AN HANDY PLACEHOLDER ---")

exit(0)

#!/usr/bin/env python3
from sys import stderr, stdout, exit, argv
from random import randrange
from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

# METADATA OF THIS TAL_SERVICE:
problem="problem_name"
service="service_name"
args_list = [
    ('arg1',int),
    ('arg2',str),
    ('arg3',bool),
    ('lang',str),
    ('META_TTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

gen_new_s = True    
for _ in range(ENV['num_questions']):
  pass
