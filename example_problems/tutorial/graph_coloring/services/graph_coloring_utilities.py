#!/usr/bin/env python3
import random
import itertools


def generateGraph(numNodes: int, numArcs: int, seed: int):
    random.seed(seed)
    graph = [ [0] * numNodes for _ in range(numNodes) ]
    maxArcs = (numNodes / 2) * (numNodes - 1)
    arcsList = set()
    while len(arcsList) <= numArcs and len(arcsList) <= maxArcs:
        arcsList.add(tuple(random.sample(range(numNodes), k=2)))
    for nodeX, nodeY in arcsList:
        graph[nodeX][nodeY] = 1
        graph[nodeY][nodeX] = 1
    return graph


def generateBipartiteGraph(numNodes: int, numArcs: int, seed: int):
    random.seed(seed)
    sep = random.randint(round(numNodes * 0.25), round(numNodes * 0.75))
    maxArcs = sep * (numNodes - sep)
    graph = [ [0] * numNodes for _ in range(numNodes) ]
    arcsList = set()
    while len(arcsList) <= numArcs and len(arcsList) <= maxArcs:
        arcsList.add((random.randint(0, sep - 1), random.randint(sep, numNodes - 1)))
    for nodeX, nodeY in arcsList:
        graph[nodeX][nodeY] = 1
        graph[nodeY][nodeX] = 1
    return graph


def isBipartite(graph: list):
    colorArr = [-1 for i in range(len(graph))]
    for i in range(len(graph)):
        if colorArr[i] == -1:
            queue = []
            queue.append(i)
            while queue:
                u = queue.pop()
                if graph[u][u] == 1:
                    return False
                for v in range(len(graph)):
                    if (graph[u][v] == 1 and
                            colorArr[v] == -1):
                        colorArr[v] = 1 - colorArr[u]
                        queue.append(v)
                    elif (graph[u][v] == 1 and
                        colorArr[v] == colorArr[u]):
                        return False
            return True
    return True


def isSafeColored(graph: list, colors: list):
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            if (graph[i][j] and colors[j] == colors[i]):
                return False
    return True


def getWrongColoringArcs(graph: list, colors: list):
    wrongArcs = set()
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            if graph[i][j] and colors[j] == colors[i] and ((i, j)[::-1] not in wrongArcs):
                wrongArcs.add((i, j))
    return wrongArcs


def graphColoring(graph: list, colorsNum: int, i: int, colors: list):
    if (i == len(graph)):
        if (isSafeColored(graph, colors)):
            return colors
        return []
    for j in range(1, colorsNum + 1):
        colors[i] = j
        if (graphColoring(graph, colorsNum, i + 1, colors)):
            return colors
        colors[i] = 0
    return []


def breakGraphColoring(graph: list, colors: list, seed: int):
    wrongArcs = set()
    random.seed(seed)
    numWrongArcs = random.randint(1, len(graph) - 1)
    i = 0
    while i <= numWrongArcs:
        nodeOne = random.randint(0, len(graph) -1)
        nodeTwo = None
        while not nodeTwo:
            nodeTwo = random.randint(0, len(graph[nodeOne]) - 1)
            if nodeTwo != nodeOne and graph[nodeOne][nodeTwo] == 1:
                colors[nodeOne] = colors[nodeTwo]
                if (nodeOne, nodeTwo)[::-1] not in wrongArcs:
                    wrongArcs.add((nodeOne, nodeTwo))
            else:
                nodeTwo = None
        i += 1
    return colors, wrongArcs


def arcsListToGraph(arcs: list):
    nodes = set(item for t in arcs for item in t)
    tmp = {}
    i = 0
    for node in nodes:
        tmp[node] = i
        i += 1
    graph = [ [0] * len(nodes) for _ in range(len(nodes)) ]
    for nodeX, nodeY in arcs:
        nodeX = tmp.get(nodeX)
        nodeY = tmp.get(nodeY)
        graph[nodeX][nodeY] = 1
        graph[nodeY][nodeX] = 1
    return graph


def isSubgraph(graph: list, subgraph: list):
    for nodeX, nodeY in subgraph:
        if not graph[nodeX][nodeY] and not graph[nodeY][nodeX]:
            return False
    return True


def isInducedSubgraph(graph: list, subgraph: list):
    nodesOfSubgraph = set(item for t in subgraph for item in t)
    for nodeX in nodesOfSubgraph:
        for nodeY in nodesOfSubgraph:
            if nodeX != nodeY and graph[nodeX][nodeY] and not ((nodeX, nodeY) in subgraph or (nodeY, nodeX) in subgraph):
                return False
    return True


def getInducedSubgraph(graph: list, subNodes: list):
    subgraph = set()
    for nodeX in subNodes:
        for nodeY in subNodes:
            if nodeX != nodeY and graph[nodeX][nodeY] and (nodeX, nodeY)[::-1] not in subgraph:
                subgraph.add((nodeX, nodeY))
    return list(subgraph)


def getNotKColorableSubgraph(graph: list, k: int, numSubNodes: int):
    for subNodes in itertools.combinations(range(len(graph)), numSubNodes):
        arcsSubgraph = getInducedSubgraph(graph, subNodes)
        subgraph = arcsListToGraph(arcsSubgraph)
        if len(subgraph) == numSubNodes:
            if k == 2:
                if isBipartite(graph):
                    colors = [0 for i in range(len(subgraph))]
                    colors = graphColoring(subgraph, k, 0, colors)
                    if colors:
                        return arcsSubgraph, colors
            else:
                colors = [0 for i in range(len(subgraph))]
                colors = graphColoring(subgraph, k, 0, colors)
                if colors:
                    return arcsSubgraph, colors
    return [], []