#!/usr/bin/env python3
  
from collections import defaultdict 
import random
  

class Graph(): 
  
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = defaultdict(list) 
        self.IN = [0] * vertices 
  
    def addEdge(self, v, u): 
        self.graph[v].append(u) 
        self.IN[u] += 1
  
    def DFSUtil(self, v, visited): 
        visited[v] = True
        for node in self.graph[v]: 
            if visited[node] == False: 
                self.DFSUtil(node, visited) 
    
  
    def getTranspose(self): 
        gr = Graph(self.V) 
        for node in range(self.V): 
            for child in self.graph[node]: 
                gr.addEdge(child, node) 
        return gr 
  
    def isSC(self): 
        visited = [False] * (self.V) 
        v = 0
        for v in range(self.V): 
            if len(self.graph[v]) > 0: 
                break
        self.DFSUtil(v, visited) 
        # If DFS traversal doesn't visit all  
        # vertices, then return false. 
        for i in range(self.V): 
            if visited[i] == False and len(self.graph[i])>0: 
                return False
        gr = self.getTranspose() 
        visited = [False] * self.V 
        gr.DFSUtil(v, visited) 
        for i in range(self.V): 
            if visited[i] == False and len(self.graph[i])>0: 
                return False
        return True
  
    def isEulerianCycle(self): 
        # Check if all non-zero degree vertices  
        # are connected 
        if self.isSC() == False: 
            return False
        # Check if in degree and out degree of  
        # every vertex is same 
        for v in range(self.V): 
            if len(self.graph[v]) != self.IN[v]: 
                return False
        return True


def printCircuit(adj):
    curr_path = [0] 
    circuit = []

    while curr_path:
        curr_v = curr_path[-1]

        if adj[curr_v]:
            next_v = adj[curr_v].pop()
            curr_path.append(next_v)
        else:
            circuit.append(curr_path.pop())
    
    for i in range(len(circuit)-1, 0, -1):
        print(circuit[i],circuit[i-1])


def GenerateGraph():
    n = random.randrange(10,20)
    m = random.randrange(10,25)

    g = Graph(n)
    graph_print = f"{n} {m}\n"
    edges = ""

    for i in range(m):
        head = random.randrange(0,n-1)
        tail = random.randrange(0,n-1)
        g.addEdge(head,tail)

        graph_print = graph_print+f"{head} {tail}\n"
        edges = edges+f"{head} {tail}-"

    return g,graph_print,edges, m

def certificateEYC (x):
    if x == 1:
    # start_node != end_node
        n = random.randrange(10,20)
        m = random.randrange(10,25)
        circuit = ""

        for i in range(m):
            if i == 0:
                start = 0
                end = random.randrange(0,n-1)
                circuit = f"{start} {end}\n"
            if i == m-1:
                start = end
                end = random.randrange(1,n-1)
                circuit = circuit+f"{start} {end}"
            if i!= 0 and i!=m-1:
                start = end
                end = random.randrange(0,n-1)
                circuit = circuit+f"{start} {end}\n"

        graph = circuit.split("\n")
        random.shuffle(graph)
        str_graph = '\n'.join(graph)
        str_graph = f"{n} {m}\n"+str_graph
        error = "Il circuito non termina nel nodo iniziale." 
        return str_graph,circuit,error

    if x == 2:
        n = random.randrange(10,20)
        m = random.randrange(10,25)
        circuit = ""
        graph = ""

        for i in range(m):
            if i == 0:
                start = 0
                end = random.randrange(0,n-1)
                circuit = f"{start} {end}\n"
                graph = f"{start} {end}\n"
            if i == m-1:
                start = end
                end = 0
                circuit = circuit+f"{start} {end}"
                graph = graph+f"{start} {n+1}"
            if i!= 0 and i!=m-1:
                start = end
                end = random.randrange(1,n-1)
                circuit = circuit+f"{start} {end}\n"
                graph = graph+f"{start} {end}\n"

        graph = graph.split("\n")
        random.shuffle(graph)
        str_graph = '\n'.join(graph)
        str_graph = f"{n} {m}\n"+str_graph
        error = "L'arco non esiste nel grafo."  
        return str_graph,circuit,error 


    if x == 3:
        n = random.randrange(10,20)
        m = random.randrange(10,25)
        circuit = ""
        graph = ""

        for i in range(m-1):
            if i == 0:
                start = 0
                end = random.randrange(0,n-1)
                circuit = f"{start} {end}\n"
                graph = f"{start} {end}\n"
            if i == m-2:
                start = end
                end = 0
                circuit = circuit+f"{start} {end}"
                graph = graph+f"{start} {end}\n{start} {end}"
            if i!= 0 and i!=m-2:
                start = end
                end = random.randrange(1,n-1)
                circuit = circuit+f"{start} {end}\n"
                graph = graph+f"{start} {end}\n"

        graph = graph.split("\n")
        random.shuffle(graph)
        str_graph = '\n'.join(graph)
        str_graph = f"{n} {m}\n"+str_graph
        error = "Il circuito non riporta il numero corretto di archi."  
        return str_graph,circuit,error        


    if x == 4:
        n = random.randrange(10,20)
        m = random.randrange(10,25)
        circuit = ""
        graph = ""

        for i in range(m):
            if i == 0:
                start = 0
                end = random.randrange(0,n-1)
                circuit = f"{start} {end}\n"
                graph = f"{start} {end}\n"
            if i == m-1:
                start = end-1
                end = 0
                circuit = circuit+f"{start} {end}"
                graph = graph+f"{start} {end}"
            if i!= 0 and i!=m-1:
                start = end
                end = random.randrange(1,n-1)
                circuit = circuit+f"{start} {end}\n"
                graph = graph+f"{start} {end}\n"

        graph = graph.split("\n")
        random.shuffle(graph)
        str_graph = '\n'.join(graph)
        str_graph = f"{n} {m}\n"+str_graph
        error = "L'arco non è collegato al precedente."  
        return str_graph,circuit,error 

 
