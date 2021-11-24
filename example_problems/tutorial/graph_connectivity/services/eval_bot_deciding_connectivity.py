#!/usr/bin/env python3

from re import M
from sys import stderr, exit

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="graph_connectivity"
service="eval_bot_deciding_connectivity"
args_list = [
    ('goal',str), 
    ('check_also_yes_certificate',int),
    ('check_also_no_certificate',int),
    ('code_lang',str),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
#TAc.print(LANG.opening_msg, "green")

goal = ENV['goal']
check_also_yes_certificate = ENV['check_also_yes_certificate']
check_also_no_certificate = ENV['check_also_no_certificate']
code_lang = ENV['code_lang']
lang = ENV['lang']

'''
g,graph_print,edges,seed = GenerateGraph(seed, n, m, True)

# Stampo il grafo + info
print("#start:")
print(f"# The assigned instance is:\n#   number of nodes: {n}\n#   number of arcs: {m}\n#   Seed: {seed}\n", end="")

print("graph:")
print(graph_print)

print(f"#? waiting for your spanning tree as routing table.\n# Format: each line two numbers separated by space. Then follow m lines, one for each arc, each with two numbers in the interval [0,n).\n# These specify the tail node and the head node of the arc, in this order.\n# Any line beggining with the '#' character is ignored.\n# If you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

span = Graph(int(n))
has_outer_edges = True
not_in_graph = []

# Asking and getting sp.tree length
print("# Tell me how long is your spanning tree")
sptree_len = TALinput(int, 1, TAc=TAc)


for i in range(sptree_len[0]):
    head, tail = TALinput(int, 2, TAc=TAc)
    head, tail = int(head),int(tail)

    if tail >= n or head >= n or tail < 0 or head < 0:
        TAc.print(LANG.render_feedback("n-at-least-1", f"# ERRORE: entrambi gli estremi di un arco devono essere nodi del grafo, ossia numeri interi ricompresi nell'intervallo [0,{ENV['MAXN']}."), "red")
        exit(0)

    # Verifico l'esistenza degli archi (e dei nodi)
    if(g.checkEdge(head,tail)):
        span.addEdge(head, tail)
    else:
        has_outer_edges = False
        arco = (int(head),int(tail))
        not_in_graph.append(arco)


# Controllo se è connesso
is_correct, not_conn = span.isConnected(True)

is_correct = has_outer_edges and has_outer_edges


out=""
for e in not_in_graph:
    out+=str(e[0])+","+str(e[0])+";"



if(is_correct):
    if (silent == 0):
        TAc.print("\n\nESATTO, il certificato e' corretto.\n","green")
else:
    TAc.print("\n\nSBAGLIATO, il certificato che mi hai dato non e' uno spanning tree corretto.\n","red")
    # Printo elenco archi non in g (se esistono)
    if(len(not_in_graph) != 0):
        TAc.print("Questi archi non appartengono al grafo","green")
        for e in not_in_graph:
            print(e)
    TAc.print("Questi nodi del grafo non sono raggiunti dal tuo spanning tree","green")
    for n in not_conn:
            print(n)
'''