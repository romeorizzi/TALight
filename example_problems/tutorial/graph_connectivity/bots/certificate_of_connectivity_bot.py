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
    #spoon = input().strip()
    #n, m = spoon.split(' ')

    # Getting arcs
    spoon = input().strip()

    while spoon[0] != "#":
        v, u = spoon.split(' ')
        v, u = int(v), int(u)
        grafo.addEdge(v, u)
        spoon = input().strip()

        if(len(spoon) == 0):
            spoon = input().strip()

    # Ricevo istruzioni dal servizio
    while spoon != "# Tell me how long is your spanning tree".strip():
        spoon = input().strip()

    sys.stderr.write("finito\n")

    # Checking spanning tree
    input_spTree, not_visited = grafo.spanning_tree()

    # Telling sp tree length
    print(len(input_spTree))

    #printing sp tree
    for i in range(len(input_spTree)):
        u, v = input_spTree[i]
        print(f"{u} {v}")

    # Getting response
    spoon = input().strip()


    while spoon != "#end".strip():
        spoon = input().strip()
        print(spoon)
        sys.stderr.write(str(spoon)+ "\n")

# Main
spoon = input().strip()
while spoon[:len("#start")] != "#start":
    spoon = input().strip()

#LEGGO il grafo
startAlgo()