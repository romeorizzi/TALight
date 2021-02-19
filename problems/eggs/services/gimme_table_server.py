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
messages_book = select_book_and_lang("gimme_table_server", ENV_lang)
        
def print_lang(msg_code, *msg_rendering, **kwargs):
    msg_text=eval(f"f'{messages_book[msg_code]}'")
    TAcprint(msg_text, *msg_rendering, **kwargs)


        

print_lang("open-channel", "green")        
#English: print(f"# I will serve: problem=eggs, service=gimme_table, n_eggs={ENV_n_eggs}, n_floors={ENV_n_floors}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

#print(f"# I will serve: problem=eggs, service=gimme_table, n_eggs={ENV_n_eggs}, n_floors={ENV_n_floors}, lang={ENV_lang}.")

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

# PRINTING OUT THE TABLE:
fmt = f"%{1+len(str(table[-1][-1]))}d"
for row in table[1:]:
    for ele in row[1:]:
        print(fmt % ele, end=" ")
    print()    
exit(0)
