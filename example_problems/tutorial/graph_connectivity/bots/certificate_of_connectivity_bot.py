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

    #sys.stderr.write(grafo.to_str()+ "\n")
    
    # Ricevo istruzioni dal servizio
    while spoon[:len("# Tell me")] != "# Tell me":
        spoon = input().strip()

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
        print(spoon)
        sys.stderr.write(str(spoon)+ "\n")
        spoon = input().strip()

# Main
spoon = input().strip()
while spoon[:len("#start")] != "#start":
    spoon = input().strip()

# Reading the graph
startAlgo()