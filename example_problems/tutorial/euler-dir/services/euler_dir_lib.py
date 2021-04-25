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
    
    #per gimme_scc
    def DFSUtility(self, v, visited): 
        visited[v] = True
        print (v) 
        for node in self.graph[v]: 
            if visited[node] == False: 
                self.DFSUtil(node, visited) 
  
    def getTranspose(self): 
        gr = Graph(self.V) 
        for node in range(self.V): 
            for child in self.graph[node]: 
                gr.addEdge(child, node) 
        return gr 

    #aggiunto per scc
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

    #aggiunto per stampa scc
    def printSCCs(self):
        stack = []
        visited =[False]*(self.V)
        for i in range(self.V):
            if visited[i]==False:
                self.fillOrder(i, visited, stack)
        gr = self.getTranspose()
        visited =[False]*(self.V)
        while stack:
             i = stack.pop()
             if visited[i]==False:
                gr.DFSUtility(i, visited)
                print(" ")
  
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
 
def example_graph(num):
    if num == 1:
        print("5 6\n0 1\n3 0\n3 1\n1 2\n2 3\n1 4\n4 3\n")
    if num == 2:
        print("5 5\n0 1\n1 2\n4 1\n0 3\n3 4\n")
    if num == 3:
        print("6 7\n0 1\n0 3\n1 2\n5 1\n4 2\n4 3\n5 3\n")
    if num == 4:
        print("7 6\n4 5\n5 0\n2 0\n0 6\n4 2\n6 4\n3 4\n0 1\n1 2\n2 3\n0 7\n")
    if num == 5:
        print("5 2\n4 5\n1 0\n2 1\n3 4\n0 3\n")
    if num == 6:
        print("6 7\n1 2\n7 0\n5 6\n4 5\n3 4\n0 1\n2 3\n")
    if num == 7:
        print("0 1\n1 2\n2 0\n3 2\n3 1\n3 4\n4 3\n4 5\n5 2\n5 6\n6 5\n7 4\n7 6\n7 7\n")

def example_graph_eval_euler(num):
    if num == 1:
        print("7 8\n5 6\n0 1\n3 0\n3 1\n1 2\n2 3\n1 4\n4 3\n")
    if num == 2:
        print("6 6\n5 5\n0 1\n1 2\n4 1\n0 3\n3 4\n")
    if num == 3:
        print("8 8\n6 7\n0 1\n0 3\n1 2\n5 1\n4 2\n4 3\n5 3\n")
    if num == 4:
        print("8 12\n7 6\n4 5\n5 0\n2 0\n0 6\n4 2\n6 4\n3 4\n0 1\n1 2\n2 3\n0 7\n")
    if num == 5:
        print("6 6\n5 2\n4 5\n1 0\n2 1\n3 4\n0 3\n")
    if num == 6:
        print("8 8\n6 7\n1 2\n7 0\n5 6\n4 5\n3 4\n0 1\n2 3\n")
    if num == 7:
        print("8 14\n0 1\n1 2\n2 0\n3 2\n3 1\n3 4\n4 3\n4 5\n5 2\n5 6\n6 5\n7 4\n7 6\n7 7\n")   

def scc(num):
    if num == 1:
        return "01234 5 6"
        print("01234 5 6\n")
    if num == 2:
        return "0 1 2 3 4 5"
        print("0 1 2 3 4 5\n")
    if num == 3:
        return "0 1 2 3 4 5 6 7"
        print("0 1 2 3 4 5 6 7\n")
    if num == 4:
        return "01234567"
        print("01234576\n")
    if num == 5:
        return "012345"
        print("012345\n")
    if num == 6:
        return "01234567"
        print("01234567\n")
    if num == 7:
        return "012 34 56 7"
        print("012 34 56 7\n")

def check_scc(scheck, sin):
    if scheck == sin:
        return True
    else:
        return False

def check_is_eul(num):
    if num == 1:
        return "N"
    if num == 2:
        return "N"
    if num == 3:
        return "N"
    if num == 4:
        return "N"
    if num == 5:
        return "Y"
    if num == 6:
        return "Y"
    if num == 7:
        return "N"
