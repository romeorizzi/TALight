#!/usr/bin/env python3
import random

from termcolor import colored

def check_val_range(val:int, MIN_VAL:int, MAX_VAL:int, TAc, LANG):
    if val < MIN_VAL or val > MAX_VAL:
        TAc.print(LANG.render_feedback("val-out-of-range", f"The value {val} falls outside the valid range [{MIN_VAL},{MAX_VAL}].", {"MIN_VAL":MIN_VAL, "MAX_VAL":MAX_VAL}), "red", ["bold"])
        return False
    return True

def check_yes_or_no_answer(ans:str, TAc, LANG):
    if ans != "yes" and ans != "no":
        TAc.print(LANG.render_feedback("wrong-answer-range", f"The answer you provided is not 'yes' or 'no'."), "red", ["bold"])
        return False
    return True
    
def random_triangle(n:int, MIN_VAL:int, MAX_VAL:int, seed:int, TAc, LANG):
    if MAX_VAL < MIN_VAL:
        TAc.print(LANG.render_feedback("range-is-empty", f"Error: I can not choose the integers for the triangle from the range [{MIN_VAL},{MAX_VAL}] since this range is empty.", {"MIN_VAL":MIN_VAL, "MAX_VAL":MAX_VAL}), "red", ["bold"])
        exit(0)
    random.seed(seed,version=2)
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
            print(' '.join([str(ele).rjust(2) for ele in row]))
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
    triangle_array = []
    for l in triangle:
        triangle_array += l
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
    triangle_array = []
    for l in triangle:
        triangle_array += l
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
    triangle_array = []
    for l in triangle:
        triangle_array += l
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
    small_index = 1
    pos = start
    array = [big_triangle[start]]
    for profondita in range(small_size - 1):
        pos += livello
        livello += 1
        for index in range(profondita + 2):
            if big_triangle[pos + index] != small_triangle[small_index]:
                return False
            small_index +=1
    return True

def cast_to_array(triangle):
    array = []
    for i in triangle:
        array += i
    return array
