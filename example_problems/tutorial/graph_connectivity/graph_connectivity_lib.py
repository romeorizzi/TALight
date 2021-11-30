<<<<<<< HEAD
#!/usr/bin/env python3
  
from collections import defaultdict 
import random 
from sys import stderr, exit
import networkx as nx
import matplotlib.pyplot as plt

class Graph(): 
  
    def __init__(self, vertices:int): 
        """Constructor: contains number of nodes (V) and a list of arcs """
        self.V = vertices 
        self.graph = defaultdict(list) 

    def add_edge(self, v:int, u:int): 
        """Add one undirected arc to the graph"""
        self.graph[v].append(u) 
        self.graph[u].append(v) 

    def to_string(self):
        """Returns a string containing the list of all arcs"""
        import json
        return json.dumps(self.graph)

    def check_edge(self, v:int, u:int):
        """Checks if an (u,v) arc exists"""
        if u == 0 and v == 0:
            return True

        if u in self.graph[v] and v in self.graph[u]:
            return True
        return False

    def list_not_connected_edges(self):
        """Returns a list containing all the non-existent arcs"""
        list_nc = []

        for v in range(self.V):
            for u in range(self.V):
                if not self.check_edge(v, u):
                    list_nc.append((v, u))
        return list_nc

    def list_connected_edges(self):
        """Returns a list containing all the existent arcs"""
        list_c = []
        counter = 0
        for v in range(self.V):
            for u in range(self.V):
                if self.check_edge(v, u):
                    list_c.append((v, u))
                    counter = counter +1
        return list_c

    def dfs_util(self, v:int, visited:list): 
        """DFS with v initial node"""
        visited[v] = True
        for node in self.graph[v]: 
            if visited[node] == False: 
                self.dfs_util(node, visited)
                
    def is_connected(self, return_not_connected=False):
        """Return if the graph is connected or not, by using DFS"""
        v = 0
        visited = [False] * (self.V)
        not_conn = []

        self.dfs_util(v, visited)
        for i in range(self.V): 
            if not visited[i]:
                not_conn.append(i)
        #sys.stderr.write(f"visited: {visited}\n")
        #sys.stderr.write(f"len not_conn: {len(not_conn)}\n")

        if(len(not_conn) != 0):
            if(return_not_connected):
                return False, not_conn
            else:
                return False, []
        return True, []

    def dfs_spanning(self, v:int, dad:int, visited:list): 
        """DFS that keeps track of visited nodes"""
        visited[v] = dad

        for node in self.graph[v]: 
            if visited[node] == -1: 
                self.dfs_spanning(node, v, visited) 

    def spanning_tree(self):
        """Returns:
        - the spanning tree in the form of a routing table
        - list of nodes not touched by the spanning tree"""  
        v = 0
        visited = [-1] * (self.V)

        spanning_tree = []
        not_visited = []

        self.dfs_spanning(v, v, visited)
        for i in range(self.V): 
            if visited[i] == -1:
                not_visited.append(i)
            else:
                spanning_tree.append((i, visited[i]))
        
        return spanning_tree, not_visited

# SECTION GENERATORS:

def generate_tree_edges(prufer:list,m:int, g:Graph):
    """Generating a labelled tree via Prufer's proof of Cayley's theorem"""
    vertices = m + 2
    graph_print = ""

    # Initialize the array of vertices
    vertex_set = [0] * vertices

    # Counting Number of occurrences of vertex in code
    for i in range(vertices - 2):
        vertex_set[prufer[i]] += 1

    # Find the smallest label not present in prufer[].
    for i in range(vertices - 2):
        for j in range(vertices):
            # If j+1 is not present in prufer set
            if (vertex_set[j] == 0):
                # Remove from Prufer set and add the pair to the graph
                vertex_set[j] = -1

                g.add_edge(j, prufer[i])

                vertex_set[prufer[i]] -= 1

                graph_print = graph_print+f"{j} {prufer[i]}\n"
                break
    
    # For the last element
    j = 0
    head = -1
    for i in range(vertices):
        if (vertex_set[i] == 0 and j == 0):
            head = i
            j += 1
        elif (vertex_set[i] == 0 and j == 1):
            g.add_edge(head, i)
            graph_print = graph_print + f"{head} {i}\n"
            break

    return g, graph_print

def is_connected_seed(seed:int):
    """Returns True if the given seed would generate a connected graph, False otherwise."""
    # We reserve those seed divisible by 3 to the NOT solvable instances
    return (seed % 3) != 0


