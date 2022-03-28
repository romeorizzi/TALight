#!/usr/bin/env python3
import os
import random
import math
import json

from termcolor import colored
from contextlib import redirect_stdout

### CONSTANTS #########################################
AVAILABLE_FORMATS = {'instance':{'pyramid':'pyramid.txt', 'lines':'lines.txt','gmpl':'gmpl.dat'},'solution':{'int_and_string':'int_and_string.txt'}}
DEFAULT_INSTANCE_FORMAT='lines.txt'
DEFAULT_SOLUTION_FORMAT='int_and_string'
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

def str_to_sequence(string: str) -> list:
    #print(f"str_to_sequence  called with {string=}")
    return [char for char in string]

def sequence_to_str(sequence):
    #print(f"sequence_to_str  called with {sequence=}")
    return "".join(e for e in sequence)

def annotated_subseq_to_sequence(annotated_solution):
    #print(f"annotated_subseq_to_sequence  called with {annotated_solution=}")
    return [annotated_solution[key] for key in sorted(annotated_solution)]

def annotated_subseq_to_str(annotated_solution) -> str:
    #print(f"annotated_subseq_to_str  called with {annotated_solution=}")
    return sequence_to_str(annotated_subseq_to_sequence(annotated_solution))

def render_annotated_subseq_as_str(solution) -> str:
    #print(f"render_annotated_subseq_as_str  called with {solution=}")
    return '\n'.join([f'{solution[key]} {key[0]} {key[1]}' for key in sorted(solution)])

def read_annotated_subseq(raw_annotated_subseq: str):
    #print(f"read_annotated_subseq  called with {raw_annotated_subseq=}")
    sol = {}
    for line in raw_annotated_subseq[:-1].split('\n'):
        values = line.split()
        sol[(int(values[1]), int(values[2]))] = values[0]
    return sol

# MANAGING REPRESENTATIONS OF INSTANCES:

# YIELD STRING REPRESENTATIONS OF GIVEN INSTANCE:

def instance_to_txt_str(instance, format_name):
    """Of the given <instance>, this function returns the .txt string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    triangle = instance['triangle']
    n = instance['n']
    MIN_VAL = instance['MIN_VAL']
    MAX_VAL = instance['MAX_VAL']
    seed = instance['seed']
    big_triangle = instance['big_triangle']
    m = instance['m']
    MIN_VAL_BIG = instance['MIN_VAL_BIG']
    MAX_VAL_BIG = instance['MAX_VAL_BIG']
    big_seed = instance['big_seed']
    measured_time = None
    answer_correct = None
    path = instance['path']
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
        output += f"\n**************************\n"
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
        output += f"\n{n}\n{m}\n{MIN_VAL}\n{MAX_VAL}\n{MIN_VAL_BIG}\n{MAX_VAL_BIG}\n{seed}\n{big_seed}\n{path}\n{measured_time}\n{answer_correct}"
    else:   
        output += f'{n}\n'
        for num_linea in range(n):
            array = triangle[num_linea]
            for el in array:
                output += str(el) + " "
            output += "\n"
        output += f"\n**************************\n"
        output += f'\n{m}\n'
        for num_linea in range(m):
            array = big_triangle[num_linea]
            for el in array:
                output += str(el) + " "
            output += "\n"
        output += f"\n{MIN_VAL}\n{MAX_VAL}\n{MIN_VAL_BIG}\n{MAX_VAL_BIG}\n{seed}\n{big_seed}\n{path}\n{measured_time}\n{answer_correct}"
    return output
    
def instance_to_dat_str(instance,format_name=''):
    """Of the given <instance>, this function returns the .dat string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    triangle = instance['triangle']
    n = instance['n']
    MIN_VAL = instance['MIN_VAL']
    MAX_VAL = instance['MAX_VAL']
    seed = instance['seed']
    big_triangle = instance['big_triangle']
    m = instance['m']
    MIN_VAL_BIG = instance['MIN_VAL_BIG']
    MAX_VAL_BIG = instance['MAX_VAL_BIG']
    big_seed = instance['big_seed']
    path = instance['path']
    measured_time = None
    answer_correct = None
    output = f"param n := {n};                  # Number of lines of the triangle\n"
    output += f"param m := {m};                  # Number of lines of the triangle\n"
    output += f"param MIN_VAL := {MIN_VAL};            # Minimum element value of the small triangle\n"
    output += f"param MAX_VAL:= {MAX_VAL};            # Maximum element value of the small triangle\n"        
    output += f"param MIN_VAL_BIG := {MIN_VAL_BIG};        # Minimum element value of the big triangle\n"
    output += f"param MAX_VAL_BIG := {MAX_VAL_BIG};       # Maximum element value of the big triangle\n"
    output += f"param seed := {seed};          # Seed generating the  small triangle\n"
    output += f"param big_seed := {big_seed};      # Seed generating the big triangle\n"
    output += f"param path := {path};              # Path along the given triangle\n"
    output += f"param measured_time := {None};   # Instance solving time\n"
    output += f"param answer_correct := {None};  # Solution to instance is correct\n"
    output += "param: SMALL_STRINGS "
    for i in range(n):
        output += "  "*i
        output += f"LINE_{i+1}"
    output += f":=\n                       {triangle[0]}  "
    for i in range(1,n):
        output += f" {triangle[i]}"
        output += " "*2
    output += ";\n"
    output += "param: BIG_STRINGS "
    for i in range(m):
        output += "  "*i
        output += f"LINE_{i+1} "
    output += f":=\n                      {big_triangle[0]}  "
    for i in range(1,m):
        output += f" {big_triangle[i]}"
        output += " "*2
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
    if format_name == "pyramid":
        delim = str_to_arr.index("**************************")
        instance['triangle'] = triangle_from_array([int(x) for x in str_to_arr[0:delim]]) # assign small triangle
        instance['big_triangle'] = triangle_from_array([int(x) for x in str_to_arr[delim+1:-8]]) # assign big triangle
    else:
        delim = str_to_arr.index("**************************")
        instance['triangle'] = triangle_from_array([int(x) for x in str_to_arr[1:delim]]) # assign small triangle
        instance['big_triangle'] = triangle_from_array([int(x) for x in str_to_arr[delim+2:-8]]) # assign big triangle
    instance['n'] = len(instance['triangle'])
    instance['m'] = len(instance['big_triangle'])
    instance['MIN_VAL'] = int(str_to_arr[-9]) # assign MIN_VAL_SMALL
    instance['MAX_VAL'] = int(str_to_arr[-8]) # assign MAX_VAL_SMALL
    instance['MIN_VAL_BIG'] = int(str_to_arr[-7]) # assign MIN_VAL_BIG
    instance['MAX_VAL_BIG'] = int(str_to_arr[-6]) # assign MAX_VAL_BIG
    instance['seed'] = int(str_to_arr[-5]) # assign small_seed
    instance['big_seed'] = int(str_to_arr[-4]) # assign big_seed
    instance['path'] = str_to_arr[-3].replace(" ","") # assign path
    instance['measured_time'] = None # assign measured_time
    instance['answer correct'] = None # assign answer_correct 
    return instance
    
