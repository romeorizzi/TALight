#!/usr/bin/env python3

from sys import stderr, exit

import collections
import random

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('code_lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

x = random.randint(1, 4)

graph,circuit,error = certificateEYC (x)

print(graph)
print("\n")
print(circuit)
answer = input()

if answer == error:
    TAc.print("\nCORRETTO", "green")
else:
    TAc.print("\nSBAGLIATO", "red")

exit(0)