def gen_instance_seed(connected=None):
    """This function returns a random seed to generate a graph instance with the specificated connectivity."""
    random.seed(None)
    seed = random.randint(10002, 99999)
    # Check connectedness requirement:
    if connected == None:
        return seed
    # ajust seed if not suitable:
    if connected != is_connected_seed(seed):
        # We reserve those seed divisible by 3 to the NOT connected graphs
        if connected:
            seed -= random.randrange(1, 3)   
        else:
            seed -= (seed % 3)  
    return seed

def generate_connected_graph(n:int, m:int, TAc, LANG):
    """Generates a connected graph by creating a labelled tree and adds some additional arcs"""
    if(m < n- 1):
        TAc.print(LANG.render_feedback("m-too-small", f'Error: I can not generate a connected graph over n={n} nodes and with only m={m} edges.'), "yellow", ["bold"])
        exit(0)
    if (n * n-1)/2 < m:
            TAc.print(LANG.render_feedback("m-too-big", f'Error: m is too big. I can\'t generate a non-connected graph. Try to give me a lower m value'), "red", ["bold"])
            exit(0)
                
    g = Graph(n)

    length = n-2 # m
    arr = [0] * length

    # Generate a random array
    for i in range(length):
        arr[i] = random.randint(0, length + 1) # tolgo il +1?

    g, graph_print = generate_tree_edges(arr, length, g)

    # Randomly add arcs until you reach m
    for i in range(m-length-1):
        head, tail = random.choice(g.list_not_connected_edges())
        g.add_edge(head, tail)
        #graph_print += "---\n"
        graph_print = graph_print+f"{head} {tail}\n"

    return g, graph_print

def generate_non_connected_graph(n:int, m:int, TAc, LANG):
    """Generates a non connected graph by creating two separated connected graphs"""
    if(n < 2):
        TAc.print(LANG.render_feedback("n-only-one", f'Error: I can not generate a NOT connected graph with only one node.'), "red", ["bold"])
        exit(0)
    tmp_n = int(n/2)
    tmp_m = int(m/2)
    g3 = Graph(n)
    graph_print3 = ""

    #check that the number of arcs is greater than m
    if(((tmp_n * (tmp_n-1))/2 + ((n-tmp_n) * (n-tmp_n-1))/2 < m)): #particular case
        if (n-1 * n-2)/2 < m:
            TAc.print(LANG.render_feedback("m-too-big", f'Error: m is too big. I can\'t generate a non-connected graph. Try to give me a lower m value'), "red", ["bold"])
            exit(0)

        g1, graph_print1 = generate_connected_graph(n-1,m-1, TAc, LANG) 

        s = graph_print1.split('\n')
        for elem in s:
            if not elem == '':
                head,tail = [int(temp)for temp in elem.split() if temp.isdigit()]
                #print(str(head) + " " +str(tail))
                g3.add_edge(head,tail)
                graph_print3 = graph_print3+f"{head} {tail}\n"
                # Adding the last node
        g3.add_edge(n-1,n-1)
        graph_print3 = graph_print3+f"{n-1} {n-1}\n"
    else:
        #common case
        #generate two graphs
        '''print("tmp_n= " + str(tmp_n) + " tmp_m= " + str(tmp_m))
        print("n-tmp_n= " + str(n-tmp_n) + " m-tmp_m= " + str(m-tmp_m))'''

        g1, graph_print1 = generate_connected_graph(tmp_n, tmp_m, TAc, LANG)
        g2, graph_print2 = generate_connected_graph(n-tmp_n, m-tmp_m, TAc, LANG)
        
        #first possible solution using the list_connected_edges() function
        '''
        for head, tail in g1.list_connected_edges():
            g3.add_edge(head,tail)
            graph_print3 = graph_print3+f"{head} {tail}\n"
        for head, tail in g2.list_connected_edges():
            g3.add_edge(head+tmp_n,tail+tmp_n)
            graph_print3 = graph_print3+f"{head+tmp_n} {tail+tmp_n}\n"

        '''

        #second solution
        s = graph_print1.split('\n')

        for elem in s:
            if not elem == '':
                head,tail = [int(temp)for temp in elem.split() if temp.isdigit()]
                #print(str(head) + " " +str(tail))
                g3.add_edge(head,tail)
                graph_print3 = graph_print3+f"{head} {tail}\n"

        s = graph_print2.split('\n')
        for elem in s:
            if not elem == '':
                head,tail = [int(temp)for temp in elem.split() if temp.isdigit()]
                #print(str(head) + " " +str(tail))
                g3.add_edge(head+tmp_n,tail+tmp_n)
                graph_print3 = graph_print3+f"{head+tmp_n} {tail+tmp_n}\n"

    return g3, graph_print3

