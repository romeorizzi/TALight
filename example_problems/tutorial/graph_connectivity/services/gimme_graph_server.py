#!/usr/bin/env python3
import random 
from re import M
from sys import stderr, exit

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="graph_connectivity"
service="gimme_a_graph"
args_list = [
    ('input_mode',str),
    ('n',int), 
    ('m',int), 
    ('seed',str),
    ('graph_connectivity',str), 
    ('display',str),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
#TAc.print(LANG.opening_msg, "green")

# Input mode
input_mode = ENV['input_mode']
if input_mode == "random":
    seed = random.randrange(10000,80000)
else:
    seed = int(input_mode)

graph_connectivity = ENV['graph_connectivity']

# Connected/disconnected/surprise
if graph_connectivity == "surprise_me":
    is_connected = bool(random.randint(0,1))
elif graph_connectivity == "connected":
    is_connected = True
else:
    is_connected = False


# Check n e m

n = ENV['n']
m = ENV['m']
if n < 1:
    TAc.print(LANG.render_feedback("n-LB", f'# ERRORE: il numero di nodi del grafo deve essere almeno 1. Invece il primo dei numeri che hai inserito è n={n}.'), "red")
    exit(0)
if m < 0:
    TAc.print(LANG.render_feedback("m-LB", f'# ERRORE: il numero di archi del grafo non può essere negativo. Invece il secondo dei numeri che hai inserito è m={m}.'), "red")
    exit(0)
if n > 1000:
    TAc.print(LANG.render_feedback("n-UB", f'# ERRORE: il numero di nodi del grafo non può eccedere 1000. Invece il primo dei numeri che hai inserito è n={n}.'), "red")
    exit(0)
if m > 10000:
    TAc.print(LANG.render_feedback("m-UB", f'# ERRORE: il numero di archi del grafo non può eccedere 10000. Invece il secondo dei numeri che hai inserito è m={m}.'), "red")
    exit(0)


g, graph_print, edges, seed = GenerateGraph(seed, n, m, is_connected)

print("#start:")
print(f"# The assigned instance is:\n#   number of nodes: {n}\n#   number of arcs: {m}\n#   Seed: {seed}\n", end="")

print("graph:")
print(graph_print)