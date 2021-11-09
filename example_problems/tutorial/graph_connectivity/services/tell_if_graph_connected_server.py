#!/usr/bin/env python3

from sys import stderr, exit

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from bot_interface import service_server_requires_and_gets_the_only_file, BotInterface

from scc_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="graph_connectivity"
service="tell_if_graph_connected"
args_list = [
    ('with_yes_certificate',int), 
    ('with_no_certificate',int),
    ('lang',str),
    ('input_mode',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
#TAc.print(LANG.opening_msg, "green")

if ENV['input_mode'] == 'terminal':
    # START CODING YOUR SERVICE:
    print(f"#? waiting for your directed graph.\nFormat: each line two numbers separated by space. Then follow m lines, one for each arc, each with two numbers in the interval [0,n). These specify the tail node and the head node of the arc, in this order.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

    # Prima riga: n,m
    n, m = TALinput(int, 2, TAc=TAc)
    #TAc.print("presi n e m","red")
else: # input_mode=TA_send_files_bot graph_connectivity
    graph=service_server_requires_and_gets_the_only_file().decode()

    lines=graph.splitlines()
    n,m = map(int,lines[0].split())


if n < 1:
    TAc.print(LANG.render_feedback("n-LB", f"# ERRORE: il numero di nodi del grafo deve essere almeno 1. Invece il primo dei numeri che hai inserito è n={n}."), "red")
    exit(0)
if m < 0:
    TAc.print(LANG.render_feedback("m-LB", f"# ERRORE: il numero di archi del grafo non può essere negativo. Invece il secondo dei numeri che hai inserito è m={m}."), "red")
    exit(0)
#print("#grafo fatto")
g = Graph(int(n))


# Controllo numerazione dei nodi tra 0 e n
for i in range(m):
    # INPUT
    if ENV['input_mode'] == 'terminal':
        head, tail = TALinput(int, 2, TAc=TAc)
    else:
        head, tail = map(int,lines[i+1].split())

    # Controllo 
    if tail >= n or head >= n or tail < 0 or head < 0:
        TAc.print(LANG.render_feedback("n-at-least-1", f"# ERRORE: entrambi gli estremi di un arco devono essere nodi del grafo, ossia numeri interi ricompresi nell'intervallo [0,{ENV['MAXN']}."), "red")
        exit(0)

    g.addEdge(int(head),int(tail))

#creazione grafo completata

is_connected = g.isConnected()
with_yes_certificate = bool(ENV['with_yes_certificate'])
with_no_certificate = bool(ENV['with_no_certificate'])

# Stampo correttezza
if(is_connected):
    TAc.print("\n\nESATTO, il grafo e' connesso.\n","green")
else:
    TAc.print("\n\nSBAGLIATO, il grafo non e' connesso.\n","red")

# Se voglio certificati
if(ENV['with_yes_certificate'] == 1  or ENV['with_no_certificate'] == 1):
    sp_tree, not_visited = g.spanning_tree()
    if(ENV['with_yes_certificate'] == 1):
        TAc.print("\nEccoti lo spanning tree:\n","yellow")
        for elem in sp_tree:
            print(elem)
    if(ENV['with_no_certificate'] == 1):
        TAc.print("\nEccoti la partizione:\n","yellow")

        for elem in sp_tree:
            print(elem[0])
        print("--")
        for elem in not_visited:
            print(elem)
exit(0)  