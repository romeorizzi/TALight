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
NUM_INSTANCES = 3
for n in range(2, 7):
    for _ in range(NUM_INSTANCES):
        seed = random.randint(100000,999999)
        instances['correct'].append([tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), n, MIN_VAL, MAX_VAL, seed])

# INSTANCES FOR GOAL = 2^n o n^2      
  
if ENV["goal"] == 'time_at_most_2_exp_n' or ENV["goal"] =='time_at_most_n_exp_2':
    instances['time_at_most_2_exp_n'] = []
    MIN_N = 8  # could still be 2^{\choose(n,2)}
    MAX_N = 15  # we intend to evaluate positively solutions as bad as O(2^n)
    if ENV["code_lang"] == "compiled":
        MAX_N = 18
    NUM_INSTANCES = 1
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
    NUM_INSTANCES = 1
    scaling_factor = 1.1
    n = MIN_N
    while n < MAX_N:
        seed = random.randint(100000,999999)
        instances['time_at_most_n_exp_2'].append([tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), n, MIN_VAL, MAX_VAL, seed])
        n = math.ceil(n*scaling_factor)
        scaling_factor += 0.1
        if n > MAX_N:
           n = MAX_N

def print_goal_summary(goal,visited_instances):
    TAc.print(LANG.render_feedback("summary", f'\n# SUMMARY OF THE RESULTS FOR GOAL "{goal}":\n'), "white", ["bold"])
    right = 0
    wrong = 0
    out_of_time = 0
    for ans in visited_instances:
        if ans[2] == "right":
            time = ans[1]
            TAc.print(LANG.render_feedback("right-ans", f'# Correct! Took time {time} on your machine.\n'), "green")
            right += 1
        elif ans[2] == "wrong":
            time = ans[1]
            n = ans[0][1] 
            MIN_VAL = ans[0][2] 
            MAX_VAL = ans[0][3] 
            seed = ans[0][4] 
            TAc.print(LANG.render_feedback("wrong-ans", f'# NO! You gave the wrong solution for the instance with these parameters:\nn = {n}, MIN_VAL = {MIN_VAL}, MAX_VAL = {MAX_VAL}, seed = {seed}.\n'), "yellow")
            wrong += 1  
        else:
            time = ans[1]
            n = ans[0][1] 
            MIN_VAL = ans[0][2] 
            MAX_VAL = ans[0][3] 
            seed = ans[0][4]
            TAc.print(LANG.render_feedback("out-of-time-ans", f'# The evaluation has been stopped since your solution took too much time to perform on the instance with these parameters:\nn = {n}, MIN_VAL = {MIN_VAL}, MAX_VAL = {MAX_VAL}, seed = {seed}.\n'), "white")
            out_of_time += 1
    if out_of_time > 0 and wrong == 0 and right >0:
        TAc.print(LANG.render_feedback("right-not-in-time", f'# OK! Your solution works well on some instances, but it didn\'t achieve the goal "{goal}".\n'), "yellow")
    elif out_of_time > 0 and wrong == 0 and right == 0:
        TAc.print(LANG.render_feedback("not-in-time", f'# Your solution didn\'t achieve the goal "{goal}".\n'), "yellow")
    elif right == len(visited_instances):
        TAc.print(LANG.render_feedback("right-in-time", f'# OK! Your solution achieved the goal "{goal}"!.\n'), "green")
    elif wrong > 0:
        TAc.print(LANG.render_feedback("right-in-time", f'# NO! Your solution doesn\'t work well on some instances!.\n'), "red")     
            
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

#CHECK TIME ELAPSED FOR correct 
        
if ENV["goal"] == 'correct':
    visited_instances_correct = []
    for instance in instances['correct']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size",'We have a triangle whose number of rows is:'), "white", ["bold"])
        TAc.print(n, "yellow", ["bold"])
        TAc.print(LANG.render_feedback("triangle-instance",'Triangle instance of reference:'), "white", ["bold"])
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("ask-path", f'\nGiven this triangle, can you provide a feasible solution?'),"white",["bold"])
        start = monotonic()
        answer = TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            exit(0)
        elif not right_length(triangle,answer) or not is_feasible_solution(answer):
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    print_goal_summary('correct',visited_instances_correct)
    exit(0)

