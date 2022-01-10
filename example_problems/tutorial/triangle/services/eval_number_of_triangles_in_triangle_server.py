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
MIN_VAL = 0
MAX_VAL = 1
MIN_SMALL_N = 2
MAX_SMALL_N = 2
MIN_BIG_N = 5
MAX_BIG_N = 10
NUM_INSTANCES = 5

for i in range (NUM_INSTANCES):
    small_seed = random.randint(100000,999999)
    big_seed = random.randint(100000,999999)
    couple = [tl.random_triangle(MIN_SMALL_N, MIN_VAL, MAX_VAL, small_seed, TAc, LANG),tl.random_triangle(MIN_BIG_N+i, MIN_VAL, MAX_VAL, big_seed, TAc, LANG)]
    instances['correct'].append([couple, [MIN_SMALL_N,MIN_BIG_N+i], MIN_VAL, MAX_VAL, [small_seed,big_seed]])
    
# INSTANCES FOR GOAL = 2^n o n^2      

# SMALL INSTANCES
  
if ENV["goal"] == 'time_at_most_2_exp_n' or ENV["goal"] =='time_at_most_n_exp_2':
    instances['time_at_most_2_exp_n'] = []
    NUM_INSTANCES = 6
    MIN_SMALL_N = 2
    MAX_SMALL_N = 4
    MIN_BIG_N = 7
    MAX_BIG_N = 12
    scaling_factor = 1.1
    if ENV["code_lang"] == "compiled":
        MAX_BIG_N = 18
        scaling_factor = 1.2
    for n in range(NUM_INSTANCES):
        small_seed = random.randint(100000,999999)
        big_seed = random.randint(100000,999999)
        couple = [tl.random_triangle(MIN_SMALL_N, MIN_VAL, MAX_VAL, small_seed, TAc, LANG),tl.random_triangle(MIN_BIG_N, MIN_VAL, MAX_VAL, big_seed, TAc, LANG)]
        instances['time_at_most_2_exp_n'].append([couple, [MIN_SMALL_N,MIN_BIG_N], MIN_VAL, MAX_VAL, [small_seed,big_seed]])
        MIN_SMALL_N = math.ceil(scaling_factor*MIN_SMALL_N)
        if MIN_SMALL_N > MAX_SMALL_N:
            MIN_SMALL_N = MAX_SMALL_N
        MIN_BIG_N = math.ceil(scaling_factor*MIN_BIG_N)
        if MIN_BIG_N > MAX_BIG_N:
            MIN_BIG_N = MAX_BIG_N

# INSTANCES FOR GOAL = n^2

# SMALL INSTANCES

if ENV["goal"] == 'time_at_most_n_exp_2':
    instances['time_at_most_n_exp_2'] = []
    NUM_INSTANCES = 15
    MIN_SMALL_N = 2
    MAX_SMALL_N = 4
    MIN_BIG_N = 20
    MAX_BIG_N = 50
    scaling_factor = 1.1
    if ENV["code_lang"] == "compiled":
        MIN_BIG_N = 30
        MAX_BIG_N = 100
    for _ in range(NUM_INSTANCES):
        small_seed = random.randint(100000,999999)
        big_seed = random.randint(100000,999999)
        couple = [tl.random_triangle(MIN_SMALL_N, MIN_VAL, MAX_VAL, small_seed, TAc, LANG),tl.random_triangle(MIN_BIG_N, MIN_VAL, MAX_VAL, big_seed, TAc, LANG)]
        instances['time_at_most_n_exp_2'].append([couple, [MIN_SMALL_N,MIN_BIG_N], MIN_VAL, MAX_VAL, [small_seed,big_seed]])
        MIN_SMALL_N = math.ceil(scaling_factor*MIN_SMALL_N)
        if MIN_SMALL_N > MAX_SMALL_N:
            MIN_SMALL_N = MAX_SMALL_N
        MIN_BIG_N = math.ceil(scaling_factor*MIN_BIG_N)
        if MIN_BIG_N > MAX_BIG_N:
            MIN_BIG_N = MAX_BIG_N


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
            small_n = ans[0][1][0] 
            big_n = ans[0][1][1]
            MIN_VAL = ans[0][2] 
            MAX_VAL = ans[0][3] 
            small_seed = ans[0][4][0] 
            big_seed = ans[0][4][1]
            TAc.print(LANG.render_feedback("wrong-ans", f'# NO! You gave the wrong solution for the instances with these parameters:\nSMALL TRIANGLE: n = {small_n}, MIN_VAL = {MIN_VAL}, MAX_VAL = {MAX_VAL}, seed = {small_seed}.\nBIG TRIANGLE: n = {big_n}, MIN_VAL = {MIN_VAL}, MAX_VAL = {MAX_VAL}, seed = {big_seed}.\n'), "yellow")
            wrong += 1  
        else:
            time = ans[1]
            small_n = ans[0][1][0] 
            big_n = ans[0][1][1]
            MIN_VAL = ans[0][2] 
            MAX_VAL = ans[0][3] 
            small_seed = ans[0][4][0] 
            big_seed = ans[0][4][1]
            TAc.print(LANG.render_feedback("out-of-time-ans", f'# The evaluation has been stopped since your solution took too much time to perform on the instances with these parameters:\nSMALL TRIANGLE: n = {small_n}, MIN_VAL = {MIN_VAL}, MAX_VAL = {MAX_VAL}, seed = {small_seed}.\nBIG TRIANGLE: n = {big_n}, MIN_VAL = {MIN_VAL}, MAX_VAL = {MAX_VAL}, seed = {big_seed}.\n'), "white")
            out_of_time += 1
    if out_of_time > 0 and wrong == 0 and right >0:
        TAc.print(LANG.render_feedback("right-not-in-time", f'# OK! Your solution works well on some instances, but it didn\'t achieve the goal "{goal}".\n'), "yellow")
    elif out_of_time > 0 and wrong == 0 and right == 0:
        TAc.print(LANG.render_feedback("not-in-time", f'# Your solution didn\'t achieve the goal "{goal}".\n'), "yellow")
    elif right == len(visited_instances):
        TAc.print(LANG.render_feedback("right-in-time", f'# OK! Your solution achieved the goal "{goal}"!.\n'), "green")
    elif wrong > 0:
        TAc.print(LANG.render_feedback("right-in-time", f'# NO! Your solution doesn\'t work well on some instances!.\n'), "red")  

