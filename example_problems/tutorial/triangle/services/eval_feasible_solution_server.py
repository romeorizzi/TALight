#!/usr/bin/env python3
from sys import stderr, exit
import random
import math
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('goal',str),
    ('code_lang',str),
]


ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# GENERATE INSTANCES

instances = []
MAX_ROWS = 10
NUM_OF_INSTANCES = 100
#EFFICIENT
if ENV["goal"] == "efficient":
    MAX_ROWS *= 5
    NUM_OF_INSTANCES *=5
    if ENV["code_lang"] == "compiled":
        MAX_ROWS *= 2
    scaling_factor = 1.3
    n = 1
    for _ in range(NUM_OF_INSTANCES):
        seed = random.randint(100000,999999)
        instances.append(tl.random_triangle(n, 0, 99, seed, TAc, LANG))
        n = math.ceil(n*scaling_factor)
        if n>MAX_ROWS:
            n = MAX_ROWS
#NOT EFFICIENT
else:
    if ENV["code_lang"] == "compiled":
        MAX_ROWS *= 2
    scaling_factor = 1.3
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

def is_feasible_solution(path):                  
    for el in path:           
        if el != "R" and el != "L":
            return False
    return True 
    
########################################### METODO LINEARE PER TESTARE ######################
########################################### POI VA ELIMINATO ################################    
def feasible_solution(triangle):                 ############################################
    random_path = ""                             ############################################
    directions = ["R","L"]                       ############################################
    for _ in range(len(triangle)-1):             ############################################
        random_path += random.choice(directions) ############################################
    return random_path                           ############################################
#############################################################################################  
#############################################################################################  
         
for triangle in instances:
    start = monotonic() 
    p = input() 
    end = monotonic()
    time += end-start
    if !right_length(instance,p):
        TAc.NO()
        if len(p) < len(instance) -1:
            TAc.print(LANG.render_feedback("no-way-short", f'{p} is not a feasible solution, as it is too short.'), "red")
        else:
            TAc.print(LANG.render_feedback("no-way-long", f'{p} is not a feasible solution, as it is too long.'), "red")
        exit(0)
    if !is_feasible_solution(p):
        TAc.NO()
        TAc.print(LANG.render_feedback("no-way-wrong-directions", f'{p} is not a feasible solution, as it contains directions different from "L" or "R".'), "red")
    print(f'Correct! [took {time} seconds on your machine]')
    if time > 50:
        TAc.OK()
        TAc.print(LANG.render_feedback("seems-correct-weak", f'Your solution answers correctly on a first set of instances, but it took too much to answer to the last instance.'), "green")
        exit(0)

TAc.OK()
TAc.print(LANG.render_feedback("seems-correct-strong", f'Your solution appears to be correct (checked on several instances).'), "green")
if ENV["goal"] == "efficient":
    TAc.OK()
    TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is {ENV["goal"]}: its running time is linear in the length of T and S.'), "green")
 
exit(0)
