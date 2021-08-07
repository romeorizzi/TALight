#!/usr/bin/env python3

# "This service will check your statement that a directed graph you provide us is Eulerian"

from sys import stderr, exit

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
    ('sc_bool',bool),
    ('goal',str),
    ('lang',str),
    ('ISATTY',bool),
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

sc=ENV['sc_bool']
answer1=g.isSC()

if answer1==sc and sc==1:
    if ENV['goal'] == 'correct':
        if answer1==True:
            TAc.print("\n\nESATTO, il grafo e' fortemente connesso.\n","green") 
            exit(0)       
        else:
            TAc.print("\n\nSBAGLIATO, il grafo non è fortemente connesso.\n","red")
            exit(0)   

    if ENV['goal'] == 'with_certificate':
        if answer1 == False:
            TAc.print("\n\nIl grafo presenta piu' di una unica componente fortemente connessa percio' NON e' un grafo diretto fortemente connesso!\n","red")
            g.printSCCs()
            exit(0)
        if answer1==True:
            cfc = g.printSCCs()
            TAc.print(f"Following is the strongly connected components in given graph: {cfc}","yellow")
            exit(0)
else:
    if sc!=0:
        TAc.print("Il grafo non è fortemente connesso", "red")
        exit(0)


answer2=g.isSC()
if answer2==sc and sc==0:
    if ENV['goal'] == 'correct':
        if answer2==True:
            TAc.print("\n\nSBAGLIATO, il grafo e' fortemente connesso.\n","red")
            exit(0)
        else:
            TAc.print("\n\nESATTO, il grafo NON e' fortemente connesso.\n","green")
    if ENV['goal'] == 'with_certificate':
        if answer2 == False:
            cfc = g.printSCCs()
            TAc.print(f"\nIl grafo che hai sottomesso non e' fortemente connesso perchè non contiene un'unica componente fortemente connessa!\Ma tutte le seguenti: {cfc}","green")
            exit(0)
        if answer2==True:
            cfc = g.printSCCs()
            TAc.print(f"\nIl grafo e' fortemente connesso perchè contiene la sola componente: {cfc}\n","red")
            exit(0)
else:
    TAc.print("Il grafo inserito è fortemente connesso", "red")
    exit(0)