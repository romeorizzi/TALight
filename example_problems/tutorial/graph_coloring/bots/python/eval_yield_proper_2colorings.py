#!/usr/bin/env python3


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
    while spoon[:len("# ?")] != "# ?":
        buffer = spoon.split(':')
        buffer[1] = "".join(buffer[1].split())
        buffer[1] = buffer[1].split(',')
        graph[int(buffer[0])] = [int(x) for x in buffer[1]]
        spoon = input().strip()

    
    result = isBipartite(graph)
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