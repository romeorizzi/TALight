#!/usr/bin/env python3

from sys import stderr, exit
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
from bot_interface import service_server_to_send_files

from pirellone_lib import gen_pirellone



# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="gimme_instance"
args_list = [
    ('input_mode',str),
    ('m',int),
    ('n',int),
    ('seed',int),
    ('instance_solvability',str),
    ('silent',bool),
    # ('display',bool),
    # ('download',bool),
    ('lang',str),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Adjust solvability param
if ENV['instance_solvability'] == 'solvable':
    solvable = True
elif ENV['instance_solvability'] == 'unsolvable':
    solvable = False
else:
    solvable = None

# get pirellone
try:
    (instance, seed) = gen_pirellone(ENV['m'], ENV['n'], ENV['seed'], solvable)
except RuntimeError:
    TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
    exit(0)

# display the instance
if ENV['display']:
    TAc.print(LANG.render_feedback("display", f"The matrix {ENV['m']}x{ENV['n']} is:"), "white", ["bold"])
    for row in instance:
        TAc.print(LANG.render_feedback("display_row", f"{row}"), "white", ["bold"])

# save the instance to file
if ENV['download']:
    dict_of_files = { f"seq_n{n}.txt": " ".join(map(str,range(n))).encode('ascii')  for n in [10, 20, 30] }
    service_server_to_send_files(dict_of_files)

    print(dict_of_files['seq_n10.txt'].decode())   # to get on of the files in clear

    
    TAc.print(LANG.render_feedback("todo", f"TODO"), "red", ["bold"])


# printing seed
TAc.print(LANG.render_feedback("seed", f"The seed is: {seed}"), "yellow", ["bold"])
# if seed % 3 != 0:
#     TAc.print(LANG.render_feedback("spoiler", f"This is a solvable seed"), "green", ["bold"])
# else:
#     TAc.print(LANG.render_feedback("spoiler", f"This is a unsolvable seed"), "red", ["bold"])

exit(0)