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
    
    #per isSC
    def DFSUtil(self, v, visited): 
        visited[v] = True
        for node in self.graph[v]: 
            if visited[node] == False: 
                self.DFSUtil(node, visited) 

    #per printSCCs
    def DFSUtility(self, v, visited): 
        visited[v] = True
        cfc = [v]
        #print (v, end=" ") 
        for node in self.graph[v]: 
            if visited[node] == False: 
                cfc += self.DFSUtility(node, visited)
        return cfc
  
    def getTranspose(self): 
        gr = Graph(self.V) 
        for node in range(self.V): 
            for child in self.graph[node]: 
                gr.addEdge(child, node) 
        return gr 

    def fillOrder(self,v,visited, stack):
        visited[v]= True
        for i in self.graph[v]:
            if visited[i]==False:
                self.fillOrder(i, visited, stack)
        stack = stack.append(v)
  
    def isSC(self): 
        visited = [False] * (self.V) 
        v = 0
        for v in range(self.V): 
            if len(self.graph[v]) > 0: 
                break
        self.DFSUtil(v, visited)  
        for i in range(self.V): 
            if visited[i] == False: 
                return False
        gr = self.getTranspose() 
        visited = [False] * self.V 
        gr.DFSUtil(v, visited) 
        for i in range(self.V): 
            if visited[i] == False: 
                return False
        return True

    #aggiunto per stampa scc
    def printSCCs(self):
        stack = []
        SCCs = []
        visited =[False]*(self.V)
        for i in range(self.V):
            if visited[i]==False:
                self.fillOrder(i, visited, stack)
        gr = self.getTranspose()
        visited =[False]*(self.V)
        while stack:
             i = stack.pop()
             if visited[i]==False:
                SCCs.append(gr.DFSUtility(i, visited))
        return SCCs

#per confronto input e cfc con permutazione
def contaspazi(s):
    count=0
    for i in s:
        if i == ' ':
            count=count+1
    return count

def permuta(s):
    a = sorted(s)
    s = "".join(a)
    return s
#####################

def GenerateGraph(seed):
    if seed == "random_seed":
        a = random.randrange(10000,80000)
        random.seed(a)
    if seed != "random_seed":
        a = seed
        random.seed(int(seed))
		
    n = random.randrange(4, 6)
    m = random.randrange(4, 8)
	
    g = Graph(n)
    graph_print = f"{n} {m}\n"
    edges = ""

    for i in range(m):
        head = random.randrange(0,n-1)
        tail = random.randrange(0,n-1)
        g.addEdge(head,tail)

        graph_print = graph_print+f"{head} {tail}\n"
        edges = edges+f"{head} {tail}-"

    return g,graph_print,edges, m, a
