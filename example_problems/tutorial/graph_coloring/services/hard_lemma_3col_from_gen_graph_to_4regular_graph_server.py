#!/usr/bin/env python3
from sys import exit
import random
from ast import literal_eval as make_tuple
import networkx as nx

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import graph_coloring_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
problem="graph_coloring"
service="hard_lemma_3col_from_gen_graph_to_4regular_graph"
args_list = [
    ('num_nodes',int),
    ('seed',str),
    ('lang',str),    
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


numNodes = ENV["num_nodes"]
numArcs = ENV["num_arcs"]

graph = None
graphColors = None
notFind = True
while notFind:
    graph = nx.fast_gnp_random_graph(numNodes, 0.5, seed=seed)
    graphColors = nx.greedy_color(graph, strategy='largest_first')
    if len(set(graphColors.values())) == 3:
        notFind = False
        TAc.print(seed, "yellow")
    else:
        seed = random.randint(100000,999999) 

adjacencyMatrix = nx.adjacency_matrix(graph)
adjacencyMatrix = adjacencyMatrix.todense().tolist()
print(LANG.render_feedback("graph", "graph: "))
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

GM = nx.algorithms.isomorphism.GraphMatcher(newGraph, graph)
if not GM.subgraph_is_isomorphic():
    TAc.print(LANG.render_feedback("not-equivalent", f"NO! The new graph is not equivalent."), "red", ["bold"])
    exit(0)

newGraphColors = nx.greedy_color(newGraph, strategy='largest_first')
if len(set(newGraph.values())) != 3:
    TAc.print(LANG.render_feedback("not-3colorable", f"NO! The new graph is meant to be 3-colorable if and only if G is 3-colorable."), "red", ["bold"])
    exit(0)

print(LANG.render_feedback("coloring", f"coloring of new graph: {newGraphColors}"))

print(LANG.render_feedback("give_coloring", f"# Enter colors for G in the form of a number for each node separated by a space: "))
buffer = TALinput(
    str,
    num_tokens=numNodes,
    regex=r"^([1-9]|1[0-9]|20)$",
    regex_explained=f"a sequence of {numNodes} numbers from 1 to {3} separeted by a space. An example is: '1 2 1'.",
    TAc=TAc
)
graphColorsOfUser = [int(i) for i in buffer]
if len(set(graphColorsOfUser)) > 3:
    TAc.print(LANG.render_feedback("wrong-colors-num", f"NO! You can't use more than {3} colors."), "red", ["bold"])
    exit(0)

adjacencyMatrixOfUser = nx.adjacency_matrix(newGraph)
adjacencyMatrixOfUser = adjacencyMatrixOfUser.todense().tolist()
result = Utilities.isSafeColored(adjacencyMatrixOfUser, graphColorsOfUser)
if not result:
    TAc.print(LANG.render_feedback("wrong-3coloring", f"NO! The coloring of the G graph is incorrect."), "red", ["bold"])
    exit(0)

for i in range(len(graphColorsOfUser)):
    if newGraphColors[i] != graphColorsOfUser[i]:
        TAc.print(LANG.render_feedback("not-coloring-from-g", f"NO! The coloring of the new graph not start from G graph."), "red", ["bold"])
        exit(0)

TAc.OK()
print()