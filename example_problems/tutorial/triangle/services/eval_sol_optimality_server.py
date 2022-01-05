#!/usr/bin/env python3
from sys import stderr, exit

import random
import math
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('code_lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

instances = []
MAX_ROWS = 10
NUM_OF_INSTANCES = 10
#EFFICIENT
if ENV["goal"] == "efficient":
    MAX_ROWS *= 5
    NUM_OF_INSTANCES *=5
    if ENV["code_lang"] == "compiled":
        MAX_ROWS *= 2
    scaling_factor = 1.4

#NOT EFFICIENT
else:
    if ENV["code_lang"] == "compiled":
        MAX_ROWS *= 2
    scaling_factor = 1.3
n = 2
for _ in range(NUM_OF_INSTANCES):
    seed = random.randint(100000,999999)
    instances.append([tl.random_triangle(n, 0, 99, seed, TAc, LANG),seed,n])
    n = math.ceil(n*scaling_factor)
    if n>MAX_ROWS:
        n = MAX_ROWS
            
#CHECK TIME ELAPSED         
for el in instances:
    time = 0
    triangle = el[0]
    seed = el[1]
    n = el[2]
    TAc.print(LANG.render_feedback("triangle-size", f'We give you a triangle with this number of rows:'), "white")
    print(n)
    TAc.print(LANG.render_feedback("print-triangle", f'The triangle of reference is:'), "white")
    tl.print_triangle(triangle)
    TAc.print(LANG.render_feedback("rought-triangle", f'The triangle can be seen as a list of lists. In this case we have:'), "white")
    print(triangle)
    TAc.print(LANG.render_feedback("best-path-question", f'Which is the best collectable reward in this triangle?'), "white")
    start = monotonic() 
    answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
    end = monotonic()
    time += end-start
    if answer != tl.best_path_cost(el[0]):
        TAc.NO()
        TAc.print(LANG.render_feedback("no-wrong-sol", f'{answer} is the wrong solution. The best reward for this triangle (seed:{seed}, {n} rows) is {tl.best_path_cost(triangle)}'), "red")
        exit(0)
    print(f'Correct! The answer is {answer} [took {time} seconds on your machine]')
    if ENV['goal'] == 'efficient':
        if time > 1:
            TAc.OK()
            TAc.print(LANG.render_feedback("seems-correct-weak", f'Your solution answers correctly on a first set of instances, but it took too much to answer to the last instance.'), "green")
            exit(0)
    else:
        if time > 50:
            TAc.OK()
            TAc.print(LANG.render_feedback("seems-correct-weak", f'Your solution answers correctly on a first set of instances, but it took too much to answer to the last instance.'), "green")
            exit(0)

TAc.OK()
TAc.print(LANG.render_feedback("seems-correct-strong", f'Your solution appears to be correct (checked on several instances).'), "green")
if ENV["goal"] == "efficient":
    TAc.OK()
    TAc.print(LANG.render_feedback("efficient", f"Your solution's running time is linear in the depth of the triangle."), "green")
exit(0)
