#!/usr/bin/env python3
from sys import stderr, exit
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from pirellone_lib import gen_pirellone



# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="gen_random_puzzle"
args_list = [
    ('m',int),
    ('n',int),
    ('instance_solvability', str),
    ('display', bool),
    ('download',bool),
    ('seed',int),
    ('lang',str),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Adjust solvability param
if ENV['instance_solvability'] == 'solvable':
    must_be_solvable = True
elif ENV['instance_solvability'] == 'unsolvable':
    must_be_solvable = False
else:
    must_be_solvable = random.choice([False, True])

# get pirellone
try:
    (instance, seed) = gen_pirellone(ENV['m'], ENV['n'], seed=ENV['seed'], solvable=must_be_solvable)
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
    TAc.print(LANG.render_feedback("todo", f"TODO"), "red", ["bold"])


# printing seed
TAc.print(LANG.render_feedback("seed", f"The seed is: {seed}"), "yellow", ["bold"])
# if seed % 3 != 0:
#     TAc.print(LANG.render_feedback("spoiler", f"This is a solvable seed"), "green", ["bold"])
# else:
#     TAc.print(LANG.render_feedback("spoiler", f"This is a unsolvable seed"), "red", ["bold"])

exit(0)