def generate_graph(n:int, m:int, seed:int, TAc, LANG):
    """Generates a graph given n, m and seed."""
    random.seed(seed)
    if is_connected_seed(seed): # Generate connected graph
        g, graph_print = generate_connected_graph(n, m, TAc=TAc, LANG=LANG) 
    else: # Generate NOT connected graph
        g, graph_print = generate_non_connected_graph(n, m, TAc=TAc, LANG=LANG)
    
    return g, graph_print, g.list_connected_edges()

if __name__ == "__main__":

    n=8
    m=11
    grafo, gp, boh = generate_graph(n, m, seed=gen_instance_seed(True), TAc=None, LANG=None)
    print(gp)

    print(grafo.is_connected(return_not_connected=True))
    '''

    n=7
    m=10
    grafo,gp = generate_connected_graph(n, m)
    print(gp)
    '''

    
    G = nx.Graph() # For networkx 

    for u, v in grafo.list_connected_edges():
        G.add_edge(u, v)

    nx.draw(G, with_labels = True)
    plt.show()
=======
#!/usr/bin/env python3
  
from collections import defaultdict 
import random 
from sys import stderr, exit
import networkx as nx
import matplotlib.pyplot as plt

class Graph(): 
  
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = defaultdict(list) 

    def addEdge(self, v, u): 
        self.graph[v].append(u) 
        #self.graph[u].append(v) 

    def tostring(self):
        import json
        return json.dumps(self.graph)


    def checkEdge(self, v, u):
        if u == 0 and v == 0:
            return True

        if u in self.graph[v]:
            return True
        return False

    def listNotConnectedEdges(self):
        list_nc = []

        for v in range(self.V):
            for u in range(self.V):
                if not self.checkEdge(v, u):
                    list_nc.append((v, u))
        return list_nc

    def listConnectedEdges(self):
        list_c = []
        counter = 0
        for v in range(self.V):
            for u in range(self.V):
                if self.checkEdge(v, u):
                    list_c.append((v, u))
                    counter = counter +1
        return list_c

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
        not_conn = []

        self.DFSUtil(v, visited)
        for i in range(self.V): 
            if not visited[i]:
                not_conn.append(i)
        
        import sys
        sys.stderr.write(f"visited: {visited}\n")
        sys.stderr.write(f"len not_conn: {len(not_conn)}\n")

        if(len(not_conn) != 0):
            if(return_not_connected):
                return False, not_conn
            else:
                return False, []
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


# SECTION GENERATORS:

'''
Generating a labelled tree via Prufer's proof of Cayley's theorem
'''
def generateTreeEdges(prufer,m, g):
    vertices = m + 2
    graph_print = ""

    # Initialize the array of vertices
    vertex_set = [0] * vertices

    # Counting Number of occurrences of vertex in code
    for i in range(vertices - 2):
        vertex_set[prufer[i]] += 1

    # Find the smallest label not present in prufer[].
    for i in range(vertices - 2):
        for j in range(vertices):
            # If j+1 is not present in prufer set
            if (vertex_set[j] == 0):
                # Remove from Prufer set and add the pair to the graph
                vertex_set[j] = -1

                g.addEdge(j, prufer[i])

                vertex_set[prufer[i]] -= 1

                graph_print = graph_print+f"{j} {prufer[i]}\n"
                break
    
    # For the last element
    j = 0
    head = -1
    for i in range(vertices):
        if (vertex_set[i] == 0 and j == 0):
            head = i
            j += 1
        elif (vertex_set[i] == 0 and j == 1):
            g.addEdge(head, i)
            graph_print = graph_print + f"{head} {i}\n"
            break

    return g, graph_print

def is_connected_seed(seed):
    """Returns True if the given seed would generate  a connected graph, False otherwise."""
    # We reserve those seed divisible by 3 to the NOT solvable instances
    return (seed % 3) != 0


def gen_instance_seed(connected=None):
    """This function returns a random seed to generate a pirellone instance with the specificated connectivity."""
    random.seed(None)
    seed = random.randint(100002,999999)
    # Check connectedness requirement:
    if connected == None:
        return seed
    # ajust seed if not suitable:
    if connected != is_connected_seed(seed):
        # We reserve those seed divisible by 3 to the NOT connected graphs
        if connected:
            seed -= random.randrange(1, 3)   
        else:
            seed -= (seed % 3)  
    return seed
        



