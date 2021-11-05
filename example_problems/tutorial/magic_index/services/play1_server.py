#!/usr/bin/env python3
from sys import stderr, exit
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('n',str),
    ('opponent',str),
    ('goal',str),
    ('feedback',str),
]
ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
vector_len = int(ENV['n'])

# this vector contains -1,0,1 and it's filled by the server with the worst case scenario and it's never shown to the user during the game.
server_vector = [None] * vector_len

# this variable contains the questions made by the user during the game
wasted_dollars = 0

# this is the vector discovered/generated during the game
discovered_vec = ['?' for _ in range(1, vector_len+1)] # print vector

# this boolean variable is initialized to True in case ENV['feedback'] == 'spot_first_gift'
firstGift = True

TAc.print(LANG.render_feedback("random_vector", f'All right, let us play on a vector of size: {vector_len}.'), "yellow", ["bold"])
print_vector(discovered_vec, TAc, LANG)

while True:
    TAc.print(LANG.render_feedback("random_vector", f'Choose an index to play:'), "yellow", ["bold"])
    chosen_index = TALinput(str, num_tokens=1, regex="^(0|[1-9][0-9]{0,5})$", regex_explained="Enter an index to discover the vector value", TAc=TAc, LANG=None)
    chosen_index = int(chosen_index[0])

    if chosen_index >= vector_len:
        TAc.print(LANG.render_feedback("error", f'The input value for the index is not between 0 and {vector_len-1}. Insert another index to play:'), "red", ["bold"])
    else:
        if ENV['opponent'] == 'optimal':
            if '0' not in server_vector:
                unknown, optimal_pos = get_positions_f(server_vector)
                if chosen_index == optimal_pos:
                    # we want to know which is the value to insert in server_vector[optimal_pos]
                    # we take the value computed in the function f, taking the greatest key of the dictionary and the corresponding value
                    _ = f(unknown)
                    server_vector[optimal_pos] = worst_f[max(worst_f)]
                    #and we clean the support dictionary
                    cleanWorst_f()
                    
                    # we generate the value for the discovered_vec based on the just computed value in f()
                    discovered_vec[chosen_index] = generate_value_for_vector(server_vector, discovered_vec, chosen_index) 


       
            print_vector(discovered_vec, TAc, LANG)
            
            # check if the user is playing (optimally) according to the chosen level
            if ENV['feedback'] == 'spot_first_gift' and firstGift:
                if vector_optmal_questions[n] != vector_questions[n]:
                    TAc.print(LANG.render_feedback("first error", f'# Here you made your first mistake!'), "yellow", ["bold"])
                    firstGift = False
            elif ENV['feedback'] == 'spot_every_gift':
                if vector_optmal_questions[n] != vector_questions[n]:
                    TAc.print(LANG.render_feedback("error", f'# Here you made a mistake!'), "yellow", ["bold"])

            wasted_dollars += 1

            # we ask if the user wants to try to give the solution
            TAc.print(LANG.render_feedback("solution proposed", f'Do you want to give the solution? (y for yes, otherwise any other character)'), "yellow", ["bold"])
            ans = TALinput(str, num_tokens=1, regex_explained="enter y if you want submit your solution, otherwise any other character", TAc=TAc, LANG=None)
            
            if ans[0].lower() == 'y':
                TAc.print(LANG.render_feedback("solution proposed", f'Enter your vector of magic indexes here: (example: 1,2,3)'), "yellow", ["bold"])
                user_solution = TALinput(str, num_tokens=1, regex="^((0|-{0,1}[1-9][0-9]{0,3})(,(0|-{0,1}[1-9][0-9]{0,3})){0,1000})|e$", regex_explained="regex for magic indexes provided by the user", TAc=TAc, LANG=None)
                user_solution = user_solution[0].split(',')

                if user_solution != ['e']:
                    user_solution = list(map(int, user_solution))
                    check_input_vector(user_solution, TAc, LANG)

                check_goal(ENV['opponent'], ENV['goal'], ENV['feedback'], magic_indexes, user_solution, vector_optmal_questions, vector_questions, wasted_dollars, min_questions, TAc, LANG)
            else:
               TAc.print(LANG.render_feedback("the game continues", f'Perfect! Let us keep playing, you have done {wasted_dollars} questions so far...'), "yellow", ["bold"])
        
        elif ENV['opponent'] == 'random':
            print()


#TODO: chiedere di controllare il discorso della chiusura del server(?) se non arriva input da linea di comando dopo un tot.