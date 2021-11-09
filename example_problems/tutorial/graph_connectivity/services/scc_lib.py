#!/usr/bin/env python3
  
from collections import defaultdict 
import random
from sys import stderr, exit

class Graph(): 
  
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = defaultdict(list) 

    def addEdge(self, v, u): 
        self.graph[v].append(u) 
        self.graph[u].append(v) 

    def tostring(self):
        import json
        return json.dumps(self.graph)


    def checkEdge(self, v, u):
        if u == 0 and v == 0:
            return True

        if u in self.graph[v]:
            return True
        return False
    '''
        DFS dato nodo v di partenza
    '''
    def DFSUtil(self, v, visited): 
        visited[v] = True
        for node in self.graph[v]: 
            if visited[node] == False: 
                self.DFSUtil(node, visited) 
    '''
        Ritorna se il grafo è connesso o no, utilizzando la DFS
    '''
    def isConnected(self, return_not_connected=False):
        v = 0
        visited = [False] * (self.V)

        self.DFSUtil(v, visited)
        for i in range(self.V): 
            #print(visited[i])
            if visited[i] == False:
                return False, []
        
        if(return_not_connected):
            # listo i non connessi
            not_conn = []
            for i in range(len(visited)):
                if(not visited[i]):
                    not_conn.append(i)

            for elem in not_conn:
                print(elem)

            return True, not_conn
        return True, []

    '''
        DFS che tiene traccia dei nodi visitati
    '''
    def DFS_spanning(self, v, dad, visited): 
        visited[v] = dad

        for node in self.graph[v]: 
            if visited[node] == -1: 
                self.DFS_spanning(node, v, visited) 

    '''
        Ritorna:
        - lo spanning tree sotto forma di routing table
        - lista dei nodi non toccati dallo spanning tree
    '''
    def spanning_tree(self):  
        v = 0
        visited = [-1] * (self.V)

        spanning_tree = []
        not_visited = []

        self.DFS_spanning(v, v, visited)
        for i in range(self.V): 
            if visited[i] == -1:
                not_visited.append(i)
            else:
                spanning_tree.append((i, visited[i]))
        
        return spanning_tree, not_visited

'''
Genera un grafo dato seed, n, m 
indicando tramite parametro 'is_connected' se deve essere connesso o no
'''
def GenerateGraph(seed, n, m, is_connected):
    if seed == "lazy":
        shake = random.randrange(10000,80000)
        random.seed(shake)
    else:
        shake = seed
        random.seed(int(seed))

    while True:
        g = Graph(n)
        graph_print = f"{n} {m}\n"
        edges = ""

        for i in range(m):
            head = random.randrange(0,n)
            tail = random.randrange(0,n)
            g.addEdge(head,tail)
            
            if(i < m-1):
                graph_print = graph_print+f"{head} {tail}\n"
            else:
                graph_print = graph_print+f"{head} {tail}"
            edges = edges+f"{head} {tail}-"
        # Esco solo se il grafo generato è connesso
        if(g.isConnected()[0] == is_connected): 
            break

    return g, graph_print, edges, shake
