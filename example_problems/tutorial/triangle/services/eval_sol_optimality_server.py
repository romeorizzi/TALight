#!/usr/bin/env python3
from sys import stderr, exit

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

def cast_to_array(triangle):
    array = []
    for i in triangle:
        array += i
    return array

def best_path_cost(triangle):
    dist = len(triangle)
    triangle_array = cast_to_array(triangle)
    triangle_array = triangle_array[::-1]
    i  = 0
    count = 1
    while dist > 1:
        triangle_array[i + dist] = max(triangle_array[i] + triangle_array[i + dist], triangle_array[i + 1] + triangle_array[i + dist])
        count += 1
        i += 1
        if count == dist:
            count = 1
            dist -= 1
            i += 1
    return triangle_array[i]

instances = []
MAX_ROWS = 10
NUM_OF_INSTANCES = 10
#EFFICIENT
if ENV["goal"] == "efficient":
    MAX_ROWS *= 5
    NUM_OF_INSTANCES *=5
    if ENV["code_lang"] == "compiled":
        MAX_ROWS *= 2
    scaling_factor = 1.3
    n = 1
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
    n = 1
    for _ in range(NUM_OF_INSTANCES):
        seed = random.randint(100000,999999)
        instances.append([tl.random_triangle(n, 0, 99, seed, TAc, LANG),seed,n])
        n = math.ceil(n*scaling_factor)
        if n>MAX_ROWS:
            n = MAX_ROWS
            
#CHECK TIME ELAPSED         
for el in instances:
    start = monotonic() 
    p = int(input(el[0]))
    end = monotonic()
    time += end-start
    if p != best_path_cost(el[0]):
        TAc.NO()
        TAc.print(LANG.render_feedback("no-wrong-sol", f'{p} is the wrong solution. The best reward for this triangle (seed:{el[1]}, {el[2]} rows) is {best_path_cost(el[0])}'), "red")
        exit(0)
    print(f'Correct! The answer is {p} [took {time} seconds on your machine]')
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
