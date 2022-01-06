#!/usr/bin/python
from sys import stderr, exit, argv
import random

usage=f"""I am bot that provides the correct answer for every service (in an infinite loop).
I will serve the following services:

1. feasible_path
2. reward_sol
3. opt_sol
4. num_triangles_in_triangle

E.G. rtal connect -e triangle eval_feasible_solution --bots/general_purpose_correct_bot.py feasible_path """

def myinput():
    spoon = ""
    while len(spoon) == 0 or spoon[0] == '#':
        spoon = input()
    return spoon

if len(argv) != 2:
    print("WARNING! Bot called with the wrong number of parameters.\n")
    print(usage)
    exit(0)

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
    answer = ""
    if argv[1]:
        for _ in range (n-1):
            answer += random.choice(directions)
        print(answer)
    else:
        for _ in range (n):
            answer += random.choice(directions)
        print(answer)
    myinput()
exit(0)
