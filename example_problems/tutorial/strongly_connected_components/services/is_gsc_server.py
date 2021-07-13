#!/usr/bin/env python3

# "This service will check your statement that a directed graph you provide us is Eulerian"

from sys import stderr, exit, argv

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="strongly_connected_components"
service="check_is_gsc"
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

# START CODING YOUR SERVICE:
print(f"#? waiting for your directed graph.\nFormat: each line two numbers separated by space. Then follow m lines, one for each arc, each with two numbers in the interval [0,n). These specify the tail node and the head node of the arc, in this order.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")
n, m = TALinput(int, 2, TAc=TAc)
if n < 1:
    TAc.print(LANG.render_feedback("n-LB", f"# ERRORE: il numero di nodi del grafo deve essere almeno 1. Invece il primo dei numeri che hai inserito è n={n}."), "red")
    exit(0)
if m < 0:
    TAc.print(LANG.render_feedback("m-LB", f"# ERRORE: il numero di archi del grafo non può essere negativo. Invece il secondo dei numeri che hai inserito è m={m}."), "red")
    exit(0)
g = Graph(int(n))

for i in range(m):
     head, tail = TALinput(int, 2, TAc=TAc)
     if tail >= n or head >= n or tail < 0 or head < 0:
        TAc.print(LANG.render_feedback("n-at-least-1", f"# ERRORE: entrambi gli estremi di un arco devono essere nodi del grafo, ossia numeri interi ricompresi nell'intervallo [0,{ENV['MAXN']}."), "red")
        exit(0)

     g.addEdge(int(head),int(tail))



if ENV['goal'] == 'correct':
    if g.isSC():
      TAc.print("\n\nESATTO, il grafo e' fortemente connesso.\n","green") 
      exit(0)       
    else:
      TAc.print("\n\nSBAGLIATO, il grafo non è fortemente connesso.\n","red")
      exit(0)   

if ENV['goal'] == 'with_certificate':
    if g.isSC() == False:
        TAc.print("\n\nIl grafo presenta piu' di una unica componente fortemente connessa percio' NON e' un grafo diretto fortemente connesso!\n","red")
        g.printSCCs()
        exit(0)
    if g.isSC():
        cfc = g.printSCCs()
        TAc.print(f"Following is the strongly connected components in given graph: {cfc}","yellow")
        exit(0)

exit(0)