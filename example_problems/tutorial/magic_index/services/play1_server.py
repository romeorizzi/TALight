#!/usr/bin/env python3
from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="magic_indexes"
service="play1_server"
args_list = [
    #('n',str),
    ('opponent',str),
    ('goal',str),
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
size, vec = random_vector_worst_case()
wasted_dollars = 0
min_questions_worst_case = check_n_questions_worst_case(len(vec))
magic_indexes = spot_magic_index(vec)
vector_optmal_questions = generate_optimal_questions_order(vec)

discovered_vec = ['?' for _ in range(1, size+1)]
vector_questions = [None for i in range(1,len(vec)+1)]



TAc.print(LANG.render_feedback("random_vector", f'I generated a vector of size: {size}.'), "yellow", ["bold"])

while True:
    TAc.print(LANG.render_feedback("random_vector", f'Choose an index to play:'), "yellow", ["bold"])
    n = TALinput(str, num_tokens=1, regex="^(0|[1-9][0-9]{0,5})$", regex_explained="enter an index n to check the value at that position", TAc=TAc, LANG=None)
    n = int(n[0])
    if n >= size:
        TAc.print(LANG.render_feedback("error", f'The input value for the index is not between 0 and {size-1}. Insert another index to play:'), "red", ["bold"])
    else:
        discovered_vec[n] = vec[n]
        vector_questions[n] = wasted_dollars 
        print_vector(discovered_vec, TAc, LANG)
        #TAc.print(LANG.render_feedback("value", f'The corresponding value for the index requested is: {vec[n]}.'), "green", ["bold"])
        wasted_dollars += 1

        # check if the user is playing (optimally) according to the chosen level
        
    
    # we ask if the user wants to try to give the solution
    TAc.print(LANG.render_feedback("solution proposed", f'Do you want to give the solution? (y / n)'), "yellow", ["bold"])
    ans = TALinput(str, num_tokens=1, regex="^([y]*|[n]*)$", regex_explained="enter Y if you want submit your solution, otherwise N", TAc=TAc, LANG=None)
    if ans[0] == 'y':
        TAc.print(LANG.render_feedback("solution proposed", f'Enter your vector of magic indexes here: (example: 1,2,3)'), "yellow", ["bold"])
        user_solution = TALinput(str, num_tokens=1, regex="^((0|-{0,1}[1-9][0-9]{0,3})(,(0|-{0,1}[1-9][0-9]{0,3})){0,1000})$", regex_explained="regex for magic indexes provided by the user", TAc=TAc, LANG=None)
        user_solution = user_solution[0].split(',')
        user_solution = list(map(int, user_solution))
        check_input_vector(user_solution, TAc, LANG)


        # we give feedback based on the chosen optimality level
        isCorrect = magic_indexes == user_solution
        if ENV['goal'] == 'correct' and isCorrect:
            TAc.print(LANG.render_feedback(" correct solution!", f'Correct!'), "green", ["bold"])
            exit(0)
        else:
            TAc.print(LANG.render_feedback("wrong solution!", f'Wrong answer!'), "red", ["bold"])
            exit(0)

    else:
        TAc.print(LANG.render_feedback("the game continues", f'Perfect! Let us keep playing, you have done {wasted_dollars} questions so far...'), "yellow", ["bold"])