def GenerateConnectedGraph(n:int, m:int, TAc, LANG):
    if(m < n-1):
        TAc.print(LANG.render_feedback("m-too-small", f'Error: I can not generate a connected graph over n={n} nodes and with only m={m} edges.'), "yellow", ["bold"])
        exit(0)
                
    g = Graph(n)

    length = n-2 # m
    arr = [0] * length

    # Genero un array randomico
    for i in range(length):
        arr[i] = random.randint(0, length + 1) # tolgo il +1?

    g, graph_print = generateTreeEdges(arr, length, g)

    # Aggiungo casualmente archi fino ad arrivare a m
    for i in range(m-length-1):
        head, tail = random.choice(g.listNotConnectedEdges())
        g.addEdge(head, tail)
        #graph_print += "---\n"
        graph_print = graph_print+f"{head} {tail}\n"

    return g, graph_print

def GenerateNonConnectedGraph(n, m, TAc, LANG):
    if(n < 2):
        TAc.print(LANG.render_feedback("n-only-one", f'Error: I can not generate a NOT connected graph with only one node.'), "yellow", ["bold"])
        exit(0)
    tmp_n = int(n/2)
    tmp_m = int(m/2)
    g3 = Graph(n)
    graph_print3 = ""

    # Controllo che il numero di archi sia maggiore rispetto a m
    if(((tmp_n * (tmp_n-1)) + ((n-tmp_n) * (n-tmp_n-1)) < m)): #casoparticolare
        g1, graph_print1 = GenerateConnectedGraph(n-1,m, TAc, LANG) 
        
        

        s = graph_print1.split('\n')
        for elem in s:
            if not elem == '':
                head,tail = [int(temp)for temp in elem.split() if temp.isdigit()]
                #print(str(head) + " " +str(tail))
                g3.addEdge(head,tail)
                graph_print3 = graph_print3+f"{head} {tail}\n"

    else:
        #casonormale
        #creo due grafi
        '''print("tmp_n= " + str(tmp_n) + " tmp_m= " + str(tmp_m))
        print("n-tmp_n= " + str(n-tmp_n) + " m-tmp_m= " + str(m-tmp_m))'''

        g1, graph_print1 = GenerateConnectedGraph(tmp_n, tmp_m, TAc, LANG)
        g2, graph_print2 = GenerateConnectedGraph(n-tmp_n, m-tmp_m, TAc, LANG)
        
        print(g1.listConnectedEdges())
        print("---")
        print(graph_print1)


        #prima possibile soluzione utilizzando la funzione listConnectedEdges()
        '''
        for head, tail in g1.listConnectedEdges():
            g3.addEdge(head,tail)
            graph_print3 = graph_print3+f"{head} {tail}\n"
        for head, tail in g2.listConnectedEdges():
            g3.addEdge(head+tmp_n,tail+tmp_n)
            graph_print3 = graph_print3+f"{head+tmp_n} {tail+tmp_n}\n"

        '''

        #seconda soluzione
        s = graph_print1.split('\n')

        for elem in s:
            if not elem == '':
                head,tail = [int(temp)for temp in elem.split() if temp.isdigit()]
                #print(str(head) + " " +str(tail))
                g3.addEdge(head,tail)
                graph_print3 = graph_print3+f"{head} {tail}\n"

        s = graph_print2.split('\n')
        for elem in s:
            if not elem == '':
                head,tail = [int(temp)for temp in elem.split() if temp.isdigit()]
                #print(str(head) + " " +str(tail))
                g3.addEdge(head+tmp_n,tail+tmp_n)
                graph_print3 = graph_print3+f"{head+tmp_n} {tail+tmp_n}\n"

    return g3, graph_print3

def generate_graph(n:int, m:int, seed:int, TAc, LANG):

    random.seed(seed)
    if is_connected_seed(seed): # Generate connected graph
        g, graph_print = GenerateConnectedGraph(n, m, TAc=TAc, LANG=LANG) 
    else: # Generate NOT connected graph
        g, graph_print = GenerateNonConnectedGraph(n, m, TAc=TAc, LANG=LANG)
    
    return g, graph_print, g.listConnectedEdges()

if __name__ == "__main__":

    n=8
    m=7
    grafo,gp = GenerateGraph("lazy", n, m, True)
    print(gp)

    print(grafo.isConnected(return_not_connected=True))
    '''

    n=7
    m=10
    grafo,gp = GenerateConnectedGraph(n, m)
    print(gp)
    '''

    
    G = nx.DiGraph() # For networkx 

    for u, v in grafo.listConnectedEdges():
        G.add_edge(u, v)

    nx.draw(G, with_labels = True)
    plt.show()
>>>>>>> 06a1e8531187c650b1a93d5a6f5a63c10e00e24d
