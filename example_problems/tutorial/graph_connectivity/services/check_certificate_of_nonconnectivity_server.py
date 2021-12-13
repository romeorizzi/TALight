#!/usr/bin/env python3

from re import M
from sys import stderr, exit
from os import environ
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import graph_connectivity_lib as gcl

# METADATA OF THIS TAL_SERVICE:
problem="graph_connectivity"
service="check_certificate_of_nonconnectivity"
args_list = [
    ("n",int), 
    #('m',int), 
    ("how_to_input_the_graph",str), 
    ("the_bipartition",str),
    ("silent",int),
    ("lang",str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
#TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
m = ENV["n"] - 1
if ENV["how_to_input_the_graph"] == "lazy":
    ENV.arg["how_to_input_the_graph"] = gcl.gen_instance_seed(False)

g, graph_print, edges = gcl.generate_graph(ENV["n"], m, int(ENV["how_to_input_the_graph"]), TAc=TAc, LANG=LANG)

# print the graph + info
TAc.print('#start:', "yellow")
TAc.print(LANG.render_feedback("assigned-instance", f'# The assigned instance is:\n#   number of nodes: {ENV["n"]}\n#   number of edges: {m}\n#   Seed: {ENV["how_to_input_the_graph"]}'), "yellow")

TAc.print('graph:', "yellow")
TAc.print(graph_print, "white")

#stderr.write("seed: " + ENV['how_to_input_the_graph']+"\n")
'''
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph() # For networkx 

for u, v in g.list_edges():
    G.add_edge(u, v)

nx.draw(G, with_labels = True)
plt.show()
'''

cert_conn = []
cert_non_conn = []

#take the bipartition from input if "lazy"
if ENV["the_bipartition"] == "lazy":
    TAc.print(LANG.render_feedback("give-bipartition",'# give me your bipartition in the format as \'the_bipartition\' argument'),"yellow")
    ENV.arg["the_bipartition"] = input()

    # TODO: check regex

# Splitting 'the_bipartition'
cert_conn, cert_non_conn = ENV["the_bipartition"].split("versus")

cert_conn = cert_conn.split()
cert_non_conn = cert_non_conn.split()

# Cast to int
cert_conn = list(map(int, cert_conn))
cert_non_conn = list(map(int, cert_non_conn))


# Check the certificate

# look for a spanning tree and generate the 2 sets
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
# Print my certificate
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

stderr.write("cert_conn: " + str(cert_conn))
stderr.write("conn_list: " + str(conn_list))

stderr.write("equals: " + str(equals))

# If correct
if(equals):
    if(ENV["silent"] == 0):
        TAc.print(LANG.render_feedback("correct-certificate",'Good! Your certificate is correct'),"green")
else: # If it's wrong
    TAc.print(LANG.render_feedback("wrong-certificate-lets-check",'WRONG, the certificate you gave me is not a correct spanning tree..Let\'s check it:'),"red")
    #look at the CONNECTED certificate items that is correct
    conn_correct = set(cert_conn).intersection(set(conn_list))
    conn_correct = list(map(str, conn_correct))

    TAc.print(LANG.render_feedback("right-connected",'These are the connected items you guessed at: ' + ",".join(conn_correct)),"white")
    #look at the UNCONNECTED certificate items that is correct
    conn_wrong = set(cert_non_conn).intersection(set(nonconn_list))
    conn_wrong = list(map(str, conn_wrong))

    TAc.print(LANG.render_feedback("wrong-connected",'\nThese, on the other hand, are the unconnected items you guessed at: ' + ",".join(conn_wrong)),"white")

