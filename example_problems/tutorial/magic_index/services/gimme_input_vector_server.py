#!/usr/bin/env python3
from sys import stderr, exit, argv
import re,random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="magic_indexes"
service="gimme_input_vector_server"
args_list = [
    ('n', str),
    ('seed', str),
    ('lang', str),
    ('ISATTY', bool),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")
n=ENV['n']

# START CODING YOUR SERVICE:
if ENV['seed']=='random_seed': 
    vec,seed = random_vector(int(n))
else:
    vec,seed = random_vector(int(n),ENV['seed'])

vec = [str(e) for e in vec]
vec = ",".join(vec)
TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
TAc.print(LANG.render_feedback("vector generated:",f"{vec} "), "yellow", ["bold"])

