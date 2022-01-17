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
instances = { 'correct' : [] }
MIN_VAL = 10
MAX_VAL = 99
NUM_INSTANCES = 3
for n in range(2, 7):
    for _ in range(NUM_INSTANCES):
        seed = random.randint(100000,999999)
        instances['correct'].append({'triangle' : tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), 'n' : n, 'MIN_VAL' : MIN_VAL, 'MAX_VAL' : MAX_VAL, 'seed' : seed, 'measured_time' : None, 'answer_is_correct' : None})
        
# INSTANCES FOR GOAL = 2^n o n^2      
  
if ENV["goal"] == 'time_at_most_2_exp_n' or ENV["goal"] =='time_at_most_n_exp_2':
    goals.append('time_at_most_2_exp_n')
    instances['time_at_most_2_exp_n'] = []
    MIN_N = 8  # could still be 2^{\choose(n,2)}
    MAX_N = 15  # we intend to evaluate positively solutions as bad as O(2^n)
    if ENV["code_lang"] == "compiled":
        MAX_N = 18
    NUM_INSTANCES = 1
    for n in range(MIN_N, MAX_N):
        seed = random.randint(100000,999999)
        instances['time_at_most_2_exp_n'].append({'triangle' : tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), 'n' : n, 'MIN_VAL' : MIN_VAL, 'MAX_VAL' : MAX_VAL, 'seed' : seed, 'measured_time' : None, 'answer_is_correct' : None})

# INSTANCES FOR GOAL = n^2

if ENV["goal"] == 'time_at_most_n_exp_2':
    goals.append('time_at_most_n_exp_2')
    instances['time_at_most_n_exp_2'] = []
    MIN_N = 16  # could still be 2^n
    if ENV["code_lang"] == "compiled":
        MIN_N = 19  # could still be 2^n
    MAX_N = 50  # we intend to evaluate positively only the linear O(n^2) solutions
    if ENV["code_lang"] == "compiled":
        MAX_N = 100
    NUM_INSTANCES = 1
    scaling_factor = 1.1
    n = MIN_N
    while n < MAX_N:
        seed = random.randint(100000,999999)
        instances['time_at_most_n_exp_2'].append({'triangle' : tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), 'n' : n, 'MIN_VAL' : MIN_VAL, 'MAX_VAL' : MAX_VAL, 'seed' : seed, 'measured_time' : None, 'answer_is_correct' : None})
        n = math.ceil(n*scaling_factor)
        scaling_factor += 0.1
        if n > MAX_N:
           n = MAX_N
            
def right_length(triangle,answer):
    if len(triangle) == len(answer)+1:
        return True
    return False

def is_feasible_solution(path):                  
    for el in path:           
        if el != "R" and el != "L":
            return False
    return True    
           
MAX_TIME = 2

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def test(instance):
    triangle = instance['triangle']
    n = instance['n']
    TAc.print(LANG.render_feedback("triangle-size",'We have a triangle whose number of rows is:'), "white", ["bold"])
    TAc.print(n, "yellow", ["bold"])
    TAc.print(LANG.render_feedback("triangle-instance",'Triangle instance of reference:'), "white", ["bold"])
    tl.print_triangle(triangle)
    TAc.print(LANG.render_feedback("ask-path", f'\nGiven this triangle, can you provide a feasible solution?'),"white",["bold"])
    start = monotonic()
    answer = TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
    end = monotonic()
    instance['measured_time'] = end-start
    if right_length(triangle,answer) and is_feasible_solution(answer):
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
