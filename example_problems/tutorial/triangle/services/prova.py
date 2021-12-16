from sys import stderr, exit
import random
import math
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

TAc = "porcodio"
LANG ="veneto diocan"

instances = []
MAX_ROWS = 10
NUM_OF_INSTANCES = 100
kind = input(" 'e' = efficient, 'ne' = not efficient\n")
#EFFICIENT
if kind == "e":
    MAX_ROWS *= 5
    NUM_OF_INSTANCES *=5
    
    lang = input(" 'c' = compiled, 'nc' = not compiled\n")
    if lang == "c":
        MAX_ROWS *= 2
    scaling_factor = 1.2
    n = 1
    for _ in range(NUM_OF_INSTANCES):
        seed = random.randint(100000,999999)
        instances.append(tl.random_triangle(n, 0, 99, seed, TAc, LANG))
        n = math.ceil(n*scaling_factor)
        if n>MAX_ROWS:
            n = MAX_ROWS
#NOT EFFICIENT
else:
    lang = input(" 'c' = compiled, 'nc' = not compiled")
    if lang == "c":
        MAX_ROWS *= 2
    scaling_factor = 1.2
    n = 1
    for _ in range(NUM_OF_INSTANCES):
        seed = random.randint(100000,999999)
        instances.append(tl.random_triangle(n, 0, 99, seed, TAc, LANG))
        n = math.ceil(n*scaling_factor)
        if n>MAX_ROWS:
            n = MAX_ROWS
            
def right_length(instance,answer):
    if len(instance) == len(answer)+1:
        return True
    return False
    
def feasible_solution(triangle):
    random_path = ""
    directions = ["R","L"]
    for _ in range(len(triangle)-1):
        random_path += random.choice(directions)
    return random_path
              
t = 0
for triangle in instances:
    start = monotonic() 
    p = feasible_solution(triangle)   
    end = monotonic()
    t += end-start
print("Your code took " + str(t) + " seconds to return all the solutions")

