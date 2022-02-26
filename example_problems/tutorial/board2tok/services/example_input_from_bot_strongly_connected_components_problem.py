#!/usr/bin/env python3

# "This service checks your statement that a directed graph you provide us is (or is not) strongly connected"

from sys import stderr, exit

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from bot_file_exchange_sym_interface import service_server_requires_and_gets_file

from scc_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="strongly_connected_components"
service="check_is_gsc"
args_list = [
    ('sc_bool',bool),
    ('input_mode',str),
    ('goal',str),
    ('feedback',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if ENV['input_mode'] == 'from_terminal':
    TAc.print(LANG.render_feedback("waiting", f"#? waiting for your directed graph.\nFormat: each line two numbers separated by space. In the first line these are the number of nodes n and the number of arcs m, respectively. Then follow m lines, one for each arc, each with two numbers in the interval [0,n). These specify the tail node and the head node of the arc, in this order.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself."), "yellow")
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
            TAc.print(LANG.render_feedback("node-label-out-of-range", f"# ERRORE alla linea {i} dove (tail,head)=({tail},{head}): entrambi gli estremi di un arco devono essere nodi del grafo, ossia numeri interi ricompresi nell'intervallo [0,{n-1}]."), "red")
            exit(0)
         g.addEdge(int(head),int(tail))
else:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file (handler `graph.txt`)."), "yellow")
    graph=service_server_requires_and_gets_file('graph.txt').decode()
    lines=graph.splitlines()
    n , m = map(int,lines[0].split())
    if n < 1:
        TAc.print(LANG.render_feedback("n-LB", f"# ERRORE: il numero di nodi del grafo deve essere almeno 1. Invece il primo dei numeri che hai inserito è n={n}."), "red")
        exit(0)
    if m < 0:
        TAc.print(LANG.render_feedback("m-LB", f"# ERRORE: il numero di archi del grafo non può essere negativo. Invece il secondo dei numeri che hai inserito è m={m}."), "red")
        exit(0)
    g = Graph(int(n))
    for i in range(1,1+m):
         head, tail = map(int,lines[i].split())
         if tail >= n or head >= n or tail < 0 or head < 0:
            TAc.print(LANG.render_feedback("node-label-out-of-range", f"# ERRORE alla linea {i} dove (tail,head)=({tail},{head}): entrambi gli estremi di un arco devono essere nodi del grafo, ossia numeri interi ricompresi nell'intervallo [0,{n-1}]."), "red")
            exit(0)
         g.addEdge(int(head),int(tail))

g_is_sc_bool=g.isSC()
SCCs = g.printSCCs()
sink_scc = ",".join(map(str,SCCs[-1]))

if g_is_sc_bool != ENV['sc_bool']:
    if g_is_sc_bool:
        TAc.print("\nNo. Il grafo è fortemente connesso, ciò è contrario a quanto hai asserito.", "red")
        if ENV['feedback'] == 'gimme_your_certificate':
            TAc.print("\nPer convincere che è fortemente connesso potrei dare una ear-decomposition del grafo. FEATURE ANCORA DA IMPLEMENTARE!\n","yellow")
    else:
        TAc.print("\nNo. Il grafo non è fortemente connesso, ciò è contrario a quanto hai asserito.", "red")
        if ENV['feedback'] == 'gimme_your_certificate':
            TAc.print(f"\nInfatti non vi è alcun arco che ti consenta di uscire da questo insieme di nodi: {sink_scc}\n","yellow")
else:
    if ENV['feedback'] != 'silent':
        if g_is_sc_bool==True:
            TAc.print("\nOk, il grafo e' fortemente connesso.","green") 
            if ENV['feedback'] == 'gimme_your_certificate':
                TAc.print("Per convincerti che è fortemente connesso potrei darti una ear-decomposition del grafo. FEATURE ANCORA DA IMPLEMENTARE!\n","yellow")
        else:
            TAc.print("\nOk, il grafo NON è fortemente connesso.","green")
            if ENV['feedback'] == 'gimme_your_certificate':
                TAc.print(f"Infatti non vi è alcun arco che ti consenta di uscire da questo insieme di nodi: {sink_scc}\n","yellow")
    if ENV['goal'] == 'with_certificate':
        if g_is_sc_bool:
            TAc.print("Andrebbe richiesto e controllato un certificato del problem solver (nella forma di una ear-decomposition oppure di un arborescenza spanning entrante ed una uscente da uno stesso nodo). FEATURE ANCORA DA IMPLEMENTARE!\n","red")
        else:
            TAc.print("Andrebbe richiesto e controllato un certificato del problem solver (nella forma di un set di nodi da cui nessun arco esce). FEATURE ANCORA DA IMPLEMENTARE!\n","red")
