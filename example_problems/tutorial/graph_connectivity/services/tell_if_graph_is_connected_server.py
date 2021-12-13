#!/usr/bin/env python3

from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from bot_interface import service_server_requires_and_gets_the_only_file, BotInterface

import graph_connectivity_lib as gcl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ("with_yes_certificate",bool), 
    ("with_no_certificate",bool),
    ("input_mode",str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

if ENV["input_mode"] == "terminal":
    TAc.print(LANG.render_feedback("ok-congruent", f'#? waiting for your undirected simple graph.\nFormat: each line two numbers separated by spaces. In the first line, these are n and m, which specify the number of nodes and the number of edges, respectively. Then follow m lines, one for each edge, each with two numbers in the interval [0,n). These specify the tail node and the head node of the edge, in this order.\nBounds: n<=1000, m<=10000.\nAny line beggining with the \'#\' character is ignored.\nIf you prefer, you can use the \'TA_send_txt_file.py\' util here to send us the lines of a file. Just plug in the util at the \'rtal connect\' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.'), 'yellow')

    # Input prima riga: n,m
    n, m = TALinput(int, 2, TAc=TAc)
    if n < 1:
        TAc.print(LANG.render_feedback("n-LB", f'# ERROR: the number of nodes in the graph must be at least 1. Instead the first of the numbers you entered is n={n}.'), "red")
        exit(0)
    if m < 0:
        TAc.print(LANG.render_feedback("m-LB", f'# ERROR: The number of edges in the graph cannot be negative. Instead the second of the numbers you entered is m={m}.'), "red")
        exit(0)
    if n > 1000:
        TAc.print(LANG.render_feedback("n-UB", f'# ERROR: The number of nodes in the graph cannot exceed 1000. Instead the first of the numbers you entered is n={n}.'), "red")
        exit(0)
    if m > 10000:
        TAc.print(LANG.render_feedback("m-UB", f'# ERROR: The number of edges in the graph cannot exceed 10000. Instead the second of the numbers you entered is m={m}.'), "red")
        exit(0)
else: # input_mode=TA_send_files_bot
    graph = service_server_requires_and_gets_the_only_file().decode()

    lines=graph.splitlines()
    n, m = map(int,lines[0].split())


#print("#grafo fatto")
g = gcl.Graph(int(n))

# Input of m edges
for i in range(m):
    # INPUT
    if ENV["input_mode"] == "terminal":
        head, tail = TALinput(int, 2, TAc=TAc)
    else:
        head, tail = map(int,lines[i+1].split())

    # Check node numbering between 0 and n
    if tail >= n or head >= n or tail < 0 or head < 0:
        TAc.print(LANG.render_feedback("wrong-range-for-node", f'# ERROR: both ends of an edge must be nodes of the graph, i.e. integers in the range [0,{ENV["MAXN"]}.'), "red")
        exit(0)

    g.add_edge(int(head),int(tail))

# Graph creation completed


# Check if connect
is_connected, _ = g.is_connected(False)

if is_connected:
    TAc.print(LANG.render_feedback("graph-connected", f'\nThe submitted graph is connected.\n'),"green")
    if ENV["with_yes_certificate"]:
        sp_tree, not_visited = g.spanning_tree()
        if ENV["with_yes_certificate"]:
            TAc.print(LANG.render_feedback("printing-sp-tree", 'As a certificate, here is a spanning tree that guarantees the mutual reachability between any two nodes (for every node, we report its father in the tree. The father of the root node 0 is 0 itself):'),"yellow")
            for elem in sp_tree:
                TAc.print(elem, "white")
else:  # input graph g is NOT connected
    TAc.print(LANG.render_feedback("graph-not-connected",'The submitted graph is NOT connected.'),"green")
    if ENV["with_no_certificate"]:
        sp_tree, not_visited = g.spanning_tree()
        TAc.print(LANG.render_feedback("node-separation",'As a certificate, I will separate the nodes of the graph into two groups with no edge having endpoints in different groups.\nHere are the nodes in the first group:'),"yellow")
        for elem in sp_tree:
            TAc.print(elem[0], "white")
        TAc.print(LANG.render_feedback("second-group",'\nAnd here are the nodes in the second group:'), "yellow")
        for elem in not_visited:
            TAc.print(elem, "white")
exit(0)  
