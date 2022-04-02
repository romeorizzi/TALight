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

# START CODING YOUR SERVICE:

# INSTANCES FOR GOAL = correct
goals = ['correct']
instances = {}
# N = small triangle size    M = big triangle size
MIN_VAL = 0
MAX_VAL = 1
MIN_N = 2 
MAX_N = 2 
MIN_M = 5
MAX_M = 10
NUM_INSTANCES = 5
scaling_factor = 1.5

instances['correct'] = tl.instances_generator(NUM_INSTANCES, scaling_factor, MIN_VAL, MAX_VAL, MIN_N, MAX_N, MIN_M, MAX_M, MIN_VAL, MAX_VAL)
    
# INSTANCES FOR GOAL = 2^n o n^2      
  
if ENV["goal"] == 'time_at_most_2_exp_n' or ENV["goal"] =='time_at_most_n_exp_2':
    goals.append('time_at_most_2_exp_n')    
    NUM_INSTANCES = 12
    MIN_N = 2
    MAX_N = 4
    MIN_M = 7
    MAX_M = 12
    scaling_factor = 1.1
    if ENV["code_lang"] == "compiled":
        MAX_M = 18
        scaling_factor = 1.2
    instances['time_at_most_2_exp_n'] = tl.instances_generator(NUM_INSTANCES, scaling_factor, MIN_VAL, MAX_VAL, MIN_N, MAX_N, MIN_M, MAX_M, MIN_VAL, MAX_VAL)

# INSTANCES FOR GOAL = n^2

if ENV["goal"] == 'time_at_most_n_exp_2':
    goals.append('time_at_most_n_exp_2')
    instances['time_at_most_n_exp_2'] = []
    NUM_INSTANCES = 15
    MIN_SMALL_N = 2
    MAX_SMALL_N = 4
    MIN_BIG_N = 20
    MAX_BIG_N = 50
    scaling_factor = 1.2
    if ENV["code_lang"] == "compiled":
        MIN_BIG_N = 30
        MAX_BIG_N = 100
    instances['time_at_most_n_exp_2'] = tl.instances_generator(NUM_INSTANCES, scaling_factor, MIN_VAL, MAX_VAL, MIN_N, MAX_N, MIN_M, MAX_M, MIN_VAL, MAX_VAL)

MAX_TIME = 2

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def test(instance):
    small_triangle = instance['triangle']
    big_triangle = instance['big_triangle']
    small = tl.cast_to_array(small_triangle)
    big = tl.cast_to_array(big_triangle)
    l = len(small_triangle)
    L = len(big_triangle)
    TAc.print(LANG.render_feedback("small-triangle-size", f'# The small triangle has this number of rows:'), "white",["bold"])
    TAc.print(l, "yellow", ["bold"])
    TAc.print(LANG.render_feedback("big-triangle-size", f'# The big triangle has this number of rows:'), "white",["bold"])
    TAc.print(L, "yellow", ["bold"])
    TAc.print(LANG.render_feedback("small-triangle", f'# The small triangle of reference is:'), "white",["bold"])
    tl.print_triangle(small_triangle)
    TAc.print(LANG.render_feedback("big-triangle", f'# The big triangle of reference is:'), "white",["bold"])
    tl.print_triangle(big_triangle)
    TAc.print(LANG.render_feedback("fit-question", f'# How many times does the small triangle fit in the big triangle?'), "white",["bold"])
    start = monotonic()
    answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
    end = monotonic()
    instance['measured_time'] = end-start
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
    if answer == right_answer:
        instance['answer_is_correct'] = True
    else:
        instance['answer_is_correct'] = False
        
# MAIN: TEST ALL TESTCASES: 

out_of_time = 0
for goal in goals:
    for instance in instances[goal]:
        test(instance)
        if instance['measured_time'] > MAX_TIME:
            out_of_time += 1
            tl.print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG)
            exit(0)
            
tl.print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG)
exit(0)

