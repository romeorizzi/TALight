#!/usr/bin/env python3

from sys import stderr, exit, argv

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# aggiorna meta.yaml
# METADATA OF THIS TAL_SERVICE:
problem="strongly_connected_components"
service="eval_find_scc"
args_list = [
    ('code_lang',str),
    ('goal',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

g, graph, edges , m = GenerateGraph()
cfc = g.printSCCs()

PS_answer = input()

if PS_answer == cfc:
    TAc.print("\nCORRETTO!","green")
if PS_answer != cfc:
    TAc.print("\nSBAGLIATO!","red")
