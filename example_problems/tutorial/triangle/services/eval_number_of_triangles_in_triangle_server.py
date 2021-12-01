#!/usr/bin/env python3
from sys import stderr, exit
import random
import math

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('big_n',int),
    ('small_n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('displayable',bool),
    ('how_to_input_the_big_triangle',str),
    ('how_to_input_the_small_triangle',str),
    ('silent',bool),
]


ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
'''    
# START CODING YOUR SERVICE:

# CHECK SIZES

if ENV["big_n"] < ENV["small_n"]:
    TAc.print(LANG.render_feedback("wrong-triangles-sizes", f'Error: the size of the bigger triangle ({ENV["big_n"]}) is smaller than the size of the smaller triangle ({ENV["small_n"]}).'), "red", ["bold"])
    exit(0)

# BIG TRIANGLE GENERATION

if ENV['how_to_input_the_big_triangle'] == "my_own_triangle":
    big_triangle = []
    TAc.print(LANG.render_feedback("insert-triangle", f'Please, insert your triangle, line by line. For every i in [1,{ENV["big_n"]}], line i comprises i integers separated by spaces.'), "yellow", ["bold"])
    for i in range(1,ENV["big_n"]+1):
        TAc.print(LANG.render_feedback("insert-line", f'Insert line i={i}, that is, {i} integers separated by spaces:'), "yellow")
        line = TALinput(int, i, token_recognizer=lambda val,TAc,LANG: tl.check_val_range(val,ENV['MIN_VAL'],ENV['MAX_VAL'],TAc,LANG), TAc=TAc, LANG=LANG)
        big_triangle.append(line)
    TAc.OK()
    TAc.print(LANG.render_feedback("triangle-insertion-completed", f'Insertion complete. Your triangle has been successfully inserted.'), "green")
elif ENV['how_to_input_the_big_triangle'] == "random":
    bign = 0
    if ENV['displayable']:
        bign =random.randint(1,30)
    else:
        bign =random.randint(1,100)
    seed = random.randint(100000,999999)
    big_triangle = tl.random_triangle(bign, ENV['MIN_VAL'], ENV['MAX_VAL'], seed, TAc, LANG)
else:
    big_triangle = tl.random_triangle(ENV["big_n"],ENV['MIN_VAL'],ENV['MAX_VAL'],int(ENV['how_to_input_the_big_triangle']),TAc,LANG)
print([bign,seed])        
# SMALL TRIANGLE GENERATION

if ENV['how_to_input_the_small_triangle'] == "my_own_triangle":
    small_triangle = []
    TAc.print(LANG.render_feedback("insert-triangle", f'Please, insert your triangle, line by line. For every i in [1,{ENV["small_n"]}], line i comprises i integers separated by spaces.'), "yellow", ["bold"])
    for i in range(1,ENV["small_n"]+1):
        TAc.print(LANG.render_feedback("insert-line", f'Insert line i={i}, that is, {i} integers separated by spaces:'), "yellow")
        line = TALinput(int, i, token_recognizer=lambda val,TAc,LANG: tl.check_val_range(val,ENV['MIN_VAL'],ENV['MAX_VAL'],TAc,LANG), TAc=TAc, LANG=LANG)
        small_triangle.append(line)
    TAc.OK()
    TAc.print(LANG.render_feedback("triangle-insertion-completed", f'Insertion complete. Your triangle has been successfully inserted.'), "green")
elif ENV['how_to_input_the_small_triangle'] == "random":
    smalln = 0
    if ENV['displayable']:
        wrong_size = True
        while wrong_size:
            smalln =random.randint(1,5)
            if bign >= smalln:
                wrong_size=False
    else:
        wrong_size = True
        while wrong_size:
            smalln =random.randint(1,100)
            if bign >= smalln:
                wrong_size=False
    seed = random.randint(100000,999999)
    small_triangle = tl.random_triangle(smalln, ENV['MIN_VAL'], ENV['MAX_VAL'], seed, TAc, LANG)
else:
    small_triangle = tl.random_triangle(ENV["small_n"],ENV['MIN_VAL'],ENV['MAX_VAL'],int(ENV['how_to_input_the_small_triangle']),TAc,LANG)
print([smalln,seed])
'''

big_triangle = [[1],[2,3],[1,1,1],[5,6,7,8],[1,3,2,5,6],[4,7,8,9,1,2],[1,5,2,4,3,1,1],[0,4,1,1,3,4,4,4]]
small_triangle = [[2],[1,1]]
big = tl.cast_to_array(big_triangle)
small = tl.cast_to_array(small_triangle)
L = len(big_triangle)
l = len(small_triangle)

right_answer = 0

livello = 1
levels = []
indexes = []
for i in range(int(((L-l+1)*(L-l+2))/2)):   
    if i >= livello*(livello+1)/2:
        livello +=1
    if tl.fits(i,livello,big,small,int(math.sqrt(2*len(small)-1)))[0]:
        right_answer +=1
        levels.append(livello)
        indexes.append(tl.fits(i,livello,big,small,int(math.sqrt(2*len(small)-1)))[1])
print(indexes)
print(levels)     
if ENV['displayable']:
    TAc.print(LANG.render_feedback("displayable-big",f'The big triangle is displayed here:\n'), "green")
    tl.print_triangle(big_triangle)
    TAc.print(LANG.render_feedback("displayable-small",f'\nThe small triangle is displayed here:\n'), "green")
    tl.print_triangle(small_triangle)
    
TAc.print(LANG.render_feedback("fit-question", f'\nGiven these triangles, how many times does the smaller one fit inside the bigger one?\nYour answer shall be a positive integer'), "green")
answer = TALinput(int, token_recognizer=lambda val,TAc,LANG: True, TAc=TAc, LANG=LANG)[0]
if answer == right_answer:
    if not ENV['silent']:
        TAc.OK()
        TAc.print(LANG.render_feedback("right-answer", f'We agree, the answer is {right_answer}.\n'), "green", ["bold"])
        if right_answer != 0:
            tl.print_triangle_occurencies(big_triangle,small_triangle,indexes,levels)     
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-answer", f'We don\'t agree, the answer is {right_answer}.'), "red", ["bold"])
exit(0)

