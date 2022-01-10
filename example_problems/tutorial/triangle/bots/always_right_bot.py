#!/usr/bin/python
from sys import stderr, exit, argv
import random

usage=f"""I am a bot that always provides the right answer. I have the following functionalities:
[1] eval feasible solution 
[2] check and reward one sol
[3] best sol
[4] number of triangles in triangle
."""

def myinput():
    spoon = ""
    while len(spoon) == 0 or spoon[0] == '#':
        try:
            spoon = input()
        except EOFError:
            exit(0)
    return spoon

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

if len(argv) != 2:
    print("WARNING! Wrong number of arguments.")
    print(usage)
    exit(0)

# EVAL FEASIBLE SOLUTION 
if argv[1] == "1":
    while True:
        # get triangle size:
        myinput() # eat triangle-size statement
        n = int(myinput())
        # get/eat triangle instance:
        for i in range(n+1):
            myinput() # eat triangle-instance statement + n rows
        # give your answer:
        myinput() # eat prompt
        directions = ['L','R']
        answer = "".join(random.choices(directions,k=n-1))
        print(answer)
    exit(0)

# EVAL AND REWARD ONE SOL
if argv[1] == "2":
    while True:
        #get triangle size:
        myinput() # eat triangle size statement
        n = int(myinput())
        # get/eat triangle instance:
        for i in range(n+1):
            myinput() # eat triangle-instance statement + n rows
        # get triangle array:
        myinput() # eat triangle array statement
        t = eval(myinput())
        # get triangle path:
        myinput() # eat path statement
        path = myinput().strip()
        # give your answer:
        myinput() # eat prompt
        print(calculate_path(t,path))
    exit(0)


# EVAL BEST SOL
if argv[1] == "3":
    while True:
        #get triangle size:
        myinput() # eat triangle size statement
        n = int(myinput())
        # get/eat triangle instance:
        for i in range(n+1):
            myinput() # eat triangle-instance statement + n rows
        # get triangle:
        myinput() # eat triangle array statement
        triangle = eval(myinput())
        # give your answer:
        myinput() # eat prompt
        print(best_path_cost(triangle))
    exit(0)

# EVAL NUMBER OF TRIANGLES IN TRIANGLE
if argv[1] == "4":
    while True:
        # get small triangle size:
        myinput() # eat small triangle size statement
        l = int(myinput())
        # get big triangle size:
        myinput() # eat big triangle size statement
        L = int(myinput())
        # get small triangle array: 
        myinput() # eat small triangle array statement
        small_array = eval(myinput())
        # get big triangle array: 
        myinput() # eat big triangle array statement
        big_array = eval(myinput())
        # give your answer:
        myinput() # eat prompt
        answer = 0
        livello = 1
        indexes = []
        for i in range(int(((L-l+1)*(L-l+2))/2)):   
            if i >= livello*(livello+1)/2:
                livello +=1
            if big_array[i] == small_array[0]:
                if fits(i,livello,big_array,small_array,l)[0]:
                    indexes.append(fits(i,livello,big_array,small_array,l)[1])
                    answer += 1
        print(answer)
    exit(0)

