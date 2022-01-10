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

instances = { 'correct' : [] }
MIN_VAL = 10
MAX_VAL = 99
NUM_INSTANCES = 5
for n in range(2, 7):
    seed = random.randint(100000,999999)
    instances['correct'].append([tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), n, MIN_VAL, MAX_VAL, seed])

# INSTANCES FOR GOAL = 2^n o n^2      
  
if ENV["goal"] == 'time_at_most_2_exp_n' or ENV["goal"] =='time_at_most_n_exp_2':
    instances['time_at_most_2_exp_n'] = []
    MIN_N = 8  # could still be 2^{\choose(n,2)}
    MAX_N = 15  # we intend to evaluate positively solutions as bad as O(2^n)
    if ENV["code_lang"] == "compiled":
        MAX_N = 18
    NUM_INSTANCES = 7
    for n in range(MIN_N, MAX_N):
        seed = random.randint(100000,999999)
        instances['time_at_most_2_exp_n'].append([tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), n, MIN_VAL, MAX_VAL, seed])

# INSTANCES FOR GOAL = n^2

if ENV["goal"] == 'time_at_most_n_exp_2':
    instances['time_at_most_n_exp_2'] = []
    MIN_N = 16  # could still be 2^n
    if ENV["code_lang"] == "compiled":
        MIN_N = 19  # could still be 2^n
    MAX_N = 50  # we intend to evaluate positively only the linear O(n^2) solutions
    if ENV["code_lang"] == "compiled":
        MAX_N = 100
    NUM_INSTANCES = 5
    scaling_factor = 1.1
    n = MIN_N
    while n < MAX_N:
        seed = random.randint(100000,999999)
        instances['time_at_most_n_exp_2'].append([tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), n, MIN_VAL, MAX_VAL, seed])
        n = math.ceil(n*scaling_factor)
        scaling_factor += 0.1
        if n > MAX_N:
           n = MAX_N
           
MAX_TIME = 2

#CHECK TIME ELAPSED FOR correct 
        
if ENV["goal"] == 'correct':
    visited_instances_correct = []
    for instance in instances['correct']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size", f'We give you a triangle with this number of rows:'), "white")
        print(n)
        TAc.print(LANG.render_feedback("print-triangle", f'The triangle of reference is:'), "white")
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("rought-triangle", f'The triangle can be seen as a list of lists. In this case we have:'), "white")
        print(triangle)
        TAc.print(LANG.render_feedback("best-path-question", f'Which is the best collectable reward in this triangle?'), "white")
        start = monotonic() 
        answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
            exit(0)
        elif answer != tl.best_path_cost(triangle):
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
    exit(0)

#CHECK TIME ELAPSED FOR time_at_most_2_exp_n
       
elif ENV["goal"] == 'time_at_most_2_exp_n':
    visited_instances_correct = []
    for instance in instances['correct']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size", f'We give you a triangle with this number of rows:'), "white")
        print(n)
        TAc.print(LANG.render_feedback("print-triangle", f'The triangle of reference is:'), "white")
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("rought-triangle", f'The triangle can be seen as a list of lists. In this case we have:'), "white")
        print(triangle)
        TAc.print(LANG.render_feedback("best-path-question", f'Which is the best collectable reward in this triangle?'), "white")
        start = monotonic() 
        answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
            exit(0)
        elif answer != tl.best_path_cost(triangle):
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    
    visited_instances_2_exp_n = []
    for instance in instances['time_at_most_2_exp_n']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size", f'We give you a triangle with this number of rows:'), "white")
        print(n)
        TAc.print(LANG.render_feedback("print-triangle", f'The triangle of reference is:'), "white")
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("rought-triangle", f'The triangle can be seen as a list of lists. In this case we have:'), "white")
        print(triangle)
        TAc.print(LANG.render_feedback("best-path-question", f'Which is the best collectable reward in this triangle?'), "white")
        start = monotonic() 
        answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_2_exp_n.append([instance,time,"out_of_time"])
            tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
            tl.print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n,TAc,LANG)
            exit(0)
        elif answer != tl.best_path_cost(triangle):
            visited_instances_2_exp_n.append([instance,time,"wrong"])
        else:
            visited_instances_2_exp_n.append([instance,time,"right"])
    tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
    tl.print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n,TAc,LANG)    
    exit(0)
    
#CHECK TIME ELAPSED FOR time_at_most_n_exp_2

else:
    visited_instances_correct = []
    for instance in instances['correct']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size", f'We give you a triangle with this number of rows:'), "white")
        print(n)
        TAc.print(LANG.render_feedback("print-triangle", f'The triangle of reference is:'), "white")
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("rought-triangle", f'The triangle can be seen as a list of lists. In this case we have:'), "white")
        print(triangle)
        TAc.print(LANG.render_feedback("best-path-question", f'Which is the best collectable reward in this triangle?'), "white")
        start = monotonic() 
        answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
            exit(0)
        elif answer != tl.best_path_cost(triangle):
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    
    visited_instances_2_exp_n = []
    for instance in instances['time_at_most_2_exp_n']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size", f'We give you a triangle with this number of rows:'), "white")
        print(n)
        TAc.print(LANG.render_feedback("print-triangle", f'The triangle of reference is:'), "white")
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("rought-triangle", f'The triangle can be seen as a list of lists. In this case we have:'), "white")
        print(triangle)
        TAc.print(LANG.render_feedback("best-path-question", f'Which is the best collectable reward in this triangle?'), "white")
        start = monotonic() 
        answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_2_exp_n.append([instance,time,"out_of_time"])
            tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
            tl.print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n,TAc,LANG)
            exit(0)
        elif answer != tl.best_path_cost(triangle):
            visited_instances_2_exp_n.append([instance,time,"wrong"])
        else:
            visited_instances_2_exp_n.append([instance,time,"right"])
    
    visited_instances_n_exp_2 = []
    for instance in instances['time_at_most_n_exp_2']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size", f'We give you a triangle with this number of rows:'), "white")
        print(n)
        TAc.print(LANG.render_feedback("print-triangle", f'The triangle of reference is:'), "white")
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("rought-triangle", f'The triangle can be seen as a list of lists. In this case we have:'), "white")
        print(triangle)
        TAc.print(LANG.render_feedback("best-path-question", f'Which is the best collectable reward in this triangle?'), "white")
        start = monotonic() 
        answer = int(TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0])
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_n_exp_2.append([instance,time,"out_of_time"])
            tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
            tl.print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n,TAc,LANG)
            tl.print_goal_summary('time_at_most_n_exp_2',visited_instances_n_exp_2,TAc,LANG) 
            exit(0)
        elif answer != tl.best_path_cost(triangle):
            visited_instances_n_exp_2.append([instance,time,"wrong"])
        else:
            visited_instances_n_exp_2.append([instance,time,"right"])
    
    tl.print_goal_summary('correct',visited_instances_correct,TAc,LANG)
    tl.print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n,TAc,LANG) 
    tl.print_goal_summary('time_at_most_n_exp_2',visited_instances_n_exp_2,TAc,LANG) 
    exit(0)
