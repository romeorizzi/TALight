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
    ('feedback',str)
]
ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
vector_len = int(ENV['n'])

# this vector contains -1,0,1 and it's filled by the server during the game.
server_vector = [None] * vector_len

# this variable contains the questions made by the server during the game
wasted_dollars = 0

# this is the vector discovered/generated during the game
discovered_vec = ['?' for _ in range(1, vector_len+1)] # print vector
TAc.print(LANG.render_feedback("random_vector", f'All right, let us play on a vector of size {vector_len}.'), "white", ["bold"])
no_more_opt_pos = False
g = False

while no_more_opt_pos == False:
    if '0' not in server_vector:
        unknown, optimal_pos = get_positions_f(server_vector)
    else:
        unknown, optimal_pos = get_positions_g(server_vector)
        g = True

    if g:
        if optimal_pos[0] == None and optimal_pos[1] == None:
            no_more_opt_pos = True

            if '0' in server_vector:
                magic_indexes = [i for i in range(server_vector.index('0'), (len(server_vector)-1) - server_vector[::-1].index('0')+1)]
                TAc.print(LANG.render_feedback("move", f'Perfect I don\'t need any more questions. The magic indexes are: {magic_indexes}.'), "green", ["bold"])
            else:
                magic_indexes = []
                TAc.print(LANG.render_feedback("move", f'Perfect I don\'t need any more questions. There are no magic indexes.'), "green", ["bold"])

            
            TAc.print(LANG.render_feedback("moves done", f'I have done {wasted_dollars} questions.'), "green", ["bold"])
            exit(0)

        elif optimal_pos[0] == None:
            optimal_pos = optimal_pos[1]
        elif optimal_pos[1] == None:
            optimal_pos = optimal_pos[0]
        else:
            optimal_pos = random.choice(optimal_pos)

    TAc.print(LANG.render_feedback("move", f'My move is on position: {optimal_pos}.'), "yellow", ["bold"])
    wasted_dollars += 1
    TAc.print(LANG.render_feedback("what's the value", f'What is the value at that position?'), "yellow", ["bold"])
    ans = TALinput(str, num_tokens=1, regex_explained="enter the value", TAc=TAc, LANG=None)
    ans = int(ans[0])

    discovered_vec[optimal_pos] = ans
    server_vector = update_server_vec(optimal_pos, ans, server_vector)
    correct_ans = check_ans(server_vector, optimal_pos)

    if not correct_ans:
        TAc.print(LANG.render_feedback("value not valid", f'Mmm... seems impossible that at index {optimal_pos} there is a {ans}. Check your value!'), "red", ["bold"])
        server_vector[optimal_pos] = None
        discovered_vec[optimal_pos] = '?'
        wasted_dollars -= 1


    TAc.print(LANG.render_feedback("situation", f'ok, so the situation now is: '), "yellow", ["bold"])
    print_vector(discovered_vec, TAc, LANG)
    
   
    