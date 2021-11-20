#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('how_to_input_the_triangle',str),
    ('path',str),
    ('display_triangle',bool),
    ('reward_the_path',bool),
    ('silent',bool),
]


ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 

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
        line = TALinput(int, i, token_recognizer=lambda val,TAc,LANG: tl.check_val_range(val,ENV['MIN_VAL'],ENV['MAX_VAL'],TAc,LANG), TAc=TAc, LANG=LANG)
        triangle.append(line)
    TAc.OK()
    TAc.print(LANG.render_feedback("triangle-insertion-completed", f'Insertion complete. Your triangle has been successfully inserted.'), "green")
else:
    triangle = tl.random_triangle(ENV["n"],ENV['MIN_VAL'],ENV['MAX_VAL'],ENV['how_to_input_the_triangle'])
if not ENV['silent'] or ENV['display_triangle'] or ENV['reward_the_path'] or ENV['how_to_input_the_triangle'] == "my_own_triangle":
    TAc.print(LANG.render_feedback("feasible-path", f'Your solution path ({ENV["path"]}) is a feasible one for this problem since it comprises {ENV["n"]-1} subsequent choices of directions (the correct number).'), "green", ["bold"])
if ENV['display_triangle']:
    TAc.print(LANG.render_feedback("display-triangle", f'The triangle of reference is the following:'), "green", ["bold"])
    tl.print_triangle(triangle)
if ENV['reward_the_path']:
    TAc.print(LANG.render_feedback("path-reward", 'Your path collects the following reward values when descending the triangle:'), "green", ["bold"])
    print(tl.calculate_path(triangle,ENV["path"].replace(" ", ""))[0])
    TAc.print(LANG.render_feedback("path-reward", f'The total reward collected by your path is {tl.calculate_path(triangle,ENV["path"].replace(" ", ""))[1]}.'), "green", ["bold"])        

exit(0)
