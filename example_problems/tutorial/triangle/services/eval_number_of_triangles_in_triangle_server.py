#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('code_lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

def cast_to_array(triangle):
    array = []
    for i in triangle:
        array += i
    return array

def fits(start,livello,big_triangle,small_triangle,small_size):
    last_visited = start
    indexes = [start]
    for i in range(1, small_size):
        last_visited += livello
        for j in range(i + 1):
            indexes.append(last_visited+j)
        last_visited += 1 
    for i in range(len(indexes)):
        if small_triangle[i] != big_triangle[indexes[i]]:
            return False
    return True
            
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
        MAX_ROWS_BIG *= 2
    big_scaling_factor = 1.3
    small_scaling_factor = 1.1
    big_n = 5
    small_n = 2
    for _ in range(NUM_OF_INSTANCES):
        seed_big = random.randint(100000,999999)
        seed_small = random.randint(100000,999999)
        instances.append([random_triangle(big_n, 0, 1, seed_big, TAc, LANG),random_triangle(small_n, 0, 1, seed_small, TAc, LANG)])
        big_n = math.ceil(big_n*big_scaling_factor)
        small_n = math.floor(small_n*small_scaling_factor)
        small_scaling_factor += 0.1
        if big_n > MAX_BIG_ROWS:
            big_n = MAX_BIG_ROWS
        if small_n > MAX_SMALL_ROWS:
            small_n = MAX_SMALL_ROWS
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
        instances.append([random_triangle(big_n, 0, 1, seed_big, TAc, LANG),random_triangle(small_n, 0, 1, seed_small, TAc, LANG),seed_big,big_n,seed_small,small_n])
        big_n = math.ceil(big_n*big_scaling_factor)
        small_n = math.floor(small_n*small_scaling_factor)
        small_scaling_factor += 0.4
        if big_n > MAX_BIG_ROWS:
            big_n = MAX_BIG_ROWS
        if small_n > MAX_SMALL_ROWS:
            small_n = MAX_SMALL_ROWS
            
#CHECK TIME ELAPSED         
for triangles in instances:
    start = monotonic() 
    answer = int(input(triangles))
    end = monotonic()
    time = end-start
    big = cast_to_array(triangles[0])
    small = cast_to_array(triangles[1])
    L = len(triangles[0])
    l = len(triangles[1])
    right_answer = 0
    livello = 1
    indexes = []
    for i in range(int(((L-l+1)*(L-l+2))/2)):   
        if i >= livello*(livello+1)/2:
            livello +=1
        if big[i] == small[0]:
            if fits(i,livello,big,small,next_indexes(i,livello,l)):
                indexes.append(next_indexes(i,livello,l))
                right_answer += 1
                
    if answer != right_answer:
        TAc.NO()
        TAc.print(LANG.render_feedback("no-wrong-sol", f'{answer} is the wrong solution. The correct number of occurencies for these triangles (big triangle seed:{triangles[2]}, big triangle rows:{triangles[3], small triangle seed:{triangles[4]}, small triangle rows {triangles[5] }) is {right_answer}.'), "red")
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





































# CHECK WHETHER THE PATH L/R ENCODING STRING HAS THE RIGHT LENGTH

if len(ENV["path"].replace(" ", "")) != ENV["n"]-1:
    TAc.NO()
    if len(ENV["path"].replace(" ", "")) < ENV["n"]-1:
        TAc.print(LANG.render_feedback("path-too-short", f'The string of the L/R choices encoding your path is too short for a triangle with n={ENV["n"]} rows.'), "red", ["bold"])
    if len(ENV["path"].replace(" ", "")) > ENV["n"]-1:
        TAc.print(LANG.render_feedback("path-too-long", f'The string of the L/R choices encoding your path is too long for a triangle with n={ENV["n"]} rows.'), "red", ["bold"])
    TAc.print(LANG.render_feedback("wrong-path-length", f'The true number of required choices is n-1={ENV["n"]-1} instead of {len(ENV["path"].replace(" ", ""))}.'), "red", ["bold"])
    exit(0)


# TRIANGLE GENERATION

if ENV['how_to_input_the_triangle'] == "my_own_triangle":
    triangle = []
    TAc.print(LANG.render_feedback("insert-triangle", f'Please, insert your triangle, line by line. For every i in [1,{ENV["n"]}], line i comprises i integers separated by spaces.'), "yellow", ["bold"])
    for i in range(1,ENV["n"]+1):
        TAc.print(LANG.render_feedback("insert-line", f'Insert line i={i}, that is, {i} integers separated by spaces:'), "yellow")
        line = TALinput(int, i, token_recognizer=lambda val,TAc,LANG: check_val_range(val,0,99,TAc,LANG), TAc=TAc, LANG=LANG)
        triangle.append(line)
    TAc.OK()
    TAc.print(LANG.render_feedback("triangle-insertion-completed", f'Insertion complete. Your triangle has been successfully inserted.'), "green")
else:
    triangle = random_triangle(ENV["n"],0,99,int(ENV['how_to_input_the_triangle']),TAc,LANG)
if not ENV['silent'] or ENV['display_triangle'] or ENV['reward_the_path'] or ENV['how_to_input_the_triangle'] == "my_own_triangle":
    TAc.print(LANG.render_feedback("feasible-path", f'Your solution path ({ENV["path"]}) is a feasible one for this problem since it comprises {ENV["n"]-1} subsequent choices of directions (the correct number).'), "green", ["bold"])
if ENV['display_triangle']:
    TAc.print(LANG.render_feedback("display-triangle", f'The triangle of reference is the following:'), "green", ["bold"])
    print_triangle(triangle)
if ENV['reward_the_path']:
    TAc.print(LANG.render_feedback("path-reward", f'The total reward collected by your path is {calculate_path(triangle,ENV["path"].replace(" ", ""))}.'), "green", ["bold"])        

exit(0)
