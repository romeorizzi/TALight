#!/usr/bin/python
from sys import stderr, exit, argv
import random
import time

usage="""I am an efficient (linear time) bot that provides the maximum collectable reward in a triangle."""

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
count = 0
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

