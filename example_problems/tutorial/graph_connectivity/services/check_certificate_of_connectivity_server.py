#!/usr/bin/env python3

from re import M
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import graph_connectivity_lib as gcl

# METADATA OF THIS TAL_SERVICE:
problem="graph_connectivity"
service="check_certificate_of_connectivity"
args_list = [
    ("n",int), 
    #('m',int), 
    ("how_to_input_the_graph",str), 
    ("silent",int),
    ("lang",str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
#TAc.print(LANG.opening_msg, "green")

m = ENV["n"] - 1
g, graph_print, edges = gcl.generate_graph(ENV["n"], m, gcl.gen_instance_seed(True), TAc=TAc, LANG=LANG)

# print the graph + info
TAc.print('#start:', "yellow")
TAc.print(LANG.render_feedback("assigned-instance", f'# The assigned instance is:\n#   number of nodes: {ENV["n"]}\n#   number of edges: {m}\n#   Seed: {ENV["how_to_input_the_graph"]}'), "yellow")

TAc.print('graph:', "yellow")
TAc.print(graph_print, "white")

TAc.print(LANG.render_feedback("waiting-sp-tree",f'#? waiting for your spanning tree as routing table.\n# Format: each line two numbers separated by space. Then follow m lines, one for each edge, each with two numbers in the interval [0,n).\n# These specify the tail node and the head node of the edge, in this order.\n# Any line beggining with the \'#\' character is ignored.\n# If you prefer, you can use the \'TA_send_txt_file.py\' util here to send us the lines of a file. Just plug in the util at the \'rtal connect\' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.'), "yellow")

span = gcl.Graph(int(ENV["n"]))
has_outer_edges = True
not_in_graph = []

# Asking and getting sp.tree length
TAc.print(LANG.render_feedback("waiting-sp-tree-len",'# Tell me how many rows are in your spanning tree table'), "yellow")

sptree_len = TALinput(int, 1, TAc=TAc)

for i in range(sptree_len[0]):
    head, tail = TALinput(int, 2, TAc=TAc)
    head, tail = int(head),int(tail)

    # Checking if the inserted nodes are in the range [0, n]
    if tail >= ENV["n"] or head >= ENV["n"] or tail < 0 or head < 0:
        TAc.print(LANG.render_feedback("n-at-least-1", f'# ERROR: both ends of an edge must be nodes of the graph, i.e. integers in the range [0,{ENV["MAXN"]}.'), "red")
        exit(0)

    # check the existence of the edges (and nodes)
    if(g.check_edge(head,tail)):
        span.add_edge(head, tail)
    else:
        has_outer_edges = False
        edge = (int(head),int(tail))
        not_in_graph.append(edge)

# check if is connect
is_correct, not_conn = span.is_connected(True)

is_correct = is_correct and has_outer_edges

'''
out=""
for e in not_in_graph:
    out+=str(e[0])+","+str(e[0])+";"
'''
stderr.write(str(is_correct)+"\n")

if(is_correct):
    if (ENV["silent"] == 0):
        TAc.print(LANG.render_feedback("correct-certificate",'Good! Your certificate is correct'),"green")
else:
    TAc.print(LANG.render_feedback("wrong-certificate-lets-check",'WRONG, the certificate you gave me is not a correct spanning tree..Let\'s check it:'),"red")
    
    # Printo elenco edgehi non in g (se esistono)
    if(len(not_in_graph) != 0):
        TAc.print(LANG.render_feedback("not-in-graph",'These edges don\'t belong to the graph'),"green")
        for e in not_in_graph:
            print(e)
    TAc.print(LANG.render_feedback("not-in-sp-tree",'These graph nodes are not reached by your spanning tree'),"green")
    for n in not_conn:
        print(n)
TAc.print('#end',"yellow")
