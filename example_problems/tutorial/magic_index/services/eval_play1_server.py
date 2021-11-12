#!/usr/bin/env python3
from sys import stderr, exit
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('config',str),
    ('moves',str),
    ('goal',str),
    ('feedback',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
final_configuration = ENV['config'].split(',')
indexes = ENV['moves'].split(',')

vector_len = len(final_configuration)

# this vector contains -1,0,1 and it's filled by the server with the worst case scenario and it's never shown to the user during the game.
server_vector = [None] * vector_len

# this variable contains the questions made by the user during the game
wasted_dollars = 0

# this boolean variable is initialized to True in case ENV['feedback'] == 'spot_first_gift'
firstGift = True

TAc.print(LANG.render_feedback("random_vector", f'All right, let us evaluate your moves...'), "yellow", ["bold"])


for n_move in range(0,len(final_configuration)):
    chosen_index = int(indexes[n_move])
   
    if '0' not in server_vector:
        unknown, optimal_pos = get_positions_f(server_vector)

        if chosen_index != optimal_pos:
            if ENV['feedback'] == 'spot_first_gift' and firstGift:
                TAc.print(LANG.render_feedback("first error", f'# Here you made your first mistake!'), "yellow", ["bold"])
                firstGift = False
            elif ENV['feedback'] == 'spot_every_gift':
                TAc.print(LANG.render_feedback("error", f'# Here you made a mistake!'), "yellow", ["bold"])
        
    else:
        unknown, optimal_pos = get_positions_g(server_vector)

        if chosen_index not in optimal_pos:
            if ENV['feedback'] == 'spot_first_gift' and firstGift:
                TAc.print(LANG.render_feedback("first error", f'# Here you made your first mistake!'), "yellow", ["bold"])
                firstGift = False
            elif ENV['feedback'] == 'spot_every_gift':
                TAc.print(LANG.render_feedback("error", f'# Here you made a mistake!'), "yellow", ["bold"])

    if final_configuration[chosen_index] == chosen_index:
        server_vector[optimal_pos] = '0' 
    elif final_configuration[chosen_index] > chosen_index:
        server_vector[optimal_pos] = '1'
    elif final_configuration[chosen_index] < chosen_index:
        server_vector[optimal_pos] = '-1'

    wasted_dollars += 1


min_questions = f(vector_len)
check_goal_eval(ENV['goal'], ENV['feedback'],wasted_dollars, min_questions, TAc, LANG)