MAX_TIME = 2

#CHECK TIME ELAPSED FOR correct 
        
if ENV["goal"] == 'correct':
    visited_instances_correct = []
    for instance in instances['correct']:
        small_triangle = instance[0][0]
        big_triangle = instance[0][1]
        small = tl.cast_to_array(small_triangle)
        big = tl.cast_to_array(big_triangle)
        l = len(small_triangle)
        L = len(big_triangle)
        TAc.print(LANG.render_feedback("small-triangle-size", f'The small triangle has this number of rows:'), "white")
        print(l)
        TAc.print(LANG.render_feedback("big-triangle-size", f'The big triangle has this number of rows:'), "white")
        print(L)
        TAc.print(LANG.render_feedback("rough-small-triangle", f'The small triangle can be seen as a list of lists. In this case we have:'), "white")
        print(small)
        TAc.print(LANG.render_feedback("rough-big-triangle", f'The big triangle can be seen as a list of lists. In this case we have:'), "white")
        print(big)
        TAc.print(LANG.render_feedback("fit-question", f'How many times does the small triangle fit in the big triangle?'), "white")
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
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            exit(0)
        elif answer != right_answer:
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    print_goal_summary('correct',visited_instances_correct)
    exit(0)

#CHECK TIME ELAPSED FOR time_at_most_2_exp_n
       
