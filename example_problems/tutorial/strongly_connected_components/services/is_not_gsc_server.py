#!/usr/bin/env python3

# "This service will check your statement that a directed graph you provide us is not Eulerian"

from sys import stderr, exit, argv

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="strongly_connected_components"
service="check_is_not_gsc"
args_list = [
    ('n',str), 
    ('m',str),
    ('sc',str),
    ('goal',str),
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
adj = [ [] for _ in range(m)]

for i in range(m):
         head, tail = input().split()
         if (int(tail)>(n-1) or int(head)>(n-1)) :
            TAc.print("\n# ERRORE: hai inserito un arco che non può essere presente nel grafo!", "red")
            exit(0)

         g.addEdge(int(head), int(tail))
         adj[int(head)].append(int(tail))

if ENV['goal'] == 'correct':
    if g.isSC():
        TAc.print("\n\nSBAGLIATO, il grafo e' fortemente connesso.\n","red")
        exit(0)
    else:
        TAc.print("\n\nESATTO, il grafo NON e' fortemente connesso.\n","green")

if ENV['goal'] == 'with_certificate':
    if g.isSC() == False:
        TAc.print("\nIl grafo che hai sottomesso non e' fortemente connesso, percio' non contiene un'unica componente fortemente connessa!","red")
        g.printSCCs()
        exit(0)
    if g.isSC():
        TAc.print("\nIl grafo e' fortemente connesso perchè contiene la sola componente:\n","geen")
        g.printSCCs()

        exit(0)

exit(0)
