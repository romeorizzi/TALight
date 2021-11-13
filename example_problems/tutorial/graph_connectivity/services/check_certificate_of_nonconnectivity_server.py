#!/usr/bin/env python3

from re import M
from sys import stderr, exit

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="graph_connectivity"
service="check_certificate_of_nonconnectivity"
args_list = [
    ('n',int), 
    #('m',int), 
    ('how_to_input_the_graph',str), 
    ('the_bipartition',str),
    ('silent',int),
    ('lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
#TAc.print(LANG.opening_msg, "green")

n = ENV['n']
m = n-1
seed = ENV['how_to_input_the_graph']
the_bipartition = ENV['the_bipartition']
silent = ENV['silent']
g,graph_print,edges,seed = GenerateGraph(seed, n, m, False)

# Stampo il grafo + info
print("#start:")
print(f"# The assigned instance is:\n#   number of nodes: {n}\n#   number of arcs: {m}\n#   Seed: {seed}\n", end="")

print("graph:")
print(graph_print)

cert_conn = []
cert_non_conn = []

# Prendo bipartizione da input se "lazy"
if the_bipartition == "lazy":
    print("# give me your bipartition in the format as \'the_bipartition\' argument")
    the_bipartition = input()

    # TODO: check regex

# Splitting 'the_bipartition'
cert_conn, cert_non_conn = the_bipartition.split("versus")

cert_conn = cert_conn.split()
cert_non_conn = cert_non_conn.split()

# Cast to int
cert_conn = list(map(int, cert_conn))
cert_non_conn = list(map(int, cert_non_conn))


# Controllo il certificato

# Cerco uno spanning tree e genero i 2 insiemi
spTree, not_spTree_list = g.spanning_tree() 

conn_list = []
for elem in spTree:
    conn_list.append(elem[0])
    conn_list.append(elem[1])
conn_list = list(set(conn_list))

nonconn_list = []
for elem in not_spTree_list:
    nonconn_list.append(elem)
nonconn_list = list(set(nonconn_list))

'''
# Printo il mio certificato
conn_out = ""
for elem in conn_list:
    conn_out += str(elem) + " "

notconn_out = ""
for elem in nonconn_list:
    notconn_out += str(elem) + " "

out = conn_out + " versus " + notconn_out

stderr.write(out)
'''

equals = sorted(cert_conn) == sorted(conn_list) and sorted(cert_non_conn) == sorted(nonconn_list)


stderr.write("equals: " + str(equals))

# Se corretto
if(equals):
    if(silent == 0):
        print(equals)
else: # Se è sbagliato
    # Guardo gli elementi CONNESSI del certificato corretti
    conn_corretti = set(cert_conn).intersection(set(conn_list))
    conn_corretti = list(map(str, conn_corretti))

    print("Questi sono gli elementi connessi che hai azzeccato: " + ",".join(conn_corretti))
    # Guardo gli elementi NON CONNESSI del certificato corretti
    conn_non_corretti = set(cert_non_conn).intersection(set(nonconn_list))
    conn_non_corretti = list(map(str, conn_non_corretti))

    print("\nQuesti invece sono gli elementi non connessi che hai azzeccato: " + ",".join(conn_non_corretti))