#CHECK TIME ELAPSED FOR time_at_most_2_exp_n
       
elif ENV["goal"] == 'time_at_most_2_exp_n':
    visited_instances_correct = []
    for instance in instances['correct']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size",'We have a triangle whose number of rows is:'), "white", ["bold"])
        TAc.print(n, "yellow", ["bold"])
        TAc.print(LANG.render_feedback("triangle-instance",'Triangle instance of reference:'), "white", ["bold"])
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("ask-path", f'\nGiven this triangle, can you provide a feasible solution?'),"white",["bold"])
        start = monotonic() 
        answer = TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            exit(0)
        elif not right_length(triangle,answer) or not is_feasible_solution(answer):
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    
    visited_instances_2_exp_n = []
    for instance in instances['time_at_most_2_exp_n']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size",'We have a triangle whose number of rows is:'), "white", ["bold"])
        TAc.print(n, "yellow", ["bold"])
        TAc.print(LANG.render_feedback("triangle-instance",'Triangle instance of reference:'), "white", ["bold"])
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("ask-path", f'\nGiven this triangle, can you provide a feasible solution?'),"white",["bold"])
        start = monotonic()
        answer = TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_2_exp_n.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n)
            exit(0)
        elif not right_length(triangle,answer) or not is_feasible_solution(answer):
            visited_instances_2_exp_n.append([instance,time,"wrong"])
        else:
            visited_instances_2_exp_n.append([instance,time,"right"])
    print_goal_summary('correct',visited_instances_correct)
    print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n)    
    exit(0)
    
#CHECK TIME ELAPSED FOR time_at_most_n_exp_2

else:
    visited_instances_correct = []
    for instance in instances['correct']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size",'We have a triangle whose number of rows is:'), "white", ["bold"])
        TAc.print(n, "yellow", ["bold"])
        TAc.print(LANG.render_feedback("triangle-instance",'Triangle instance of reference:'), "white", ["bold"])
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("ask-path", f'\nGiven this triangle, can you provide a feasible solution?'),"white",["bold"])
        start = monotonic() 
        answer = TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            exit(0)
        elif not right_length(triangle,answer) or not is_feasible_solution(answer):
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    
    visited_instances_2_exp_n = []
    for instance in instances['time_at_most_2_exp_n']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size",'We have a triangle whose number of rows is:'), "white", ["bold"])
        TAc.print(n, "yellow", ["bold"])
        TAc.print(LANG.render_feedback("triangle-instance",'Triangle instance of reference:'), "white", ["bold"])
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("ask-path", f'\nGiven this triangle, can you provide a feasible solution?'),"white",["bold"])
        start = monotonic() 
        answer = TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_2_exp_n.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n)
            exit(0)
        elif not right_length(triangle,answer) or not is_feasible_solution(answer):
            visited_instances_2_exp_n.append([instance,time,"wrong"])
        else:
            visited_instances_2_exp_n.append([instance,time,"right"])
    
    visited_instances_n_exp_2 = []
    for instance in instances['time_at_most_n_exp_2']:
        triangle = instance[0]
        n = instance[1]
        TAc.print(LANG.render_feedback("triangle-size",'We have a triangle whose number of rows is:'), "white", ["bold"])
        TAc.print(n, "yellow", ["bold"])
        TAc.print(LANG.render_feedback("triangle-instance",'Triangle instance of reference:'), "white", ["bold"])
        tl.print_triangle(triangle)
        TAc.print(LANG.render_feedback("ask-path", f'\nGiven this triangle, can you provide a feasible solution?'),"white",["bold"])
        start = monotonic() 
        answer = TALinput(str, line_recognizer=lambda path,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
        end = monotonic()
        time = end-start
        if time > MAX_TIME:
            visited_instances_n_exp_2.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n)
            print_goal_summary('time_at_most_n_exp_2',visited_instances_n_exp_2) 
            exit(0)
        elif not right_length(triangle,answer) or not is_feasible_solution(answer):
            visited_instances_n_exp_2.append([instance,time,"wrong"])
        else:
            visited_instances_n_exp_2.append([instance,time,"right"])
    
    print_goal_summary('correct',visited_instances_correct)
    print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n) 
    print_goal_summary('time_at_most_n_exp_2',visited_instances_n_exp_2) 
    exit(0)
