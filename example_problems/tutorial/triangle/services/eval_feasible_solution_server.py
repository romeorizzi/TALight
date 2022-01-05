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
    
# GENERATE INSTANCES

instances = []
MAX_ROWS = 10
NUM_OF_INSTANCES = 25
#EFFICIENT
if ENV["goal"] == "efficient":
    MAX_ROWS *= 5
    if ENV["code_lang"] == "compiled":
        MAX_ROWS *= 2
    scaling_factor = 1.3
    n = 2
    for _ in range(NUM_OF_INSTANCES):
        seed = random.randint(100000,999999)
        instances.append(tl.random_triangle(n, 0, 99, seed, TAc, LANG))
        n = math.ceil(n*scaling_factor)
        if n>MAX_ROWS:
            n = MAX_ROWS
#NOT EFFICIENT
else:
    if ENV["code_lang"] == "compiled":
        MAX_ROWS *= 2
    scaling_factor = 1.3
    n = 2
    for _ in range(NUM_OF_INSTANCES):
        seed = random.randint(100000,999999)
        instances.append(tl.random_triangle(n, 0, 99, seed, TAc, LANG))
        n = math.ceil(n*scaling_factor)
        if n>MAX_ROWS:
            n = MAX_ROWS
            
def right_length(triangle,answer):
    if len(triangle) == len(answer)+1:
        return True
    return False

def is_feasible_solution(path):                  
    for el in path:           
        if el != "R" and el != "L":
            return False
    return True 

#CHECK TIME ELAPSED  
time = 0       
for triangle in instances:
    start = monotonic()
    TAc.print(LANG.render_feedback("triangle-size",'We have a triangle whose number of rows is:'), "white", ["bold"])
    TAc.print(len(triangle), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("triangle-instance",'Triangle instance of reference:'), "white", ["bold"])
    tl.print_triangle(triangle)
    TAc.print(LANG.render_feedback("ask-path", f'\nGiven this triangle, can you provide a feasible solution?'),"white",["bold"])
    answer = TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
    end = monotonic()
    time += end-start
    if not right_length(triangle,answer):
        TAc.NO()
        if len(answer) < len(triangle) -1:
            TAc.print(LANG.render_feedback("no-way-short", f'{answer} is not a feasible solution, as it is too short.'), "red")
        else:
            TAc.print(LANG.render_feedback("no-way-long", f'{answer} is not a feasible solution, as it is too long.'), "red")
        exit(0)
    if not is_feasible_solution(answer):
        TAc.NO()
        TAc.print(LANG.render_feedback("no-way-wrong-directions", f'{answer} is not a feasible solution, as it contains directions different from "L" or "R".'), "red")
        exit(0)
    print(f'Correct! [took {time} seconds on your machine]')
    if time > 3:
        TAc.OK()
        TAc.print(LANG.render_feedback("seems-correct-weak", f'Your solution answers correctly on a first set of instances, but it took too much to answer to the last triangle.'), "green")
        exit(0)

TAc.OK()
TAc.print(LANG.render_feedback("seems-correct-strong", f'Your solution appears to be correct (checked on several instances).'), "green")
if ENV["goal"] == "efficient":
    TAc.OK()
    TAc.print(LANG.render_feedback("efficient", f"Your solution's running time is linear in the depth of the triangle."), "green")
 
exit(0)
