#!/usr/bin/python
from sys import stderr, exit, argv
import random

usage="""I am an efficient (linear time) bot that checks whether a given candidate solution for a given triangle instance is indeed a feasible solution. This is the case if and only if the candidate solution is a string in {L,R}^n where n is the size of the assigned triangle."""

def myinput():
    spoon = ""
    while len(spoon) == 0 or spoon[0] == '#':
        spoon = input()
    return spoon

while True:
    # get triangle size:
    myinput() # eat triangle-size statement
    n = int(myinput())
    # get/eat triangle instance:
    for i in range(n+1):
        myinput() # eat triangle-instance statement + n rows
    # get triangle path:
    myinput() # eat path statement
    path = myinput().strip()
    # give your answer:
    myinput() # eat prompt
    good = True
    if len(path) != n-1:
        print(f"no # because a path from the only element in row 0 to any element in row n-1={n-1} should specify precisely n-1={n-1} directions. Therefore, we expected a string of length n-1={n-1}. Instead your string has length {len(path)}.")
        good = False
    else:
        for char in path:
            if char not in {'L','R'}:
                print("no # because a feasible path should specify each choice (whether to go left or right at every step desending the triangle). Therefore, a path is a string over the alphabet {L,R}. Instead, your string contains a '{cher} character.")
                good = False
                break
    if good:
        print('yes')
exit(0)

