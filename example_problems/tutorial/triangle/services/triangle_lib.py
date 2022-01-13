#!/usr/bin/env python3
import random

from termcolor import colored

def check_val_range(val:int, MIN_VAL:int, MAX_VAL:int, TAc, LANG):
    if val < MIN_VAL or val > MAX_VAL:
        TAc.print(LANG.render_feedback("val-out-of-range", f"The value {val} falls outside the valid range [{MIN_VAL},{MAX_VAL}].", {"MIN_VAL":MIN_VAL, "MAX_VAL":MAX_VAL}), "red", ["bold"])
        return False
    return True

def check_yes_or_no_answer(ans:str, TAc, LANG):
    ans = ans.split()[0]
    if ans != "yes" and ans != "no":
        TAc.print(LANG.render_feedback("wrong-answer-range", f"The answer you provided is not 'yes' or 'no'."), "red", ["bold"])
        return False
    return True

def random_triangle(n:int, MIN_VAL:int, MAX_VAL:int, seed:int, TAc, LANG):
    if MAX_VAL < MIN_VAL:
        TAc.print(LANG.render_feedback("range-is-empty", f"Error: I can not choose the integers for the triangle from the range [{MIN_VAL},{MAX_VAL}] since this range is empty.", {"MIN_VAL":MIN_VAL, "MAX_VAL":MAX_VAL}), "red", ["bold"])
        exit(0)
    random.seed(seed)
    triangle = []
    values = [i for i in range (MIN_VAL,MAX_VAL+1)]
    for row in range(0,n):
        triangle.append(random.choices(values, k=row+1))
    return triangle

def print_triangle(triangle, file_format:bool =False):
    n = len(triangle)
    if file_format:
        print(n)
        for row in triangle:
            print(' '.join([str(ele).ljust(2) for ele in row]))
    else:
        left_margin = (2 * n) - 2
        for row in triangle:
            print(end="  "*left_margin)
            left_margin -= 1
            for ele in row:
                print(str(ele).ljust(2), end='  ')
            print()

            
def print_path(triangle, path_values, TAc, LANG):
    if len(triangle) - 1 != len(path_values):
        TAc.print(LANG.render_feedback("wrong-path-length", f"Error: The path you provided is not a feasible solution for this triangle, as it doesn't comprise {len(triangle) - 1} directions."),"red", ["bold"])
        exit(0)
    triangle_array = cast_to_array(triangle)
    n = len(triangle)
    path = [0]
    i = 0
    last_pos = 0
    for move in path_values:
        if(move == "L"):
            path.append(i+1 + last_pos)
            last_pos += i + 1 
        else:
            path.append(i+2 + last_pos)
            last_pos += i + 2 
        i += 1
    left_margin = (2 * n) - 2
    count = 0
    for row in triangle:
        print(end="  "*left_margin)
        left_margin -= 1
        for ele in row:
            if count in path:
                print(colored(str(ele).ljust(2),'cyan',attrs=['bold']), end='  ')
            else:
                print(str(ele).ljust(2), end='  ')
            count += 1
        print()
    return 
        
def calculate_path(triangle,path_values):
    triangle_array = cast_to_array(triangle)
    n = len(triangle)
    path = [triangle_array[0]]
    s = triangle_array[0]
    i = 0
    last_pos = 0
    for move in path_values:
        if(move == "L"):
            path.append(triangle_array[i+1 + last_pos])
            s += triangle_array[i+1 + last_pos]
            last_pos += i + 1 
        else:
            path.append(triangle_array[i+2 + last_pos])
            s += triangle_array[i+2 + last_pos]
            last_pos += i + 2 
        i += 1
    return s

def best_path_cost(triangle):
    dist = len(triangle)
    triangle_array = cast_to_array(triangle)
    triangle_array = triangle_array[::-1]
    i  = 0
    count = 1
    while dist > 1:
        triangle_array[i + dist] = max(triangle_array[i] + triangle_array[i + dist], triangle_array[i + 1] + triangle_array[i + dist])
        count += 1
        i += 1
        if count == dist:
            count = 1
            dist -= 1
            i += 1
    return triangle_array[i]
    
def random_path(m,n):
    directions = ["L","R"]
    if m==n:
        path = ''.join(map(str,random.choices(directions, k=random.randint(n-1,n-1))))
    else:
        path = ''.join(map(str,random.choices(directions, k=random.randint(m,n-1))))
    return path

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
            return False,[]
    return True,indexes
    
def cast_to_array(triangle):
    array = []
    for i in triangle:
        array += i
    return array

def print_triangle_occurencies(big_triangle,indexes):
    big_array = cast_to_array(big_triangle)
    n = len(big_triangle)
    count = 0
    index = 0
    left_margin = (2 * n) - 2
    for row in big_triangle:
        print(end="  "*left_margin)
        left_margin -= 1
        for ele in row:
            if index in indexes:
                print(colored(str(ele).ljust(2),'cyan',attrs=['bold']), end='  ')
                count += 1
            else:
                print(str(ele).ljust(2), end='  ')
            index += 1
        print()

def print_goal_summary(goal,testcases,num_testcases_passed,num_testcases_correct_ans,num_testcases_wrong_ans,out_of_time, TAc,LANG):
    TAc.print(LANG.render_feedback("summary", f'\n# SUMMARY OF THE RESULTS FOR GOAL "{goal}":\n'), "white", ["bold"])
    for t,i in zip(testcases,range(1,1+len(testcases))):
        if t['answer_is_correct'] == True:
            TAc.print(LANG.render_feedback("right-ans", f'# TestCase {i}: Correct answer! Took time {t["measured_time"]} on your machine.\n'), "green")
        elif t['answer_is_correct'] == False:
            if 'path' in t.keys():
                TAc.print(LANG.render_feedback("wrong-ans-with-path-in-instance", f'# NO! You gave the wrong solution for the instance with this parameters:\n#n = {t["n"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["seed"]}, path = {t["path"]}.\n'), "yellow")
            else:
                TAc.print(LANG.render_feedback("wrong-ans", f'# NO! You gave the wrong solution for the instance with this parameters:\n#n = {t["n"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["seed"]}.\n'), "yellow")
        else:
            if 'path' in t.keys():
                TAc.print(LANG.render_feedback("out-of-time-ans-with-path-in-instance", f'# The evaluation has been stopped since your solution took too much time on this or previous instances. The parameters of this instance are:\n#n = {t["n"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["seed"]}, path = {t["path"]}.\n'), "white")
            else:
                TAc.print(LANG.render_feedback("out-of-time-ans", f'# The evaluation has been stopped since your solution took too much time on this or previous instances. The parameters of this instance are:\n#n = {t["n"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["seed"]}.\n'), "white")
            
    if num_testcases_passed == len(testcases):
        TAc.print(LANG.render_feedback("right-in-time", f'# OK! Your solution achieved goal "{goal}".\n'), "green")
    if out_of_time > 0 and num_testcases_wrong_ans == 0:
        TAc.print(LANG.render_feedback("right-not-in-time", f'# OK! Though all answers produced by your solution are correct, still it exceeded the time limit on some instances. As such, you did not achieve goal "{goal}".\n'), "yellow")
    else:
        TAc.print(LANG.render_feedback("wrong-answ", f'# NO! Your solution gave wrong answers on at least one instance. Your solution does NOT achieve goal "{goal}".\n'), "red")   
