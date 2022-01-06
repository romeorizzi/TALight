#!/usr/bin/python
from sys import stderr, exit, argv
import random

usage="""I am an efficient (linear time) bot that provides the reward for a feasible solution (path) in a given triangle."""

def myinput():
    spoon = ""
    while len(spoon) == 0 or spoon[0] == '#':
        spoon = input()
    return spoon

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

