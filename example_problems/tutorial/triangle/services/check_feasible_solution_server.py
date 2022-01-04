#!/usr/bin/env python3
from sys import stderr, exit
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('MIN_VAL',int),
    ('MAX_VAL',int),
]


ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE:

# TRIANGLE AND PATH GENERATION

n = random.randint(1,30)
seed = random.randint(100000,999999)
triangle= tl.random_triangle(n, ENV['MIN_VAL'], ENV['MAX_VAL'], seed, TAc, LANG)
path = tl.random_path(n-2,n)
if len(triangle) -1 == len(path):
    right_answer = "yes"
else:
    right_answer = "no"
TAc.print(LANG.render_feedback("triangle-size","We have a triangle whose number of rows is:"), "white", ["bold"])
TAc.print(len(triangle), "yellow", ["bold"])
TAc.print(LANG.render_feedback("triangle-instance","Triangle instance of reference:"), "white", ["bold"])
tl.print_triangle(triangle)
TAc.print(LANG.render_feedback("display-path", f'\nGiven this triangle, do you think the following path offers a feasible solution?'), "white", ["bold"])
TAc.print(path, "yellow", ["bold"])
TAc.print(LANG.render_feedback("prompt", f'\nType [yes/no] to answer.'), "white", ["bold"])
answer = TALinput(str, line_recognizer=lambda val,TAc,LANG: tl.check_yes_or_no_answer(val,TAc,LANG), TAc=TAc, LANG=LANG)[0]
if answer == right_answer:
    if not ENV['silent']:
        TAc.OK()
        TAc.print(LANG.render_feedback("right-answer", f'# We agree, the answer is {right_answer}.'), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-answer", f'# We don\'t agree, the answer is {right_answer}.'), "red", ["bold"])
exit(0)
