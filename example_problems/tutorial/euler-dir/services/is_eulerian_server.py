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


if ENV['n'] == 'lazy' and ENV['m'] == 'lazy':
    n,m = input().split()
    n = int(n)
    m = int(m)
    
g = Graph(int(n))
    
adj = [ [] for _ in range(int(m))]

for i in range(int(m)):
         head, tail = input().split()
         if int(tail)>(n-1) or int(head)>(n-1) :
            TAc.print("\n# ERRORE: hai inserito un arco non può essere presente nel grafo!\n", "red")
            exit(0)

         g.addEdge(int(head),int(tail))
         adj[int(head)].append(int(tail))
  
answer = g.isEulerianCycle()

if ENV['goal'] == 'correct':
    if answer == True:
      TAc.print("\nESATTO, il grafo contiene un circuito euleriano!\n","green") 
      exit(0)       
    else:
      TAc.print("\nSBAGLIATO, il grafo NON contiene un circuito euleriano!\n","red")
      exit(0)   

if ENV['goal'] == 'with_certificate':
    if answer == False:
        TAc.print("\nIl grafo hai sottomesso non è euleriano, perciò non contiene un circuito euleriano!\n","red")
        exit(0)
    if answer == True:
        TAc.print("\nIl circuito è:\n","geen")
        printCircuit(adj)
        
        exit(0)

exit(0)