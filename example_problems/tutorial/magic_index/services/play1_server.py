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
TAc.print(LANG.render_feedback("random_vector", f'I generated a vector of size: {size}.'), "yellow", ["bold"])
wasted_dollars = 0


while True:
    TAc.print(LANG.render_feedback("random_vector", f'Choose an index to play:'), "yellow", ["bold"])
    n = TALinput(str, num_tokens=1, regex="^(0|[1-9][0-9]{0,5})$", regex_explained="enter an index n to check the value at that position", TAc=TAc, LANG=None)
    n = int(n[0])
    if n >= size:
        TAc.print(LANG.render_feedback("error", f'The input value for the index is not between 0 and {size-1}. Insert another index to play:'), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback("value", f'The corresponding value for the index requested is: {vec[n]}.'), "green", ["bold"])
        wasted_dollars += 1

# TODO: creare una variabile con le domande minime da farsi per trovare tutti i MI
# ad ogni ciclo chiediamo all'utente se sa quali sono i MI e se vuole inserirli o continuare a giocare.
# In base al goal che inserisce se ci da il vettore corretto di MI allora andiamo a vedere quante domande ha fatto:
# se goal "corretto" e lista MI giusta --> ok altrimenti no
# e analogamente per il resto. 