def get_instance_from_dat(instance_as_str, format_name):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
    split_instance = instance_as_str.split(";")
    instance = {}
    instance['triangle'] = json.loads("["+get_param(split_instance[11]).replace(" ","").replace("\n","").replace("][","],[")+"]") # assign small triangle
    instance['big_triangle'] = json.loads("["+get_param(split_instance[12]).replace(" ","").replace("\n","").replace("][","],[")+"]") # assign big triangle
    instance['n'] = int(get_param(split_instance[0])) # assign n
    instance['m'] = int(get_param(split_instance[1])) # assign m
    instance['MIN_VAL_SMALL'] = int(get_param(split_instance[2])) # assign MIN_VAL_SMALL
    instance['MAX_VAL_SMALL'] = int(get_param(split_instance[3])) # assign MAX_VAL_SMALL
    instance['MIN_VAL_BIG'] = int(get_param(split_instance[4])) # assign MIN_VAL_BIG
    instance['MAX_VAL_BIG'] = int(get_param(split_instance[5])) # assign MAX_VAL_BIG
    instance['small_seed'] = int(get_param(split_instance[6])) # assign small_seed
    instance['big_seed'] = int(get_param(split_instance[7])) # assign big_seed
    instance['path'] = get_param(split_instance[8]).replace(" ","") # assign big_seed
    instance['measured_time'] = None # assign measured_time
    instance['answer_correct'] = None # assign answer_correct
    return instance


# SUPPORT METHODS

def instances_generator(num_instances, scaling_factor: float, MIN_VAL: int, MAX_VAL: int, MIN_N: int, MAX_N: int, MIN_M = 0, MAX_M = 0, MIN_VAL_BIG = 0, MAX_VAL_BIG = 0):
    instances = [] 
    n = MIN_N
    m = MIN_M
    for _ in range(num_instances):
        instance = {}
        # first triangle
        seed = random.randint(100000,999999)
        instance['n'] = n
        instance['triangle'] = random_triangle(n,MIN_VAL,MAX_VAL,seed)
        instance['MIN_VAL'] = MIN_VAL
        instance['MAX_VAL'] = MAX_VAL
        instance['seed'] = seed
        instance['path'] = random_path(n,n)
        n = math.ceil(scaling_factor*n)
        if n > MAX_N:
            n = MAX_N
        #second triangle
        instance['m'] = m
        instance['big_triangle'] = random_triangle(m,MIN_VAL_BIG,MAX_VAL_BIG,seed)
        instance['MIN_VAL_BIG'] = MIN_VAL_BIG
        instance['MAX_VAL_BIG'] = MAX_VAL_BIG
        instance['big_seed'] = seed
        m = math.ceil(scaling_factor*m)
        if m > MAX_M:
            m = MAX_M
        instance['measured_time'] = None
        instance['answer_correct'] = None
        instances.append(instance)
    return instances
    
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
    
def random_triangle(n:int, MIN_VAL:int, MAX_VAL:int, seed:int):
    random.seed(seed)
    triangle = []
    values = [i for i in range (MIN_VAL,MAX_VAL+1)]
    for row in range(0,n):
        triangle.append(random.choices(values, k=row+1))
    return triangle

def print_triangle(triangle):
    n = len(triangle)
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


       
       

        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
