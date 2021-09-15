#!/usr/bin/env python3


def isSafeColored(graph: list, colors: list):
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            if (graph[i][j] and colors[j] == colors[i]):
                return False
    return True


def startAlgo():
    numNodes = None
    spoon = input().strip()
    while spoon[:len("graph:")] != "graph:":
        if spoon[:len("#   number of nodes:")] == '#   number of nodes:':
            numNodes = spoon.split(':')[1]
            numNodes = int("".join(numNodes.split()))
        spoon = input().strip()

    graph = [ [0] * numNodes for _ in range(numNodes) ]
    spoon = input().strip()
    while spoon[:len("coloring:")] != "coloring:":
        buffer = spoon.split(':')
        buffer[1] = "".join(buffer[1].split())
        buffer[1] = buffer[1].split(',')
        graph[int(buffer[0])] = [int(x) for x in buffer[1]]
        spoon = input().strip()

    colors = spoon.split(':')[1]
    colors = "".join(colors.split())
    colors = colors.split(',')
    colors = [int(x) for x in colors]
    result = isSafeColored(graph, colors)

    spoon = input().strip()
    while spoon[:len("# ?")] != "# ?":
        spoon = input().strip()
    if result:
        print('yes')
    else:
        print('no')

    spoon = input().strip()
    while spoon[:len("# ")] == "# ":
        spoon = input().strip()



spoon = input().strip()
while spoon[:len("#start")] != "#start":
    spoon = input().strip()
startAlgo()
while True:
    if spoon == '#end':
        exit(0)
    else:
        startAlgo()