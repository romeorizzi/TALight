#!/usr/bin/env python3

from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from bot_interface import service_server_requires_and_gets_the_only_file, BotInterface

import graph_connectivity_lib as gcl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('with_yes_certificate',bool), 
    ('with_no_certificate',bool),
    ('input_mode',str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

if ENV['input_mode'] == 'terminal':
    TAc.print(LANG.render_feedback("ok-congruent", f'#? waiting for your directed graph.\nFormat: each line two numbers separated by space. Then follow m lines, one for each arc, each with two numbers in the interval [0,n). These specify the tail node and the head node of the arc, in this order.\nBounds: n<=1000, m<=10000.\nAny line beggining with the \'#\' character is ignored.\nIf you prefer, you can use the \'TA_send_txt_file.py\' util here to send us the lines of a file. Just plug in the util at the \'rtal connect\' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.'), 'yellow')

    # Input prima riga: n,m
    n, m = TALinput(int, 2, TAc=TAc)
    if n < 1:
        TAc.print(LANG.render_feedback("n-LB", f'# ERROR: the number of nodes in the graph must be at least 1. Instead the first of the numbers you entered is n={n}.'), "red")
        exit(0)
    if m < 0:
        TAc.print(LANG.render_feedback("m-LB", f'# ERROR: The number of arcs in the graph cannot be negative. Instead the second of the numbers you entered is m={m}.'), "red")
        exit(0)
    if n > 1000:
        TAc.print(LANG.render_feedback("n-UB", f'# ERROR: The number of nodes in the graph cannot exceed 1000. Instead the first of the numbers you entered is n={n}.'), "red")
        exit(0)
    if m > 10000:
        TAc.print(LANG.render_feedback("m-UB", f'# ERROR: The number of arcs in the graph cannot exceed 10000. Instead the second of the numbers you entered is m={m}.'), "red")
        exit(0)
else: # input_mode=TA_send_files_bot
    graph = service_server_requires_and_gets_the_only_file().decode()

    lines=graph.splitlines()
    n, m = map(int,lines[0].split())


#print("#grafo fatto")
g = gcl.Graph(int(n))

# Input of m arcs
for i in range(m):
    # INPUT
    if ENV['input_mode'] == 'terminal':
        head, tail = TALinput(int, 2, TAc=TAc)
    else:
        head, tail = map(int,lines[i+1].split())

    # Check node numbering between 0 and n
    if tail >= n or head >= n or tail < 0 or head < 0:
        TAc.print(LANG.render_feedback("wrong-range-for-node", f'# ERROR: both ends of an arc must be nodes of the graph, i.e. integers in the range [0,{ENV["MAXN"]}.'), "red")
        exit(0)

    g.add_edge(int(head),int(tail))

# Graph creation completed


# Check if connect
is_connected, _ = g.is_connected(False)

if is_connected:
    TAc.print(LANG.render_feedback("graph-connected", f'Good! The submitted graph is connected.\n'),"green")
    #TAc.print(LANG.render_feedback("graph-connected", f'\nThe submitted graph is connected.\n'),"green")
    if ENV['with_yes_certificate']:
        sp_tree, not_visited = g.spanning_tree()
        if ENV['with_yes_certificate']:
            TAc.print(LANG.render_feedback("printing-sp-tree", "Here there is a spanning tree:\n","yellow"))
            for elem in sp_tree:
                TAc.print(elem, "white")
else:  # input graph g is NOT connected
    TAc.print(LANG.render_feedback("graph-not-connected","The provided graph is NOT connected."),"red")
    if ENV['with_no_certificate']:
        sp_tree, not_visited = g.spanning_tree()
        TAc.print(LANG.render_feedback("printing-bipartition","I'll give you a bipartition of the graph.\nHere there are the connected nodes:"),"yellow")
        for elem in sp_tree:
            TAc.print(elem[0], "white")
        TAc.print(LANG.render_feedback("print-not-conected","\nAnd here the not connected ones:"), "yellow")
        for elem in not_visited:
            TAc.print(elem, "white")
exit(0)  
