#!/usr/bin/env python3
import random
import math

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

def best_reward_and_path(triangle):
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
    reward = triangle_array[i]
    triangle_array = triangle_array[::-1]
    path = ""
    last_pos = 0
    dist = len(triangle)
    for j in range(dist-1):
        if triangle_array[j+1 + last_pos] > triangle_array[j+2 + last_pos] :
            path += "L"
            last_pos += j + 1 
        else:
            path += "R"
            last_pos += j + 2 
    return reward,path
    
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
            elif 'MIN_SMALL_N' in t.keys():
                TAc.print(LANG.render_feedback("wrong-ans", f'# NO! You gave the wrong solution for the instance with this parameters:\n#SMALL TRIANGLE: n = {t["MIN_SMALL_N"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["small_seed"]}.\n#BIG TRIANGLE: n = {t["MIN_BIG_N"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["big_seed"]}.\n'), "yellow")
            else:
                TAc.print(LANG.render_feedback("wrong-ans", f'# NO! You gave the wrong solution for the instance with this parameters:\n#n = {t["n"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["seed"]}.\n'), "yellow")
        else:
            if 'path' in t.keys():
                TAc.print(LANG.render_feedback("out-of-time-ans-with-path-in-instance", f'# The evaluation has been stopped since your solution took too much time on this or previous instances. The parameters of this instance are:\n#n = {t["n"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["seed"]}, path = {t["path"]}.\n'), "white")
            elif 'MIN_SMALL_N' in t.keys():
                TAc.print(LANG.render_feedback("out-of-time-t-in-T", f'# The evaluation has been stopped since your solution took too much time on this or previous instances. The parameters of this instance are:\n#SMALL TRIANGLE: n = {t["MIN_SMALL_N"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["small_seed"]}.\n#BIG TRIANGLE: n = {t["MIN_BIG_N"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["big_seed"]}.\n'), "yellow")
            else:
                TAc.print(LANG.render_feedback("out-of-time-ans", f'# The evaluation has been stopped since your solution took too much time on this or previous instances. The parameters of this instance are:\n#n = {t["n"]}, MIN_VAL = {t["MIN_VAL"]}, MAX_VAL = {t["MAX_VAL"]}, seed = {t["seed"]}.\n'), "white")
       
    if num_testcases_passed == len(testcases):
        TAc.print(LANG.render_feedback("right-in-time", f'# OK! Your solution achieved goal "{goal}".\n'), "green")
    if out_of_time > 0 and num_testcases_wrong_ans == 0:
        TAc.print(LANG.render_feedback("right-not-in-time", f'# OK! Though all answers produced by your solution are correct, still it exceeded the time limit on some instances. As such, you did not achieve goal "{goal}".\n'), "yellow")
    elif num_testcases_wrong_ans != 0:
        TAc.print(LANG.render_feedback("wrong-answ", f'# NO! Your solution gave wrong answers on at least one instance. Your solution does NOT achieve goal "{goal}".\n'), "red")   

def print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG):    
    TAc.print(LANG.render_feedback('summary-of-results', '# SUMMARY OF RESULTS:'), 'green')
    num_instances = {}
    num_instances_passed = {}
    num_instances_correct_ans = {}
    num_instances_wrong_ans = {}
    alive = True
    for goal in goals:
        num_instances[goal] = len(instances[goal])
        num_instances_passed[goal] = 0
        num_instances_correct_ans[goal] = 0
        num_instances_wrong_ans[goal] = 0
        for instance in instances[goal]:
            if instance['answer_is_correct'] == False:
                num_instances_wrong_ans[goal] += 1
            elif instance['answer_is_correct'] == True:
                num_instances_correct_ans[goal] += 1
                if instance['measured_time'] <= MAX_TIME:
                    num_instances_passed[goal] += 1
        if alive:
            print_goal_summary(goal,instances[goal],num_instances_passed[goal],num_instances_correct_ans[goal],num_instances_wrong_ans[goal], out_of_time, TAc,LANG)
        if num_instances_passed[goal] < num_instances[goal]:
            alive = False
    TAc.print(LANG.render_feedback('short-summary-of-results', '# SUMMARY OF RESULTS:'), 'green')
    for goal in goals:
        if num_instances_passed[goal] == num_instances[goal]:
            TAc.print(LANG.render_feedback('goal-passed', f'# Goal {goal}: PASSED (passed instances: {num_instances_passed[goal]}/{num_instances[goal]} instances)'), 'green', ['bold'])
        else:
            TAc.print(LANG.render_feedback('goal-NOT-passed', f'# Goal {goal}: NOT passed (passed instances: {num_instances_passed[goal]}/{num_instances[goal]} instances, correct answers: {num_instances_correct_ans[goal]}/{num_instances[goal]}, wrong answers: {num_instances_wrong_ans[goal]}/{num_instances[goal]} instances)'), 'red', ['bold'])
    TAc.print(f"\n# WE HAVE FINISHED", "white")

def separate_answer(answer):
    r = ""
    p = ""
    for i in range(len(answer)):
        if answer[i].isdigit():
            r += answer[i]
        else:
            p += answer[i]
    return [int(r),p]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
