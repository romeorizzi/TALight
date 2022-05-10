#!/usr/bin/env python3
import os
import random
import math
from datetime import datetime

from termcolor import colored
from contextlib import redirect_stdout

### CONSTANTS #########################################
AVAILABLE_FORMATS = {'instance':{'pyramid':'pyramid.txt', 'in_lines':'in_lines.txt','triangle_dat':'triangle.dat'},'solution':{'all_solutions': 'all_solutions.txt'}}
DEFAULT_INSTANCE_FORMAT='in_lines'
DEFAULT_SOLUTION_FORMAT='all_solutions'
#######################################################

def format_name_to_file_extension(format_name, format_gender):
    assert format_gender in AVAILABLE_FORMATS, f'No format has been adopted for objects of the gender `{format_gender}`.'
    assert format_name in AVAILABLE_FORMATS[format_gender], f'Format_name `{format_name}` unsupported for objects of gender {format_gender}.'
    return AVAILABLE_FORMATS[format_gender][format_name]

def file_extension_to_format_name(file_extension):
    for format_gender in AVAILABLE_FORMATS:
        for format_name in AVAILABLE_FORMATS[format_gender]:
            if AVAILABLE_FORMATS[format_gender][format_name] == file_extension:
                return format_name
    assert False, f'No adopted format is associated to the file_extension `{file_extension}`.'

def format_name_expand(format_name, format_gender):
    long_format_name = format_name_to_file_extension(format_name, format_gender)
    format_list = long_format_name.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = None
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    return format_primary, format_secondary
    
# MANAGING REPRESENTATIONS OF SOLUTIONS:

def solutions(instance,path,instance_format=DEFAULT_INSTANCE_FORMAT):
    sols = {}
    sols['check_feasible_sol'] = len(path) == instance['n'] -1 # the given path is a feasible solution
    if sols['check_feasible_sol']:
        sols['check_and_reward_one_sol'] = f"{calculate_path(instance['triangle'],path)} (path = {path})"
    else:
        sols['check_and_reward_one_sol'] = f"None # expected path length = {instance['n']-1}, but received a path whose length is {len(path)}"
    value, best_path = best_reward_and_path(instance['triangle'])
    sols['check_best_sol'] = f"best reward: {value}, best_path: {best_path}"
    if instance['n'] <= instance['m']:
        sols['check_number_of_triangles_in_triangle'] = num_of_occurrences(cast_to_array(instance['triangle']),cast_to_array(instance['big_triangle']),instance['n'],instance['m'])[0]
    else:
        sols['check_number_of_triangles_in_triangle'] = f"None # expected m>n, but received m = {instance['m']} and n = {instance['n']}"
    return sols

# MANAGING REPRESENTATIONS OF INSTANCES:

# YIELD STRING REPRESENTATIONS OF GIVEN INSTANCE:

def instance_to_str(instance, format_name=DEFAULT_INSTANCE_FORMAT):
    """This function returns the string representation of the given <instance> provided in format <instance_format_name>"""
    format_primary, format_secondary = format_name_expand(format_name, 'instance')
    if format_primary == 'dat':
        return instance_to_dat_str(instance, format_name)
    if format_primary == 'txt':
        return instance_to_txt_str(instance, format_name)

def instance_to_txt_str(instance, format_name="pyramid"):
    """Of the given <instance>, this function returns the .txt string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    triangle = instance['triangle']
    n = instance['n']
    if 'm' in instance.keys():
        big_triangle = instance['big_triangle']    
        m = instance['m']
    else:
        m = 0    
    output= f''
    if format_name == 'pyramid':
        for num_linea in range(n):
            output+=f" "*2*(n-1-num_linea)
            array = triangle[num_linea]
            for i in range(num_linea+1):
                el = str(array[i])
                if len(el) == 1:
                    output += el + "   "
                else:
                    output += el + "  "
            output += " "*2*(n-num_linea) + "\n"
        if m!= 0:
            output += "\n#\n\n"
        for num_linea in range(m):
            output+=f" "*2*(m-1-num_linea)
            array = big_triangle[num_linea]
            for i in range(num_linea+1):
                el = str(array[i])
                if len(el) == 1:
                    output += el + "   "
                else:
                    output += el + "  "
            output += " "*2*(m-num_linea) + "\n"
    else:   
        output += f'{n}\n'
        for num_linea in range(n):
            array = triangle[num_linea]
            for el in array:
                output += str(el) + " "
            output += "\n"
        if m!= 0:
            output += "\n#\n\n"
            output += f'{m}\n'
            for num_linea in range(m):
                array = big_triangle[num_linea]
                for el in array:
                    output += str(el) + " "
                output += "\n"
    return output
    
def instance_to_dat_str(instance,format_name='triangle_dat'):
    """Of the given <instance>, this function returns the .dat string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    triangle = instance['triangle']
    n = instance['n']
    if 'm' in instance.keys():
        big_triangle = instance['big_triangle']    
        m = instance['m']
    else:
        m = 0   
    output = f"param n := {n};                  # Number of lines of the triangle\n"
    if m!= 0:
        output += f"param m := {m};                  # Number of lines of the triangle\n"
    output += "param: SMALL_TRIANGLE "    
    output += f":= {triangle[0]} "
    for i in range(1,n):
        output += f"{triangle[i]} "
    if m!= 0:
        output += ";\nparam: BIG_TRIANGLE "
        output += f":= {big_triangle[0]} "
        for i in range(1,m):
            output += f"{big_triangle[i]} "
    output += ";\nend;"
    return output

