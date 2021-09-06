#!/usr/bin/env python3
from sys import exit
import random
from ast import literal_eval as make_tuple

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import graph_coloring_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
problem="graph_coloring"
service="yield_proper_colorings"
args_list = [
    ('num_nodes',int),
    ('num_arcs',int),
    ('seed',str),
    ('k',str),
    ('goal',str),
    ('lang',str),    
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

graph = Utilities.generateGraph(numNodes, numArcs, seed)
print(LANG.render_feedback("graph", "graph: "))
for i in range(len(graph)):
    print(f"\t{i}:  ", end="")
    print(*graph[i], sep = ", ")

rightColors = []
if ENV['k'] == 'num_nodes':
    colorsNum = numNodes
else:
    colorsNum = int(ENV['k'])


if ENV['goal'] == 'yes_no':
    colors = [0 for i in range(len(graph))]
    colors = Utilities.graphColoring(graph, colorsNum, 0, colors)
    print(LANG.render_feedback("yes_no", f"# the graph is {colorsNum}-colorable? (yes/no): "))
    buffer = TALinput(
        str,
        num_tokens=1,
        regex=r"^(yes|no)$",
        regex_explained="yes or no",
        TAc=TAc
    )
    userInput = buffer[0]
    if (len(colors) == 0 and userInput == 'no') or (len(colors) > 0  and userInput == 'yes'):
        TAc.OK()
        print()
    else:
        TAc.NO()
        print()
elif ENV['goal'] == 'give_coloring':
    print(LANG.render_feedback("give_coloring", f"# Enter colors in the form of a number for each node separated by a space: "))
    buffer = TALinput(
        str,
        num_tokens=numNodes,
        regex=r"^([1-9]|1[0-9]|20)$",
        regex_explained=f"a sequence of {numNodes} numbers from 1 to {colorsNum} separeted by a space. An example is: '1 2 1'.",
        TAc=TAc
    )
    colors = [int(i) for i in buffer]
    if len(set(colors)) > colorsNum:
        TAc.print(LANG.render_feedback("wrong-colors-num", f"NO! You can't use more than {colorsNum} colors"), "red", ["bold"])
    else:
        result = Utilities.isSafeColored(graph, colors)
        if result:
            TAc.OK()
            print()
        else:
            TAc.NO()
            print()
elif ENV['goal'] == 'give_minimal_uncolorable_induced_subgraph':
    print(LANG.render_feedback("give_violated_arc", "Insert the arcs of the minimal uncolorable induced subgraph like a tuple of the two nodes connected by that arc, if the graph itself is already the minimum uncolorable induced one insert an empty line."))
    buffer = TALinput(
        str,
        regex=r"^(\(([0-9][0-9]{0,2}|1000),([0-9][0-9]{0,2}|1000)\)|\s*)$",
        regex_explained="an empty line or a sequence of tuple with number from 0 to " + str(numNodes - 1) + " separated by spaces. An example is: '(1,2) (3,4)'.",
        TAc=TAc
    )
    buffer = list(filter(None, buffer))
    arcsSubgraph = [make_tuple(i) for i in buffer]

    if arcsSubgraph:
        if not Utilities.isSubgraph(graph, arcsSubgraph):
            TAc.print(LANG.render_feedback("wrong-subgraph", f"NO! This is not a valid subgraph"), "red", ["bold"])
            exit(0)

        if not Utilities.isInducedSubgraph(graph, arcsSubgraph):
            TAc.print(LANG.render_feedback("wrong-induced-subgraph", f"NO! This is not a valid induced subgraph"), "red", ["bold"])
            exit(0)

        subgraph = Utilities.arcsListToGraph(arcsSubgraph)
    else:
        subgraph = graph

    colors = [0 for i in range(len(subgraph))]
    colors = Utilities.graphColoring(subgraph, colorsNum, 0, colors)
    if colors:
        TAc.print(LANG.render_feedback("wrong-induced-subgraph-colorable", f"NO! This is {colorsNum}-colorable"), "red", ["bold"])
        exit(0)

    if colorsNum < len(subgraph) - 1:
        minimalArcsSubgraph, colors = Utilities.getNotKColorableSubgraph(graph, colorsNum, len(subgraph) - 1)
        if minimalArcsSubgraph:
            TAc.print(LANG.render_feedback("wrong-induced-subgraph-minimal", f"NO! This is not minimal not {colorsNum}-colorable induced subgraph"), "red", ["bold"])
            exit(0)
    
    TAc.OK()
    print()