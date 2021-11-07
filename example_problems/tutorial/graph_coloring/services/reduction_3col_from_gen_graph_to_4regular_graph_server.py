#!/usr/bin/env python3
from sys import exit
import random
from ast import literal_eval as make_tuple
import networkx as nx

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import graph_coloring_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('num_nodes',int),
    ('format',str),    
    ('ISATTY',bool),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.print_opening_msg(), "green")

# START CODING YOUR SERVICE:


if ENV["seed"] == 'random_seed':
    seed = random.randint(100000,999999)    
else:
    seed = int(ENV["seed"])
print(LANG.render_feedback("assigned-instance", f"# The assigned instance is:\n#   number of nodes: {ENV['num_nodes']}\n#   number of arcs: {ENV['num_arcs']}\n#   Seed: "), end="")
TAc.print(seed, "yellow")


numNodes = ENV["num_nodes"]
numArcs = ENV["num_arcs"]

graph = nx.fast_gnp_random_graph(numNodes, 0.5, seed=seed)
print(LANG.render_feedback("graph", "graph: "))
print(f"{len(graph.nodes())} {len(graph.edges())}")
if ENV['format'] == 'list_of_edges':
    for u,v in graph.edges():
        print(f"{u} {v}")
elif ENV['format'] == 'adjacency_matrix':
    adjacencyMatrix = Utilities.arcsListToGraph(graph.edges())
    for i in range(len(adjacencyMatrix)):
        print(f"\t{i}:  ", end="")
        print(*adjacencyMatrix[i], sep = ", ")

print(LANG.render_feedback("give_new_graph", "# Insert the new graph as a list of edges, where an edge is a tuple of the two nodes connected by that edge:"))
buffer = TALinput(
    str,
    regex=r"^(\(([0-9][0-9]{0,2}|1000),([0-9][0-9]{0,2}|1000)\))$",
    regex_explained="a sequence of tuple with number from 0 to " + str(numNodes - 1) + " separated by spaces. An example is: '(1,2) (3,4)'.",
    TAc=TAc
)
buffer = list(filter(None, buffer))
inputArcs = [make_tuple(i) for i in buffer]

newGraph = nx.Graph(inputArcs)

if not nx.is_k_regular(newGraph, 4):
    TAc.print(LANG.render_feedback("not-4regular", f"NO! The new graph is not 4-regular."), "red", ["bold"])
    exit(0)

graphColors = nx.greedy_color(graph, strategy='largest_first')
newGraphColors = nx.greedy_color(newGraph, strategy='largest_first')
if len(set(newGraph.values())) == 3 and len(set(graphColors.values())) != 3:
    TAc.print(LANG.render_feedback("not-3colorable", f"NO! The new graph is meant to be 3-colorable if G is 3-colorable."), "red", ["bold"])
    exit(0)
elif len(set(newGraph.values())) != 3 and len(set(graphColors.values())) == 3:
    TAc.print(LANG.render_feedback("not-3colorable", f"NO! The new graph is meant to be not 3-colorable if G is not 3-colorable."), "red", ["bold"])
    exit(0)

TAc.OK()
print()