# GET INSTANCE FROM STRING REPRESENTATION:
def get_instance_from_str(instance_as_str, instance_format_name=DEFAULT_INSTANCE_FORMAT):
    """This function returns the instance it gets from its string representation as provided in format <instance_format_name>."""
    format_primary, format_secondary = format_name_expand(instance_format_name, 'instance')
    if format_primary == 'dat':
        return get_instance_from_dat(instance_as_str, instance_format_name)
    if format_primary == 'txt':
        return get_instance_from_txt(instance_as_str, instance_format_name)

def get_instance_from_txt(instance_as_str, format_name):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
    instance = {}
    str_to_arr = instance_as_str.split()
    delim = "#"
    if delim in str_to_arr:
        del_index = str_to_arr.index(delim)        
        instance['triangle'] = triangle_from_array([int(x) for x in str_to_arr[:del_index]])
        instance['big_triangle'] = triangle_from_array([int(x) for x in str_to_arr[del_index+1:]])
        instance['n'] = len(instance['triangle'])        
        instance['m'] = len(instance['big_triangle'])        
    else:
        instance['triangle'] = triangle_from_array([int(x) for x in str_to_arr])
        instance['n'] = len(instance['triangle'])        
    return instance
    
def get_instance_from_dat(instance_as_str, format_name):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
    split_instance = instance_as_str.split(";")
    instance = {}
    if len(split_instance) != 4:
        instance['n'] = int(get_param(split_instance[0])) # assign n
        instance['m'] = int(get_param(split_instance[1])) # assign m
        instance['triangle'] = list(ast.literal_eval(get_param(split_instance[2]).replace("] [","],[").replace(" ",""))) # assign triangle
        instance['big_triangle'] = list(ast.literal_eval(get_param(split_instance[3]).replace("] [","],[").replace(" ",""))) # assign big triangle
    else:
        instance['n'] = int(get_param(split_instance[0])) # assign n
        instance['triangle'] = list(ast.literal_eval(get_param(split_instance[1]).replace("] [","],[").replace(" ","")))
    return instance


# SUPPORT METHODS

def instances_generator(num_instances, scaling_factor: float, MIN_VAL: int, MAX_VAL: int, MIN_N: int, MAX_N: int, MIN_M = 0, MAX_M = 0, seed = "random_seed", big_seed = "random_seed"):
    instances = [] 
    n = MIN_N
    m = MIN_M
    for _ in range(num_instances):
        instance = {}
        # first triangle
        if seed == "random_seed":
            seed = random.randint(100000,999999)
        instance['n'] = n
        instance['triangle'] = random_triangle(n,MIN_VAL,MAX_VAL,seed)
        instance['MIN_VAL'] = MIN_VAL
        instance['MAX_VAL'] = MAX_VAL
        instance['seed'] = seed
        n = math.ceil(scaling_factor*n)
        if n > MAX_N:
            n = MAX_N
        #second triangle
        if big_seed == "random_seed":
            big_seed = random.randint(100000,999999)
        instance['m'] = m
        instance['big_triangle'] = random_triangle(m,MIN_VAL,MAX_VAL,big_seed)
        instance['big_seed'] = big_seed
        m = math.ceil(scaling_factor*m)
        if m > MAX_M:
            m = MAX_M
        instance['measured_time'] = None
        instance['answer_correct'] = None
        instances.append(instance)
    return instances

def check_yes_or_no_answer(val:str, TAc, LANG):
    if val != "yes" and val != "no":
        TAc.print(LANG.render_feedback("val-not-correct", f"The answer {val} is not 'yes' or 'no'."), "red", ["bold"])
        return False
    return True

def check_val_range(val:int, MIN_VAL:int, MAX_VAL:int, TAc, LANG):
    print(type(val))
    if val < MIN_VAL or val > MAX_VAL:
        TAc.print(LANG.render_feedback("val-out-of-range", f"The value {val} falls outside the valid range [{MIN_VAL},{MAX_VAL}].", {"MIN_VAL":MIN_VAL, "MAX_VAL":MAX_VAL}), "red", ["bold"])
        return False
    return True

