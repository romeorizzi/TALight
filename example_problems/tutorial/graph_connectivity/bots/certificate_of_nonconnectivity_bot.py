#!/usr/bin/env python3

from sys import stderr, exit

import sys
import graph_connectivity_lib as gcl

def startAlgo():
    spoon = input().strip()
    # Skipping first lines
    while spoon[:len("graph:")] != "graph:":
        spoon = input().strip()

    dimensions = input().strip()

    n, m = dimensions.split(' ')
    n = int(n)
    m = int(m)
    # Creating graph
    grafo = gcl.Graph(n)

    # Getting arcs
    for _ in range(m):
        spoon = input().strip()
        v, u = spoon.split(' ')
        v, u = int(v), int(u)
        grafo.add_edge(v, u)


    # Checking spanning tree
    input_spTree, not_visited = grafo.spanning_tree()
    
    conn_list = []
    for elem in input_spTree:
        conn_list.append(elem[0])
        conn_list.append(elem[1])
    conn_list = list(set(conn_list))

    nonconn_list = []
    for elem in not_visited:
        nonconn_list.append(elem)
    nonconn_list = list(set(nonconn_list))

    conn_out = ""
    for elem in conn_list:
        conn_out += str(elem) + " "

    notconn_out = ""
    for elem in nonconn_list:
        notconn_out += str(elem) + " "

    out = conn_out + " versus " + notconn_out

    stderr.write(out )
    print(out)

    # Getting response
    spoon = input()
    
    while spoon != "#end".strip():
        print(spoon)
        sys.stderr.write(str(spoon)+ "\n")
        spoon = input().strip()

# Main
spoon = input().strip()
while spoon[:len("#start")] != "#start":
    print(spoon)
    sys.stderr.write(str(spoon)+ "\n")
    spoon = input().strip()

# Reading the graph
startAlgo()