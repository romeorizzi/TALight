#!/usr/bin/env python3

from sys import stderr, exit

import sys
import graph_connectivity_lib as gcl

send_certificate = True

def startAlgo():
    spoon = input().strip()
    # Skipping first lines
    while spoon[:len("graph:")] != "graph:":
        spoon = input().strip()
        sys.stderr.write(f"> {spoon}\n")

    dimensions = input().strip()

    n, m = dimensions.split(' ')
    n = int(n)
    m = int(m)
    #sys.stderr.write(f"dimens {n}, {m}\n")
    # Creating graph
    grafo = gcl.Graph(n)

    # Getting arcs
    for _ in range(m):
        spoon = input().strip()
        v, u = spoon.split(' ')
        v, u = int(v), int(u)
        grafo.add_edge(v, u)

    #sys.stderr.write(grafo.to_str()+ "\n")
    
    # Sending answer
    connected = grafo.is_connected()[0]

    if(connected):
        print("yes")
    else:
        print("no")

    # Getting response
    spoon = input().strip()


    if(send_certificate):
        # Checking spanning tree
        input_spTree, not_visited = grafo.spanning_tree()
        if(connected):
            # Telling sp tree length
            print(len(input_spTree))
            sys.stderr.write(f"sp-tree dim {len(input_spTree)}\n")

            #printing sp tree
            for i in range(len(input_spTree)):
                u, v = input_spTree[i]
                print(f"{u} {v}")
        else:
            pass

        
    while spoon != "#end".strip():
        print(spoon)
        sys.stderr.write(str(spoon)+ "\n")
        spoon = input().strip()

# Main
spoon = input().strip()

# Reading the graph
startAlgo()