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
        self.IN[u ] += 1
  
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
        # If DFS traversal doesn't visit all vertices, then return false. 
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
        # Check if all non-zero degree vertices are connected 
        if self.isSC() == False: 
            return False
        # Check if in degree and out degree of every vertex is same 
        for v in range(self.V): 
            if len(self.graph[v]) != self.IN[v]: 
                return False
        return True
    
    ##########################
    #### per Eulerian Walk ###

    def isConnected(self): 
        visited = [False] * (self.V) 
        v = 0
        for v in range(self.V): 
            if len(self.graph[v]) > 0: 
                break
        self.DFSUtil(v, visited) 
        # If DFS traversal doesn't visit all vertices, then return false. 
        for i in range(self.V): 
            if visited[i] == False and len(self.graph[i])>0: 
                return False
        return True
  
    def isEulerianWalk(self):
        # Check if all non-zero degree vertices are connected
        if self.isConnected() == False:
            return False
        #Count vertices with odd degree
        odd1 = 0
        odd2 = 0
        for i in range(self.V):
            if len(self.graph[i]) - self.IN[i] == 1:
                odd1 +=1
            if self.IN[i] - len(self.graph[i]) == 1:
                odd2 +=1
            if len(self.graph[i]) - self.IN[i] > 1:
                return False
            if self.IN[i] - len(self.graph[i]) > 1:
                return False
        if odd1 > 1 and odd2 > 1:
            return False
        else:
            return True

    # This function removes edge u-v from graph   
    def rmvEdge(self, u, v):
        for index, key in enumerate(self.graph[u]):
            if key == v:
                self.graph[u].pop(index)
        for index, key in enumerate(self.graph[v]):
            if key == u:
                self.graph[v].pop(index)
 
    # A DFS based function to count reachable vertices from v
    def DFSCount(self, v, visited):
        count = 1
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                count = count + self.DFSCount(i, visited)        
        return count
 
    # The function to check if edge u-v can be considered as next edge in Euler Tour
    def isValidNextEdge(self, u, v):
        # The edge u-v is valid in one of the following two cases:
  
          #  1) If v is the only adjacent vertex of u
        if len(self.graph[u]) == 1:
            return True
        else:
            '''
             2) If there are multiple adjacents, then u-v is not a bridge
                 Do following steps to check if u-v is a bridge
  
            2.a) count of vertices reachable from u'''   
            visited =[False]*(self.V)
            count1 = self.DFSCount(u, visited)
 
            '''2.b) Remove edge (u, v) and after removing the edge, count
                vertices reachable from u'''
            self.rmvEdge(u, v)
            visited =[False]*(self.V)
            count2 = self.DFSCount(u, visited)
 
            #2.c) Add the edge back to the graph
            self.addEdge(u,v)
 
            # 2.d) If count1 is greater, then edge (u, v) is a bridge
            return False if count1 > count2 else True
 
 
    # Print Euler tour starting from vertex u
    def printEulerUtil(self, u):
        #Recur for all the vertices adjacent to this vertex
        for v in self.graph[u]:
            #If edge u-v is not removed and it's a a valid next edge
            if self.isValidNextEdge(u, v):
                print("%d %d " %(u,v)),
                self.rmvEdge(u, v)
                self.printEulerUtil(v)
    
    '''The main function that print Eulerian Trail. It first finds an odd
   degree vertex (if there is any) and then calls printEulerUtil()
   to print the path '''
    def printEulerTour(self):
        #Find a vertex with odd degree
        u = 0
        for i in range(self.V):
            if len(self.graph[i]) %2 != 0 :
                u = i
                break
        # Print tour starting from odd vertex
        print ("\n")
        self.printEulerUtil(u)
############################################################
############################################################

# stampa per eulerian cycle
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


def GenerateGraph(seed,n,m):
    if seed == "random_seed":
        a = random.randrange(10000,80000)
        random.seed(a)
    if seed != "random_seed":
        a = seed
        random.seed(int(seed))

    g = Graph(n)
    graph_print = f"{n} {m}\n"
    edges = ""

    for i in range(m):
        head = random.randrange(0,n)
        tail = random.randrange(0,n)
        g.addEdge(head,tail)

        graph_print = graph_print+f"{head} {tail}\n"
        edges = edges+f"{head} {tail}-"

    return g,graph_print,edges, a

def certificateEYC (x,seed):
    if seed == "random_seed":
        a = random.randrange(10000,80000)
        random.seed(a)
    if seed != "random_seed":
        a = seed
        random.seed(int(seed))

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
        return str_graph,circuit,error,a

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
        return str_graph,circuit,error,a 


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
        return str_graph,circuit,error,a        


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
        return str_graph,circuit,error ,a

 
