#!/usr/bin/env python3
from sys import stderr, exit
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('displayable',bool),
    ('how_to_input_the_triangle',str),
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
    path = tl.random_path(ENV['n'])
elif ENV['how_to_input_the_triangle'] == "random":
    n = 0
    if ENV['displayable']:
        n =random.randint(1,20)
    else:
        n=random.randint(1,100)
    seed = random.randint(100000,999999)
    triangle = tl.random_triangle(n, ENV['MIN_VAL'], ENV['MAX_VAL'], seed, TAc, LANG)
    path = tl.random_path(n-1,n)
else:
    triangle = tl.random_triangle(ENV["n"],ENV['MIN_VAL'],ENV['MAX_VAL'],int(ENV['how_to_input_the_triangle']),TAc,LANG)
    path = tl.random_path(ENV['n'],ENV['n']) 
if ENV['displayable']:
    TAc.print(LANG.render_feedback("displayable-path",f'The path {path} moving towards the bottom of the triangle is displayed here:\n'), "green")
    tl.print_path(triangle,path,TAc,LANG)
TAc.print(LANG.render_feedback("reward-question", f'\nGiven this path, which reward does it collect?\nYour answer shall be a positive integer.'), "green")
right_answer = tl.calculate_path(triangle,path)
answer = TALinput(int, token_recognizer=lambda val,TAc,LANG: True, TAc=TAc, LANG=LANG)[0]
if answer == right_answer:
    if not ENV['silent'] or ENV['feedback'] == "yes_no":
        TAc.OK()
        TAc.print(LANG.render_feedback("right-answer", f'We agree, the answer is {right_answer}.'), "green", ["bold"])
else:
    TAc.NO()
    if ENV['feedback'] == "yes_no":
        TAc.print(LANG.render_feedback("wrong-answer", f'We don\'t agree, the reward you provided is not the right one for the given path.'), "red", ["bold"])
    if ENV['feedback'] == "bigger_or_smaller":    
        if answer < right_answer:
            TAc.print(LANG.render_feedback("smaller-than-right", f'We don\'t agree, the reward you provided is smaller than the right one for the given path.'), "red", ["bold"])
            exit(0)
        TAc.print(LANG.render_feedback("bigger-than-right", f'We don\'t agree, the reward you provided is bigger than the right one for the given path.'), "red", ["bold"])
        exit(0)
    if ENV['feedback'] == "true_reward":
        TAc.print(LANG.render_feedback("right-reward", f'The right reward for the given path is {right_answer}.'), "yellow", ["bold"])
        exit(0)
exit(0)
