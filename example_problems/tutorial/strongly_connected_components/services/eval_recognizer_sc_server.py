#!/usr/bin/env python3

# This service will check if given a directed graph, you can decide whether it is Eulerian? And can you do it efficiently?

from sys import stderr, exit

import collections
import random
from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="strongly_connected_components"
service="eval_gsc"
args_list = [
    ('code_lang',str),
    ('goal',str),
    ('lang',str),
    ('seed',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

seed = ENV['seed']
g, graph, edges , m, a = GenerateGraph(seed)
TAc.print(f"\nSeed dell'istanza: {a}\n", "yellow")
true_answer = g.isSC()

TAc.print(f"{graph}", "yellow")

PS_answer = input()

if PS_answer == 'Y' or PS_answer == 'y':
    PS_answer = "yes"
if PS_answer == 'N' or PS_answer == 'n':
    PS_answer = "no"
if PS_answer!= 'yes' and PS_answer!='no':
    TAc.print("Input non valido, scrivere Y/y o N/n\n","red")
    exit(0)

if true_answer == False:    
    if PS_answer == 'yes':
        TAc.print("\nSBAGLIATO, il grafo non è fortemente connesso!\n","red")
    if PS_answer == 'no':
        TAc.print(f"\nRISPOSTA CORRETTA!\n", "green")

if true_answer == True:
    if PS_answer == 'yes':
        TAc.print(f"\nRISPOSTA CORRETTA!\n", "green")
    if PS_answer == 'no':
        TAc.print("\nSBAGLIATO, il grafo è fortemente connesso!\n","red")
    
exit(0)
