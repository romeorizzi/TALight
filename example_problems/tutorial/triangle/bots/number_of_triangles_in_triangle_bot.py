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
    # get triangle size:
    myinput() # eat triangle size statement
    sizes = eval(myinput()) 
    l = sizes[0]
    L = sizes[1]
    # get triangle arrays: 
    myinput() # eat triangle arrays statement
    arrays = eval(myinput())   
    small_array = arrays[0]
    big_array = arrays[1]
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
    myinput()
exit(0)
