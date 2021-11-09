#!/usr/bin/env python3

from sys import stderr, exit

import sys
sys.path.append('..')
from scc_lib import *

def startAlgo():
    numNodes = None
    spoon = input().strip()
    # Getting graph
    while spoon[:len("graph:")] != "graph:":
        # Getting number of nodes
        if spoon[:len("#   number of nodes:")] == '#   number of nodes:':
            numNodes = spoon.split(':')[1]
            numNodes = int("".join(numNodes.split()))
        spoon = input().strip()
    # Creating graph
    grafo = Graph(numNodes)


    # Getting sp. tree dimensions
    spoon = input().strip()
    n, m = spoon.split(' ')

    # Getting arcs
    spoon = input().strip()
    while spoon[0] != "#":
        v, u = spoon.split(' ')
        v, u = int(v), int(u)
        grafo.addEdge(v, u)
        spoon = input().strip()

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

    #stderr.write(out )
    print(out)

    # Getting response
    spoon = input()
    print(spoon)

# Main
spoon = input().strip()
while spoon[:len("#start")] != "#start":
    spoon = input().strip()

#LEGGO il grafo
startAlgo()