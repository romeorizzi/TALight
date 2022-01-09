#!/usr/bin/python
from sys import stderr, exit, argv
import random

usage=f"""I am bot that provides a feasible path for every instance (in an infinite loop).
"""

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
    # give your answer:
    myinput() # eat prompt
    directions = ['L','R']
    answer = "".join(random.choices(directions,k=n-1))
    print(answer)
exit(0)
