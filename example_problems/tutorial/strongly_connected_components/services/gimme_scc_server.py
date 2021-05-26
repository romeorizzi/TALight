#!/usr/bin/env python3

# "This service will check your statement that a directed graph you provide us is Eulerian"

from sys import stderr, exit, argv

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# aggiorna meta.yaml

# METADATA OF THIS TAL_SERVICE:
problem="strongly_connected_components"
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


if ENV['n'] == 'lazy' and ENV['m'] == 'lazy':
    n,m = input().split()
    n = int(n)
    m = int(m)

g = Graph(n)

for i in range(m):
         head, tail = input().split()
         if (int(tail)>(n-1) or int(head)>(n-1)) :
            TAc.print("\n# ERRORE: hai inserito un arco non può essere presente nel grafo!", "red")
            exit(0)

         g.addEdge(int(head),int(tail))

cfc = g.printSCCs()
print (f"Following are strongly connected components in given graph: {cfc}")