def check_path(ans:str, TAc, LANG):
    for d in ans:
        if d!= "L" and d != "R":
            TAc.print(LANG.render_feedback("wrong-answer-range", f"The path you provided does not consist only of 'L's or 'R's."), "red", ["bold"])
            return False
    return True
    
def random_triangle(n:int, MIN_VAL:int, MAX_VAL:int, seed:int):
    random.seed(seed)
    triangle = []
    values = [i for i in range (MIN_VAL,MAX_VAL+1)]
    for row in range(0,n):
        triangle.append(random.choices(values, k=row+1))
    return triangle

def print_triangle(triangle,instance_format=DEFAULT_INSTANCE_FORMAT):
    n = len(triangle)
    if instance_format == "pyramid":
        left_margin = (2 * n) - 2
        for row in triangle:
            print(end="  "*left_margin)
            left_margin -= 1
            for ele in row:
                 print(str(ele).ljust(2), end='  ')
            print()
    else:
        print(n)
        for line in triangle:
            l = ""
            for el in line:
                l+= f"{el} "
            print(f"{l}")
             
def print_path(triangle, path_values,instance_format=DEFAULT_INSTANCE_FORMAT):
    if instance_format == "pyramid":
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
    else:
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
        count = 0
        for row in triangle:
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
    random.seed(int(round(datetime.now().timestamp())))
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

def num_of_occurrences(small,big,l,L):
    right_answer = 0
    livello = 1
    indexes = []
    for i in range(int(((L-l+1)*(L-l+2))/2)):   
        if i >= livello*(livello+1)/2:
            livello +=1
        if big[i] == small[0]:
            if fits(i,livello,big,small,l)[0]:
                indexes.append(fits(i,livello,big,small,l)[1])
                right_answer += 1
    return right_answer, indexes  
    
def cast_to_array(triangle):
    array = []
    for i in triangle:
        array += i
    return array

def print_triangle_occurencies(big_triangle,indexes,instance_format=DEFAULT_INSTANCE_FORMAT):
    if instance_format == "pyramid":
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
    else:
        big_array = cast_to_array(big_triangle)
        n = len(big_triangle)
        count = 0
        index = 0
        left_margin = (2 * n) - 2
        for row in big_triangle:
            for ele in row:
                if index in indexes:
                    print(colored(str(ele).ljust(2),'cyan',attrs=['bold']), end='  ')
                    count += 1
                else:
                    print(str(ele).ljust(2), end='  ')
                index += 1
            print()
    return
        
def separate_answer(answer):
    r = ""
    p = ""
    for i in range(len(answer)):
        if answer[i].isdigit():
            r += answer[i]
        else:
            p += answer[i]
    return [int(r),p]

def triangle_from_array(elements):
    t = []
    i = 0
    j = 1
    while j < len(elements) + 1: 
        t.append(elements[i:j])
        k = i
        i = j
        j += int(math.sqrt(k+j)) + 1
    return t       

def get_param(string):
    answer = ""
    for i in range(1,len(string)):
        if string[-i] == "=":
            return answer[::-1]
        else:
            answer += string[-i]
    return answer[::-1]

def get_instance_from_terminal(p1,p2):
    instance = {}
    instance['triangle'] = random_triangle(int(p1[0]),int(p1[1]),int(p1[2]),int(p1[3]))
    instance['n'] = int(p1[0])
    instance['MIN_VAL'] = int(p1[1])
    instance['MAX_VAL'] = int(p1[2])
    instance['seed'] = int(p1[3])
    if len(p2) != 0:
        instance['m'] = int(p2[0])
        instance['MIN_VAL_BIG'] = int(p2[1])
        instance['MAX_VAL_BIG'] = int(p2[2])
        instance['big_seed'] = int(p2[3])
        instance['big_triangle'] = random_triangle(int(p2[0]),int(p2[1]),int(p2[2]),int(p2[3]))
    instance['path'] = p1[4]
    instance['measured_time'] = None
    instance['answer_correct'] = None
    return instance 
    
    
def print_goal_summary(goal,testcases,num_testcases_passed,num_testcases_correct_ans,num_testcases_wrong_ans,out_of_time, TAc,LANG):
    TAc.print(LANG.render_feedback("summary", f'\n# SUMMARY OF THE RESULTS FOR GOAL "{goal}":\n'), "white", ["bold"])
    for t,i in zip(testcases,range(1,1+len(testcases))):
        if t['answer_correct'] == True:
            TAc.print(LANG.render_feedback("right-ans", f'# TestCase {i}: Correct answer! Took time {t["measured_time"]} on your machine.\n'), "green")
        elif t['answer_correct'] == False:
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
            if instance['answer_correct'] == False:
                num_instances_wrong_ans[goal] += 1
            elif instance['answer_correct'] == True:
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
  
