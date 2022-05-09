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
MIN_VAL = 10
MAX_VAL = 99
NUM_INSTANCES = 5
scaling_factor = 1.5
MIN_N = 3
MAX_N = 10
instances['correct'] = tl.instances_generator(NUM_INSTANCES, scaling_factor, MIN_VAL, MAX_VAL, MIN_N, MAX_N)

# INSTANCES FOR GOAL = 2^n o n^2      
  
if ENV["goal"] == 'time_at_most_2_exp_n' or ENV["goal"] =='time_at_most_n_exp_2':
    goals.append("time_at_most_2_exp_n")
    MIN_N = 8  # could still be 2^{\choose(n,2)}
    MAX_N = 15  # we intend to evaluate positively solutions as bad as O(2^n)
    if ENV["code_lang"] == "compiled":
        MAX_N = 18
    NUM_INSTANCES = 10
    sacling_factor = 1.2
    instances['time_at_most_2_exp_n'] = tl.instances_generator(NUM_INSTANCES, scaling_factor, MIN_VAL, MAX_VAL, MIN_N, MAX_N) 
    
# INSTANCES FOR GOAL = n^2

if ENV["goal"] == 'time_at_most_n_exp_2':
    goals.append("time_at_most_n_exp_2")
    MIN_N = 16  # could still be 2^n
    if ENV["code_lang"] == "compiled":
        MIN_N = 19  # could still be 2^n
    MAX_N = 50  # we intend to evaluate positively only the linear O(n^2) solutions
    if ENV["code_lang"] == "compiled":
        MAX_N = 100
    NUM_INSTANCES = 30
    scaling_factor = 1.1
    instances['time_at_most_n_exp_2'] = tl.instances_generator(NUM_INSTANCES, scaling_factor, MIN_VAL, MAX_VAL, MIN_N, MAX_N) 

MAX_TIME = 2

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def test(instance):
    triangle = instance['triangle']
    n = instance['n']
    path = tl.random_path(n,n)
    TAc.print(LANG.render_feedback("triangle-size",'# We have a triangle whose number of rows is:'), "white", ["bold"])
    TAc.print(n, "yellow", ["bold"])
    TAc.print(LANG.render_feedback("print-triangle", f'# The triangle of reference is:'), "white", ["bold"])
    tl.print_triangle(triangle)
    TAc.print(LANG.render_feedback("display-path",f'# We give you the following path.'),"white", ["bold"])
    TAc.print(path, "yellow", ["bold"])
    TAc.print(LANG.render_feedback("display-path",f'# Calculate the reward it gets descending from the top element following the directions contained in the path.'),"white", ["bold"])
    start = monotonic()
    answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
    end = monotonic()
    instance['measured_time'] = end-start
    if answer == tl.calculate_path(triangle,path):
        instance['answer_correct'] = True
    else:
        instance['answer_correct'] = False
    

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
