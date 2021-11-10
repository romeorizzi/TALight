#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
problem="triangle"
service="check_sol_value"
args_list = [
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('how_to_input_the_triangle',str),
    ('opt_sol_val',int),
    ('feedback',str),
    ('silent',bool),
]


ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 

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

best_reward = tl.best_path_cost(triangle)

if ENV['opt_sol_val'] == best_reward:
    if ENV['feedback'] == "yes_no" or not ENV['silent']:
        TAc.OK()
        TAc.print(LANG.render_feedback("right-best-sol", f'We agree, the solution value you provided is the best one for your triangle.'), "green", ["bold"])
    exit(0)
else:
    if ENV['feedback'] == "yes_no":
        TAc.NO()
        TAc.print(LANG.render_feedback("wrong-best-sol", f'We don\'t agree, the solution value you provided is not the best one for your triangle.'), "red", ["bold"])
    if ENV['feedback'] == "bigger_or_smaller":    
        if ENV['opt_sol_val'] < best_reward:
            TAc.NO()
            TAc.print(LANG.render_feedback("smaller-than-best", f'We don\'t agree, the solution value you provided is smaller than the best one for your triangle.'), "red", ["bold"])
            exit(0)
        TAc.NO()
        TAc.print(LANG.render_feedback("bigger-than-best", f'We don\'t agree, the solution value you provided is bigger than the best one for your triangle.'), "red", ["bold"])
        exit(0)
if ENV['feedback'] == "true_opt_val":
    TAc.print(LANG.render_feedback("best-value", f'The best reward for your triangle is {best_reward}.'), "yellow", ["bold"])
    exit(0)
           
exit(0)
