#!/usr/bin/env python3
from sys import exit
import random
from ast import literal_eval as make_tuple

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import graph_coloring_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
problem="graph_coloring"
service="recognize_proper_colorings"
args_list = [
    ('num_nodes',int),
    ('num_arcs',int),
    ('seed',str),
    ('coloring',str),
    ('goal',str),
    ('lang',str),    
    ('ISATTY',bool),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

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

colors = [0 for i in range(len(graph))]
rightColors = []
colorsNum = 4
while not rightColors:
    rightColors = Utilities.graphColoring(graph, colorsNum, 0, colors)
    colorsNum += 1

print(LANG.render_feedback("graph", "graph: "))
for i in range(len(graph)):
    print(f"\t{i}:  ", end="")
    print(*graph[i], sep = ", ")

newColors = None
wrongArcs = None
print(LANG.render_feedback("coloring", "coloring: "), end="")
if ENV['coloring'] == 'improper' or (ENV['coloring'] == 'surprise' and bool(random.randint(0, 1))):
    newColors, wrongArcs = Utilities.breakGraphColoring(graph, rightColors, seed)
    print(*newColors, sep = ", ")
else:  
    print(*rightColors, sep = ", ")
if ENV['goal'] == "yes_no":
    print(LANG.render_feedback("yes_no", "is the coloring proper? (yes/no): "))
    buffer = TALinput(
        str,
        num_tokens=1,
        regex=r"^(yes|no)$",
        regex_explained="yes or no",
        TAc=TAc
    )
    userInput = buffer[0]
    if (wrongArcs and userInput == 'no') or (not wrongArcs and userInput == 'yes'):
        TAc.OK()
    else:
        TAc.NO()
else:
    print(LANG.render_feedback("give_violated_arc", "if the coloring is not proper, indicate the violated arcs by inserting an arc like a tuple of the two nodes connected by that arc, if the coloring is proper insert an empty line."))
    buffer = TALinput(
        str,
        regex=r"^(\(([0-9][0-9]{0,2}|1000),([0-9][0-9]{0,2}|1000)\)|\s*)$",
        regex_explained="an empty line or a sequence of tuple with number from 0 to " + str(numNodes - 1) + " separated by spaces. An example is: '(1,2) (3,4)'.",
        TAc=TAc
    )
    buffer = list(filter(None, buffer))
    inputArcs = [make_tuple(i) for i in buffer]
    if not inputArcs and not wrongArcs:
        TAc.OK()
    elif not inputArcs and wrongArcs:
        TAc.print(LANG.render_feedback("wrong-arcs", f"NO! The coloring is not proper, the violated arcs is {' '.join(map(str, wrongArcs))}"), "red", ["bold"])
    elif not wrongArcs and inputArcs:
        TAc.print(LANG.render_feedback("wrong-not-proper", f"NO! The coloring is proper!"), "red", ["bold"])
    else:
        if len(wrongArcs) != len(inputArcs):
            TAc.print(LANG.render_feedback("wrong-proper", f"NO! The violated arc is {' '.join(map(str, wrongArcs))}"), "red", ["bold"])
            exit(0)
        for i in wrongArcs:
            if i not in inputArcs and i[::-1] not in inputArcs:
                TAc.print(LANG.render_feedback("wrong-proper", f"NO! The violated arc is {' '.join(map(str, wrongArcs))}"), "red", ["bold"])
                exit(0)
        TAc.OK()