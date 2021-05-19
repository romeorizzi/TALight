#!/usr/bin/env python3
from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="magic_indexes"
service="spot_magic_indexes_server"
args_list = [
    ('input_vector',str),
    ('lang',str),
    ('ISATTY',bool),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
if ENV['input_vector'] == 'lazy_input':
    TAc.print("\n#Enter an increasing sequence of integer values separated by commas (no spaces). This will be your <input_vector> (example: -12,0,34,56). You will be returned the sorted list of magic indexes for this vector.", "green")
    TAc.print("\n#Insert your input vector:", "green")
    vec = TALinput(str, num_tokens=1, regex="^(lazy|(0|-{0,1}[1-9][0-9]{0,3})(,(0|-{0,1}[1-9][0-9]{0,3})){0,1000})$", regex_explained="enter a sorted vector of distinct integer numbers separated by commas (example: -12,0,34,56)", TAc=TAc, LANG=None)
    vec = vec[0].split(',')
else:
    vec = ENV['input_vector'].split(',')
vec = list(map(int, vec))
check_input_vector(vec, TAc, LANG)

TAc.print("[", "yellow", end="")
got_one = False
for i in range(len(vec)):
  if vec[i] == i:
      if not got_one:
          got_one = True
          TAc.print(f"{i}", "yellow", end="")
      else:
          TAc.print(f", {i}", "yellow", end="")          
TAc.print("]", "yellow")
exit(0)

