#!/usr/bin/env python3
  
from collections import defaultdict 
  

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
        visited = [False] * self.V 
  
        v = 0
        for v in range(self.V): 
            if len(self.graph[v]) > 0: 
                break
  
        self.DFSUtil(v, visited) 
  
        # If DFS traversal doesn't visit all  
        # vertices, then return false. 
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
 

 
