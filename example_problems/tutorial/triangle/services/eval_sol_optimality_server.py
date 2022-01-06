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
TAc.print(LANG.render_feedback("triangle-size", f'We give you a triangle with this number of rows:'), "white")

goals = [ 'correct' ]  # we intend to evaluate positively solutions as bad as O(2^{\choose(n,2)})
instances = { 'correct' : [] }
MIN_VAL = 10
MAX_VAL = 99
NUM_INSTANCES = 3
for n in range(2, 7):
    for _ in range(NUM_INSTANCES):
        seed = random.randint(100000,999999)
        instances['correct'].append([tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), n, MIN_VAL, MAX_VAL, seed])

prerequisites = {}
prerequisites['time_at_most_n^2'] = [time_at_most_2^n]
prerequisites['time_at_most_2^n'] = ['correct']
        
if ENV["goal"] in {'time_at_most_2^n','time_at_most_n^2'}:
    goals.append('time_at_most_2^n')
    instances['time_at_most_2^n'] = []
    MIN_N = 8  # could still be 2^{\choose(n,2)}
    MAX_N = 15  # we intend to evaluate positively solutions as bad as O(2^n)
    if ENV["code_lang"] == "compiled":
        MAX_N = 18
    NUM_INSTANCES = 1
    for _ in range(MIN_N, MAX_N):
        seed = random.randint(100000,999999)
        instances['time_at_most_2^n'].append([tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), n, MIN_VAL, MAX_VAL, seed])

if ENV["goal"] == 'time_at_most_n^2':
    goals.append('time_at_most_n^2')
    instances['time_at_most_n^2'] = []
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
        instances['time_at_most_n^2'].append([tl.random_triangle(n, MIN_VAL, MAX_VAL, seed, TAc, LANG), n, MIN_VAL, MAX_VAL, seed])
        n = math.ceil(n*scaling_factor)
        scaling_factor += 0.1
        if n > MAX_ROWS:
           n = MAX_ROWS

goals_achieved = []
goal_failed = None
for goal in goals:
    TAc.print(LANG.render_feedback("goal-open", f'We now test whether your solution attains goal {goal}:'), "yellow")
    for instance in instances[goal]:
        TAc.print(LANG.render_feedback("goal-failed", f'Your solution has failed on the above test instance. Goal {goal} has not been achieved.'), "yellow")
        if not test(instance):
            goal_failed = goal
            print_summary_and_exit()
    goals_achieved.append(goal)
    TAc.print(LANG.render_feedback("goal-achieved", f'Your solution has achieved goal {goal}!'), "yellow")

def print_summary_and_exit():
    TAc.print(LANG.render_feedback("summary", f'\nSUMMARY OF THE RESULTSS:'), "green", ["bold"])
    for goal in goals_achieved:
        TAc.print(LANG.render_feedback("goal", f' - Goal {goal}: '), end='', "white")
        TAc.print(LANG.render_feedback("achieved", 'achieved!'), end='', "green")
    if goal_failed != None:
        TAc.print(LANG.render_feedback("goal-failed", f' - Goal {goal_failed}: '), end='', "white")
        TAc.print(LANG.render_feedback("failed", 'failed!'), end='', "red", ["bold"])
        if ENV["goal"] == goal_failed:
            TAc.print(LANG.render_feedback("evaluation-stopped1", f'The evaluation has been stopped because of failure on a test-case for your goal.'), "white")
        else:
            TAc.print(LANG.render_feedback("evaluation-stopped2", f'The evaluation has been stopped because of failure on a test-case for goal {goal_failed}. Goal {goal_failed} is a necessary prerequisite for your goal {ENV["goal"]}.'), "white")
    exit(0)
        
           

#CHECK TIME ELAPSED         
for el in instances:
    time = 0
    triangle = el[0]
    seed = el[1]
    n = el[2]
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
    time += end-start
    if answer != tl.best_path_cost(el[0]):
        TAc.NO()
        TAc.print(LANG.render_feedback("no-wrong-sol", f'{answer} is the wrong solution. The best reward for this triangle (seed:{seed}, {n} rows) is {tl.best_path_cost(triangle)}'), "red")
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
