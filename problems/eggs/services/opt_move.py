#!/usr/bin/env python3

from os import environ
from sys import exit
from math import inf as IMPOSSIBLE

from multilanguage import *

ENV_lang = environ["TAL_lang"]
ENV_n_eggs = int(environ["TAL_n_eggs"])
ENV_n_floors = int(environ["TAL_n_floors"])
ENV_colored_feedback = (environ["TAL_ISATTY"] == "1")

set_colors(ENV_colored_feedback)
messages_book = select_book_and_lang("opt_move_server", ENV_lang)
        
def print_lang(msg_code, *msg_rendering, **kwargs):
    msg_text=eval(f"f'{messages_book[msg_code]}'")
    TAcprint(msg_text, *msg_rendering, **kwargs)


        

print_lang("open-channel", "green")        
#English: print(f"# I will serve: problem=eggs, service=opt_move, n_eggs={ENV_n_eggs}, n_floors={ENV_n_floors}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

# INITIALIZATON: allocation, base cases, sentinels
table = [ [0] + [IMPOSSIBLE] * ENV_n_floors ]
for u in range(ENV_n_eggs):
    table.append([0] + [None] * ENV_n_floors)

# INDUCTTVE STEP: the min-max recursion with nature playing against
for u in range(1,1+ENV_n_eggs):
    for f in range(1,1+ENV_n_floors):
        table[u][f] = IMPOSSIBLE
        for first_launch_floor in range(1,1+f):
            table[u][f] = min(table[u][f],1+max(table[u][f-first_launch_floor],table[u-1][first_launch_floor-1]))

if table[ENV_n_eggs][ENV_n_floors] < ENV_min:
    print(f"No! When you are given {ENV_n_eggs} eggs and the floors are {ENV_n_floors} then there exists a policy that guarantees you to find out the truth in strictly less than {ENV_min} launches, whatever will happen (worst case).")
    #English:  print("No! When you are given {ENV_n_eggs} eggs and the floors are {ENV_n_floors} then there exists a policy that guarantees you to find out the truth in strictly less than {ENV_min} launches, whatever will happen (worst case).")
if table[ENV_n_eggs][ENV_n_floors] > ENV_min:
    print(f"No! When you are given {ENV_n_eggs} eggs and the floors are {ENV_n_floors} then no policy guarantees you to find out the truth within {ENV_min} launches in every possible scenario (aka, whathever the truth is).")
    #English: 
if table[ENV_n_eggs][ENV_n_floors] == ENV_min:
    print(f"Yes! Indeed, {ENV_min} is the smallest possibl natural B such that, when you are given {ENV_n_eggs} eggs and the floors are {ENV_n_floors}, still there exists a policy that guarantees you to find out the truth within B launches in every possible scenario.")
    #English: 
exit(0)
