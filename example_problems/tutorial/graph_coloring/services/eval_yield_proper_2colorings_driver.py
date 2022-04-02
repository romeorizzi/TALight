#!/usr/bin/env python3
from sys import exit
import random
from ast import literal_eval as make_tuple

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import graph_coloring_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('commitment',str),
    ('goal',str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.print_opening_msg(), "green")

# START CODING YOUR SERVICE:


if ENV["seed"] == 'random_seed':
    seed = random.randint(100000,999999)   
else:
    seed = int(ENV["seed"])
random.seed(seed)
print(LANG.render_feedback("assigned-instance", f"# The seed of assigned instance is: "), end="")
TAc.print(seed, "yellow")
print("#start")


num_matches = 10
matchWin = 0
numNodes = 4
numArcs = 5
colorsNum = 2
matchDone = 1
while matchDone <= num_matches:
    internalSeed = random.randint(100000,999999)
    print(LANG.render_feedback("new-match", f"# match {matchDone} of {num_matches}. Instance:\n#   number of nodes: {numNodes}\n#   number of arcs: {numArcs}\n#   seed: "), end="")
    TAc.print(internalSeed, "yellow")

    graph = None
    if bool(random.randint(0, 1)):
        graph = Utilities.generateBipartiteGraph(numNodes, numArcs, seed)
    else:
        graph = Utilities.generateGraph(numNodes, numArcs, seed)

    print(LANG.render_feedback("graph", "graph: "))
    for i in range(len(graph)):
        print(f"\t{i}:  ", end="")
        print(*graph[i], sep = ", ")
        

    if ENV['commitment'] == 'yes_no':
        isBipartite = Utilities.isBipartite(graph)
        print(LANG.render_feedback("yes_no", f"# ? the graph is {colorsNum}-colorable? (yes/no): "))
        buffer = TALinput(
            str,
            num_tokens=1,
            regex=r"^(yes|no)$",
            regex_explained="yes or no",
            TAc=TAc
        )
        userInput = buffer[0]
        if (not isBipartite and userInput == 'no') or (isBipartite  and userInput == 'yes'):
            TAc.OK()
            print('\n')
            matchWin += 1
        else:
            TAc.NO()
            print('\n')
    elif ENV['commitment'] == 'give_coloring':
        print(LANG.render_feedback("give_coloring", f"# ? Enter a color in the form of a number for each node separated by a space: "))
        buffer = TALinput(
            str,
            num_tokens=numNodes,
            regex=r"^([1-9]|1[0-9]|20)$",
            regex_explained=f"a sequence of {numNodes} numbers from 1 to {colorsNum} separeted by a space. An example is: '1 2 1'.",
            TAc=TAc
        )
        colors = [int(i) for i in buffer]
        if len(set(colors)) > colorsNum:
            TAc.print(LANG.render_feedback("wrong-colors-num", f"NO! You can't use more than {colorsNum} colors\n"), "red", ["bold"])
        else:
            result = Utilities.isSafeColored(graph, colors)
            if result:
                TAc.OK()
                print('\n')
                matchWin += 1
            else:
                TAc.NO()
                print('\n')
    elif ENV['commitment'] == 'give_minimal_uncolorable_induced_subgraph':
        print(LANG.render_feedback("give_violated_arc", "# ? Insert the arcs of the minimal uncolorable induced subgraph like a tuple of the two nodes connected by that arc, if the graph itself is already the minimum uncolorable induced one insert an empty line."))
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
                TAc.print(LANG.render_feedback("wrong-subgraph", f"NO! This is not a valid subgraph\n"), "red", ["bold"])
                matchWin -= 1
            elif not Utilities.isInducedSubgraph(graph, arcsSubgraph):
                TAc.print(LANG.render_feedback("wrong-induced-subgraph", f"NO! This is not a valid induced subgraph\n"), "red", ["bold"])
                matchWin -= 1
            else:
                subgraph = Utilities.arcsListToGraph(arcsSubgraph)
        else:
            subgraph = graph
            isBipartite = Utilities.isBipartite(subgraph)
            if isBipartite:
                TAc.print(LANG.render_feedback("wrong-induced-subgraph-colorable", f"NO! This is {colorsNum}-colorable\n"), "red", ["bold"])
                matchWin -= 1
            elif colorsNum < len(subgraph) - 1:
                minimalArcsSubgraph, colors = Utilities.getNotKColorableSubgraph(graph, colorsNum, len(subgraph) - 1)
                if minimalArcsSubgraph:
                    TAc.print(LANG.render_feedback("wrong-induced-subgraph-minimal", f"NO! This is not minimal not {colorsNum}-colorable induced subgraph\n"), "red", ["bold"])
                    matchWin -= 1
        
        TAc.OK()
        print('\n')
        matchWin += 1
    elif ENV['goal'] == 'give_coloring_or_minimal_uncolorable_induced_subgraph':
        print(LANG.render_feedback("give_violated_arc", "# ? Insert the arcs of the minimal uncolorable induced subgraph like a tuple of the two nodes connected by that arc, if the graph is uncorable insert colors in the form of a number for each node separated by a space"))
        buffer = TALinput(
            str,
            regex=r"^(\(([0-9][0-9]{0,2}|1000),([0-9][0-9]{0,2}|1000)\)|[1-9]|1[0-9]|20)$",
            regex_explained="a sequence of colors or of tuple with number from 0 to " + str(numNodes - 1) + " separated by spaces. An example is: '(1,2) (3,4)'.",
            TAc=TAc
        )
        if buffer[0] == '(':
            buffer = list(filter(None, buffer))
            arcsSubgraph = [make_tuple(i) for i in buffer]

            if arcsSubgraph:
                if not Utilities.isSubgraph(graph, arcsSubgraph):
                    TAc.print(LANG.render_feedback("wrong-subgraph", f"NO! This is not a valid subgraph"), "red", ["bold"])
                    matchWin -= 1
                elif not Utilities.isInducedSubgraph(graph, arcsSubgraph):
                    TAc.print(LANG.render_feedback("wrong-induced-subgraph", f"NO! This is not a valid induced subgraph"), "red", ["bold"])
                    matchWin -= 1
                subgraph = Utilities.arcsListToGraph(arcsSubgraph)
            else:
                subgraph = graph

                isBipartite = Utilities.isBipartite(subgraph)
                if isBipartite:
                    TAc.print(LANG.render_feedback("wrong-induced-subgraph-colorable", f"NO! This is {colorsNum}-colorable"), "red", ["bold"])
                    matchWin -= 1
                elif colorsNum < len(subgraph) - 1:
                    minimalArcsSubgraph, colors = Utilities.getNotKColorableSubgraph(graph, colorsNum, len(subgraph) - 1)
                    if minimalArcsSubgraph:
                        TAc.print(LANG.render_feedback("wrong-induced-subgraph-minimal", f"NO! This is not minimal not {colorsNum}-colorable induced subgraph"), "red", ["bold"])
                        matchWin -= 1
            TAc.OK()
            print()
        else:
            colors = [int(i) for i in buffer]
            if len(set(colors)) > colorsNum:
                TAc.print(LANG.render_feedback("wrong-colors-num", f"NO! You can't use more than {colorsNum} colors"), "red", ["bold"])
            else:
                result = Utilities.isSafeColored(graph, colors)
                if result:
                    TAc.OK()
                    print()
                else:
                    matchWin -= 1
                    TAc.print(LANG.render_feedback("wrong-colors-num", f"NO! The graph is not {colorsNum}-colorable so you have to insert the minimal uncolorable induced subgraph"), "red", ["bold"])
        matchWin += 1

    matchDone += 1
    if ENV['goal'] == 'linear':
        numNodes = round(numNodes * 1.2)
        numArcs = round(numArcs * 1.2)

print('#end')
print(LANG.render_feedback("matches-statistics", f"# Statistics:\n#   Matches won: {matchWin}/{num_matches}"))
