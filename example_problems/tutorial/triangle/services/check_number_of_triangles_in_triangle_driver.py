#!/usr/bin/env python3
from sys import stderr, exit
import random
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('big_n',int),
    ('small_n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('display_big',bool),
    ('display_small',bool),
    ('display_sol',bool),
    ('how_to_input_the_big_triangle',str),
    ('how_to_input_the_small_triangle',str),
    ('silent',bool),
]


ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

#CHECK MIN_VAL <= MAX_VAL
if ENV['MIN_VAL'] > ENV['MAX_VAL']:
    TAc.NO()
    TAc.print(LANG.render_feedback("range-is-empty", f"Error: I can not choose the integers for the triangle from the range [{MIN_VAL},{MAX_VAL}] since this range is empty.", {"MIN_VAL":MIN_VAL, "MAX_VAL":MAX_VAL}), "red", ["bold"])
    exit(0)
    
# CHECK SIZES
if ENV["big_n"] < ENV["small_n"]:
    TAc.print(LANG.render_feedback("wrong-triangles-sizes", f'Error: the size of the bigger triangle ({ENV["big_n"]}) is smaller than the size of the smaller triangle ({ENV["small_n"]}).'), "red", ["bold"])
    exit(0)
    
# BIG TRIANGLE GENERATION
if ENV["how_to_input_the_big_triangle"] == "my_own_triangle":
    big_triangle = []
    TAc.print(LANG.render_feedback("insert-triangle", f'Please, insert your triangle, line by line. For every i in [1,{ENV["big_n"]}], line i comprises i integers separated by spaces.'), "yellow", ["bold"])
    for i in range(1,ENV["big_n"]+1):
        TAc.print(LANG.render_feedback("insert-line", f'Insert line i={i}, that is, {i} integers separated by spaces:'), "yellow")
        line = TALinput(int, i, token_recognizer=lambda val,TAc,LANG: tl.check_val_range(val,ENV["MIN_VAL"],ENV["MAX_VAL"],TAc,LANG), TAc=TAc, LANG=LANG)
        big_triangle.append(line)
    TAc.OK()
    TAc.print(LANG.render_feedback("triangle-insertion-completed", f'Insertion complete. Your triangle has been successfully inserted.'), "green")
elif ENV["how_to_input_the_big_triangle"] == "random":
    seed = random.randint(100000,999999)
    big_triangle = tl.random_triangle(ENV["big_n"], ENV["MIN_VAL"], ENV["MAX_VAL"], seed)
else:
    big_triangle = tl.random_triangle(ENV["big_n"],ENV["MIN_VAL"],ENV["MAX_VAL"],int(ENV["how_to_input_the_big_triangle"]))
       
# SMALL TRIANGLE GENERATION
if ENV["how_to_input_the_small_triangle"] == "my_own_triangle":
    small_triangle = []
    TAc.print(LANG.render_feedback("insert-triangle", f'Please, insert your triangle, line by line. For every i in [1,{ENV["small_n"]}], line i comprises i integers separated by spaces.'), "yellow", ["bold"])
    for i in range(1,ENV["small_n"]+1):
        TAc.print(LANG.render_feedback("insert-line", f'Insert line i={i}, that is, {i} integers separated by spaces:'), "yellow")
        line = TALinput(int, i, token_recognizer=lambda val,TAc,LANG: tl.check_val_range(val,ENV["MIN_VAL"],ENV["MAX_VAL"],TAc,LANG), TAc=TAc, LANG=LANG)
        small_triangle.append(line)
    TAc.OK()
    TAc.print(LANG.render_feedback("triangle-insertion-completed", f'Insertion complete. Your triangle has been successfully inserted.'), "green")
elif ENV["how_to_input_the_small_triangle"] == "random":
    seed = random.randint(100000,999999)
    small_triangle = tl.random_triangle(ENV["small_n"], ENV["MIN_VAL"], ENV["MAX_VAL"], seed)
else:
    small_triangle = tl.random_triangle(ENV["small_n"],ENV["MIN_VAL"],ENV["MAX_VAL"],int(ENV["how_to_input_the_small_triangle"]))

big = tl.cast_to_array(big_triangle)
small = tl.cast_to_array(small_triangle)
L = len(big_triangle)
l = len(small_triangle)

right_answer = 0

livello = 1
indexes = []
for i in range(int(((L-l+1)*(L-l+2))/2)):   
    if i >= livello*(livello+1)/2:
        livello +=1
    if big[i] == small[0]:
        if tl.fits(i,livello,big,small,l)[0]:
            indexes.append(tl.fits(i,livello,big,small,l)[1])
            right_answer += 1
            
if ENV["display_big"]:
    TAc.print(LANG.render_feedback("display-big",f'The big triangle is displayed here:\n'), "green")
    tl.print_triangle(big_triangle)
if ENV["display_small"]:    
    TAc.print(LANG.render_feedback("display-small",f'\nThe small triangle is displayed here:\n'), "green")
    tl.print_triangle(small_triangle)
    
TAc.print(LANG.render_feedback("fit-question", f'\nGiven these triangles, how many times does the smaller one fit inside the bigger one?\nYour answer shall be a positive integer'), "green")
answer = TALinput(int, token_recognizer=lambda val,TAc,LANG: True, TAc=TAc, LANG=LANG)[0]
if answer == right_answer:
    if not ENV["silent"]:
        TAc.OK()
        if ENV["display_sol"]:
            TAc.print(LANG.render_feedback("right-answer-display", f'We agree, the answer is {right_answer}, as you can see below.\n'), "green", ["bold"])
            tl.print_triangle_occurencies(big_triangle,sum(indexes,[]))
        else:
            TAc.print(LANG.render_feedback("right-answer", f'We agree, the answer is {right_answer}.\n'), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-answer", f'We don\'t agree, the answer is {right_answer}.'), "red", ["bold"])  
exit(0)

