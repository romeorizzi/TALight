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

def calculate_path(triangle,path_values):
    triangle_array = cast_to_array(triangle)
    n = len(triangle)
    path = [triangle_array[0]]
    s = triangle_array[0]
    i = 0
    last_pos = 0
    for move in path_values:
        if(move == "L"):
            path.append(triangle_array[i+1 + last_pos])
            s += triangle_array[i+1 + last_pos]
            last_pos += i + 1 
        else:
            path.append(triangle_array[i+2 + last_pos])
            s += triangle_array[i+2 + last_pos]
            last_pos += i + 2 
        i += 1
    return s

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
        directions = ["L","R"]
        path = ""
        seed = random.randint(100000,999999)
        for _ in range(n-1):
            path += random.choice(directions)
        instances.append([tl.random_triangle(n, 0, 99, seed, TAc, LANG),path,seed,n])
        n = math.ceil(n*scaling_factor)
        if n>MAX_ROWS:
            n = MAX_ROWS
            
#CHECK TIME ELAPSED         
for el in instances:
    start = monotonic() 
    answer = int(input([el[0],el[1]]))
    end = monotonic()
    time += end-start
    if answer != calculate_path(el[0],el[1]):
        TAc.NO()
        TAc.print(LANG.render_feedback("no-wrong-sol", f'{answer} is the wrong solution. The  reward for this path in this triangle (seed:{el[2]}, {el[3]} rows) is {calculate_path(el[0],el[1])}.'), "red")
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





































# CHECK WHETHER THE PATH L/R ENCODING STRING HAS THE RIGHT LENGTH

if len(ENV["path"].replace(" ", "")) != ENV["n"]-1:
    TAc.NO()
    if len(ENV["path"].replace(" ", "")) < ENV["n"]-1:
        TAc.print(LANG.render_feedback("path-too-short", f'The string of the L/R choices encoding your path is too short for a triangle with n={ENV["n"]} rows.'), "red", ["bold"])
    if len(ENV["path"].replace(" ", "")) > ENV["n"]-1:
        TAc.print(LANG.render_feedback("path-too-long", f'The string of the L/R choices encoding your path is too long for a triangle with n={ENV["n"]} rows.'), "red", ["bold"])
    TAc.print(LANG.render_feedback("wrong-path-length", f'The true number of required choices is n-1={ENV["n"]-1} instead of {len(ENV["path"].replace(" ", ""))}.'), "red", ["bold"])
    exit(0)


# TRIANGLE GENERATION

if ENV['how_to_input_the_triangle'] == "my_own_triangle":
    triangle = []
    TAc.print(LANG.render_feedback("insert-triangle", f'Please, insert your triangle, line by line. For every i in [1,{ENV["n"]}], line i comprises i integers separated by spaces.'), "yellow", ["bold"])
    for i in range(1,ENV["n"]+1):
        TAc.print(LANG.render_feedback("insert-line", f'Insert line i={i}, that is, {i} integers separated by spaces:'), "yellow")
        line = TALinput(int, i, token_recognizer=lambda val,TAc,LANG: tl.check_val_range(val,0,99,TAc,LANG), TAc=TAc, LANG=LANG)
        triangle.append(line)
    TAc.OK()
    TAc.print(LANG.render_feedback("triangle-insertion-completed", f'Insertion complete. Your triangle has been successfully inserted.'), "green")
else:
    triangle = tl.random_triangle(ENV["n"],0,99,int(ENV['how_to_input_the_triangle']),TAc,LANG)
if not ENV['silent'] or ENV['display_triangle'] or ENV['reward_the_path'] or ENV['how_to_input_the_triangle'] == "my_own_triangle":
    TAc.print(LANG.render_feedback("feasible-path", f'Your solution path ({ENV["path"]}) is a feasible one for this problem since it comprises {ENV["n"]-1} subsequent choices of directions (the correct number).'), "green", ["bold"])
if ENV['display_triangle']:
    TAc.print(LANG.render_feedback("display-triangle", f'The triangle of reference is the following:'), "green", ["bold"])
    tl.print_triangle(triangle)
if ENV['reward_the_path']:
    TAc.print(LANG.render_feedback("path-reward", f'The total reward collected by your path is {tl.calculate_path(triangle,ENV["path"].replace(" ", ""))}.'), "green", ["bold"])        

exit(0)
