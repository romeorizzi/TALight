#!/usr/bin/env python3

# "This service will check your statement that a directed graph you provide us is Eulerian"

from sys import stderr, exit, argv

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="euler-dir"
service="check_is_eulerian"
args_list = [
    ('graph',str),
    ('n',str), 
    ('m',str),
    ('eulerian',str),
    ('goal',str),
    ('feedback',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

if ENV['graph'] == '1':
    TAc.print("\nGrafo esempio 1 --- da fare")

if ENV['graph'] == '2':
    TAc.print("\nGrafo esempio 2 --- da fare")

if ENV['n'] == 'lazy':
    TAc.print("\nInserisci il numero di nodi presenti nel grafo:\n","green")
    n = int(input())
    g = Graph(n)

    if ENV['m'] == 'lazy':
        TAc.print("\nInserisci il numero di nodi presenti nel grafo:\n","green")
        m = int(input())

    TAc.print("\nInserisci gli archi indicando nodo di partenza e fine separati da uno spazio (es:0 1):\n","green")
    for i in range(m):
         head, end = input().split()
         g.addEdge(int(head), int(end))
  

if g.isEulerianCycle():
    if ENV['eulerian'] == "yes":
        TAc.print("\n\nESATTO, il grafo contiene un ciclo euleriano\n","green")
       
    else:
        TAc.print("\n\nSBAGLIATO, il grafo contiene un ciclo euleriano\n","red")
        
else:
    if ENV['eulerian'] == "no":
        TAc.print("\n\nESATTO, il grafo NON contiene un ciclo euleriano\n","green")
        
    else:
        TAc.print("\n\nSBAGLIATO, il grafo NON contiene un ciclo euleriano\n","red")
       