elif ENV["goal"] == 'time_at_most_2_exp_n':
    visited_instances_correct = []
    for instance in instances['correct']:
        small_triangle = instance[0][0]
        big_triangle = instance[0][1]
        small = tl.cast_to_array(small_triangle)
        big = tl.cast_to_array(big_triangle)
        l = len(small_triangle)
        L = len(big_triangle)
        TAc.print(LANG.render_feedback("small-triangle-size", f'The small triangle has this number of rows:'), "white")
        print(l)
        TAc.print(LANG.render_feedback("big-triangle-size", f'The big triangle has this number of rows:'), "white")
        print(L)
        TAc.print(LANG.render_feedback("rough-small-triangle", f'The small triangle can be seen as a list of lists. In this case we have:'), "white")
        print(small)
        TAc.print(LANG.render_feedback("rough-big-triangle", f'The big triangle can be seen as a list of lists. In this case we have:'), "white")
        print(big)
        TAc.print(LANG.render_feedback("fit-question", f'How many times does the small triangle fit in the big triangle?'), "white")
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
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            exit(0)
        elif answer != right_answer:
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    
    visited_instances_2_exp_n = []
    for instance in instances['time_at_most_2_exp_n']:
        small_triangle = instance[0][0]
        big_triangle = instance[0][1]
        small = tl.cast_to_array(small_triangle)
        big = tl.cast_to_array(big_triangle)
        l = len(small_triangle)
        L = len(big_triangle)
        TAc.print(LANG.render_feedback("small-triangle-size", f'The small triangle has this number of rows:'), "white")
        print(l)
        TAc.print(LANG.render_feedback("big-triangle-size", f'The big triangle has this number of rows:'), "white")
        print(L)
        TAc.print(LANG.render_feedback("rough-small-triangle", f'The small triangle can be seen as a list of lists. In this case we have:'), "white")
        print(small)
        TAc.print(LANG.render_feedback("rough-big-triangle", f'The big triangle can be seen as a list of lists. In this case we have:'), "white")
        print(big)
        TAc.print(LANG.render_feedback("fit-question", f'How many times does the small triangle fit in the big triangle?'), "white")
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
        if time > MAX_TIME:
            visited_instances_2_exp_n.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n)
            exit(0)
        elif answer != right_answer:
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
        small_triangle = instance[0][0]
        big_triangle = instance[0][1]
        small = tl.cast_to_array(small_triangle)
        big = tl.cast_to_array(big_triangle)
        l = len(small_triangle)
        L = len(big_triangle)
        TAc.print(LANG.render_feedback("small-triangle-size", f'The small triangle has this number of rows:'), "white")
        print(l)
        TAc.print(LANG.render_feedback("big-triangle-size", f'The big triangle has this number of rows:'), "white")
        print(L)
        TAc.print(LANG.render_feedback("rough-small-triangle", f'The small triangle can be seen as a list of lists. In this case we have:'), "white")
        print(small)
        TAc.print(LANG.render_feedback("rough-big-triangle", f'The big triangle can be seen as a list of lists. In this case we have:'), "white")
        print(big)
        TAc.print(LANG.render_feedback("fit-question", f'How many times does the small triangle fit in the big triangle?'), "white")
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
        if time > MAX_TIME:
            visited_instances_correct.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            exit(0)
        elif answer != right_answer:
            visited_instances_correct.append([instance,time,"wrong"])
        else:
            visited_instances_correct.append([instance,time,"right"])
    
    visited_instances_2_exp_n = []
    for instance in instances['time_at_most_2_exp_n']:
        small_triangle = instance[0][0]
        big_triangle = instance[0][1]
        small = tl.cast_to_array(small_triangle)
        big = tl.cast_to_array(big_triangle)
        l = len(small_triangle)
        L = len(big_triangle)
        TAc.print(LANG.render_feedback("small-triangle-size", f'The small triangle has this number of rows:'), "white")
        print(l)
        TAc.print(LANG.render_feedback("big-triangle-size", f'The big triangle has this number of rows:'), "white")
        print(L)
        TAc.print(LANG.render_feedback("rough-small-triangle", f'The small triangle can be seen as a list of lists. In this case we have:'), "white")
        print(small)
        TAc.print(LANG.render_feedback("rough-big-triangle", f'The big triangle can be seen as a list of lists. In this case we have:'), "white")
        print(big)
        TAc.print(LANG.render_feedback("fit-question", f'How many times does the small triangle fit in the big triangle?'), "white")
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
        if time > MAX_TIME:
            visited_instances_2_exp_n.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n)
            exit(0)
        elif answer != right_answer:
            visited_instances_2_exp_n.append([instance,time,"wrong"])
        else:
            visited_instances_2_exp_n.append([instance,time,"right"])
    
    visited_instances_n_exp_2 = []
    for instance in instances['time_at_most_n_exp_2']:
        small_triangle = instance[0][0]
        big_triangle = instance[0][1]
        small = tl.cast_to_array(small_triangle)
        big = tl.cast_to_array(big_triangle)
        l = len(small_triangle)
        L = len(big_triangle)
        TAc.print(LANG.render_feedback("small-triangle-size", f'The small triangle has this number of rows:'), "white")
        print(l)
        TAc.print(LANG.render_feedback("big-triangle-size", f'The big triangle has this number of rows:'), "white")
        print(L)
        TAc.print(LANG.render_feedback("rough-small-triangle", f'The small triangle can be seen as a list of lists. In this case we have:'), "white")
        print(small)
        TAc.print(LANG.render_feedback("rough-big-triangle", f'The big triangle can be seen as a list of lists. In this case we have:'), "white")
        print(big)
        TAc.print(LANG.render_feedback("fit-question", f'How many times does the small triangle fit in the big triangle?'), "white")
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
        if time > MAX_TIME:
            visited_instances_n_exp_2.append([instance,time,"out_of_time"])
            print_goal_summary('correct',visited_instances_correct)
            print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n)
            print_goal_summary('time_at_most_n_exp_2',visited_instances_n_exp_2) 
            exit(0)
        elif answer != right_answer:
            visited_instances_n_exp_2.append([instance,time,"wrong"])
        else:
            visited_instances_n_exp_2.append([instance,time,"right"])
    
    print_goal_summary('correct',visited_instances_correct)
    print_goal_summary('time_at_most_2_exp_n',visited_instances_2_exp_n) 
    print_goal_summary('time_at_most_n_exp_2',visited_instances_n_exp_2) 
    exit(0)

