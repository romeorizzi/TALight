#!/usr/bin/env python3

from os import environ
from sys import exit
from math import inf as IMPOSSIBLE

from multilanguage import *

ENV_lang = environ["TAL_lang"]
ENV_min = int(environ["TAL_min"])
ENV_n_eggs = int(environ["TAL_n_eggs"])
ENV_n_floors = int(environ["TAL_n_floors"])
ENV_colored_feedback = (environ["TAL_ISATTY"] == "1")

set_colors(ENV_colored_feedback)
messages_book = select_book_and_lang("confirm_min_throws_server", ENV_lang)
        
def render_feedback(msg_code, msg_English_rendition):
    if messages_book == None:
        return msg_English_rendition
    return eval(f"f'{messages_book[msg_code]}'")
        

TAcprint(render_feedback("open-channel", f"# I will serve: problem=eggs, service=confirm_min_throws, n_min={ENV_min}, n_eggs={ENV_n_eggs}, n_floors={ENV_n_floors}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}."), "green")        

# INITIALIZATON: allocation, base cases, sentinels
table = [ [0] + [IMPOSSIBLE] * ENV_n_floors ]
for u in range(ENV_n_eggs):
    table.append([0] + [None] * ENV_n_floors)

# INDUCTTVE STEP: the min-max recursion with nature playing against
for u in range(1,1+ENV_n_eggs):
    for f in range(1,1+ENV_n_floors):
        table[u][f] = IMPOSSIBLE
        best_launch_floor = None
        for first_launch_floor in range(1,1+f):
            if table[u][f] > 1+max(table[u][f-first_launch_floor],table[u-1][first_launch_floor-1]):
                best_launch_floor = first_launch_floor
                table[u][f] = 1+max(table[u][f-first_launch_floor],table[u-1][first_launch_floor-1])

print(f"When you are given {ENV_n_eggs} eggs and the floors are {ENV_n_floors} then there exists a policy that guarantees you to find out the truth in strictly less than {table[ENV_n_eggs][ENV_n_floors]} launches.\nThis is optimal.\nA possible first move for such an optimal strategy is to launch one egg from floor {best_launch_floor}.")

exit(0)
