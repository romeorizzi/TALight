#!/usr/bin/env python3

# "This service will check your statement that a directed graph you provide us is Eulerian"

from sys import stderr, exit, argv

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# aggiorna meta.yaml

# METADATA OF THIS TAL_SERVICE:
problem="euler-dir"
service="gimme_scc"
args_list = [
    ('n',str), 
    ('m',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

if ENV['n'] == 'lazy':
    TAc.print('\n# Inserisci il numero di nodi presenti nel grafo:\n',"yellow")
    n = int(input())

g = Graph(n)
    

if ENV['m'] == 'lazy':
    TAc.print('\n\n# Inserisci il numero di archi presenti nel grafo:\n',"yellow")
    m = int(input())
adj = [ [] for _ in range(m)]

TAc.print("\n# Inserisci gli archi, ogni arco su una nuova riga, indicando nodo di partenza e fine separati da uno spazio (es:0 1).\nRicorda l'enumerazione dei nodi parte da zero!\n","yellow")
for i in range(m):
    head, tail = input().split()
    if int(tail)>(n-1) or int(head)>(n-1) :
        TAc.print("\n# ERRORE: hai inserito un arco che non può essere presente nel grafo!", "red")
        exit(0)

    g.addEdge(int(head),int(tail))
    adj[int(head)].append(int(tail))

print ("Following are strongly connected components in given graph")
g.printSCCs()