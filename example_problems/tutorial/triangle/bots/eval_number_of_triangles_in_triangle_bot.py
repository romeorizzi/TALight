#!/usr/bin/python
from sys import stderr, exit, argv
import random

usage=f"""I am an efficient (linear time) bot that provides the number of occurencies of a triangle in another triangle (in an infinite loop)."""

def myinput():
    spoon = ""
    while len(spoon) == 0 or spoon[0] == '#':
        spoon = input()
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



             
             
               
             
             
             
             
             
             
             
             
             
