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
MAX_BIG_ROWS = 10
MAX_SMALL_ROWS = 2
NUM_OF_INSTANCES = 10
#EFFICIENT
if ENV["goal"] == "efficient":
    MAX_BIG_ROWS *= 5
    NUM_OF_INSTANCES *=10
    MAX_SMALL_ROWS *= 2
    if ENV["code_lang"] == "compiled":
        MAX_BIG_ROWS *= 2
    big_scaling_factor = 1.4
    small_scaling_factor = 1.1

#NOT EFFICIENT
else:
    if ENV["code_lang"] == "compiled":
        MAX_BIG_ROWS *= 2
    big_scaling_factor = 1.3
    small_scaling_factor = 1.1
big_n = 5
small_n = 2
for _ in range(NUM_OF_INSTANCES):
    seed_big = random.randint(100000,999999)
    seed_small = random.randint(100000,999999)
    instances.append([tl.random_triangle(big_n, 0, 1, seed_big, TAc, LANG),tl.random_triangle(small_n, 0, 1, seed_small, TAc, LANG),seed_big,big_n,seed_small,small_n])
    big_n = math.ceil(big_n*big_scaling_factor)
    small_n = math.floor(small_n*small_scaling_factor)
    small_scaling_factor += 0.4
    if big_n > MAX_BIG_ROWS:
        big_n = MAX_BIG_ROWS
    if small_n > MAX_SMALL_ROWS:
        small_n = MAX_SMALL_ROWS
            
#CHECK TIME ELAPSED         
for triangles in instances:
    time = 0
    big_triangle = triangles[0]
    small_triangle = triangles[1]
    big = tl.cast_to_array(big_triangle)
    small = tl.cast_to_array(small_triangle)
    L = len(big_triangle)
    l = len(small_triangle)
    TAc.print(LANG.render_feedback("print-infos", f'We have to calculate the number of occurencies of a small triangle in a big triangle. The sizes of the two are respectively:'), "red")
    print([l,L])
    TAc.print(LANG.render_feedback("rough-triangle",f'Each triangle can be described as a list of lists, where each of these lists represents a line of the triangle. The corrseponding lists are:'),"white")
    print([small,big])
    TAc.print(LANG.render_feedback("question",f'How many times the small triangle fits inside the big triangle?'),"white")
    start = monotonic() 
    answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
    end = monotonic()
    time = end-start
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
                
    if answer != right_answer:
        TAc.NO()
        TAc.print(LANG.render_feedback("no-wrong-sol", f'{answer} is the wrong solution. The correct number of occurencies for these triangles (big triangle seed:{triangles[2]}, big triangle rows:{triangles[3]}, small triangle seed:{triangles[4]}, small triangle rows {triangles[5] }) is {right_answer}.'), "red")
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
