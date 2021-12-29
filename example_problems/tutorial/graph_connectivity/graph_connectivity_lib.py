#!/usr/bin/env python3
  
from collections import defaultdict 
import random 
from sys import stderr, exit
import networkx as nx
import matplotlib.pyplot as plt

class Graph(): 
  
    def __init__(self, num_nodes:int): 
        """Constructor: a graph is the number of its nodes (n), the number of its edges (m), and a dictionary (graph) associating to each node the list of its neighbors. The labels of the nodes are the integers in [0,n)."""
        self.n = num_nodes 
        self.m = 0 
        self.graph = defaultdict(list) 

    def add_edge(self, v:int, u:int): 
        """Add one edge to the undirected graph"""
        self.graph[v].append(u) 
        self.graph[u].append(v)
        self.m += 1

    def check_edge(self, v:int, u:int):
        """Checks if an (u,v) edge exists"""
        return  u in self.graph[v]

    def list_edges(self):
        """Returns a list containing all the existent edges"""
        #return [ (v, u) for v in range(self.n) for u in range(self.n) if self.check_edge(v, u) ]
        list = []
        for u in range(self.n):
            for v in self.graph[u]:
                if((v, u) not in list):
                    list.append((u,v))
        return list

    def list_nonedges(self):
        """Returns a list containing all the non-existent edges"""
        existent_edges = self.list_edges()
        return [ (v, u) for v in range(self.n) for u in range(self.n) if (u,v) not in existent_edges ]

    def dfs_util(self, v:int, visited:list): 
        """DFS with v initial node"""
        visited[v] = True
        for node in self.graph[v]: 
            if visited[node] == False: 
                self.dfs_util(node, visited)
                
    def is_connected(self, return_not_connected=False):
        """Return if the graph is connected or not, by using DFS"""
        v = 0
        visited = [False] * (self.n)
        not_conn = []


        self.dfs_util(v, visited)

        for i in range(self.n): 
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
        visited = [-1] * (self.n)

        spanning_tree = []
        not_visited = []

        self.dfs_spanning(v, v, visited)
        for i in range(self.n): 
            if visited[i] == -1:
                not_visited.append(i)
            else:
                spanning_tree.append((i, visited[i]))
        
        return spanning_tree, not_visited

# RENDITIONS AND VISUALIZATIONS:
    def to_str(self):
        str_rep = f"{self.n} {self.m}\n"
        for tail,head in self.list_edges():
            str_rep += f"{tail} {head}\n"
        return str_rep

    def to_json(self):
        """Returns a string containing the list of all edges"""
        import json
        return json.dumps(self.graph)

    def get_n(self):
        """Returns the number of nodes"""
        return self.n

    def get_m(self):
        """Returns the number of arcs"""
        return self.m
    
# SECTION FRIEND FUNCTIONS:

def graph_union(list_of_graphs):
    num_nodes = sum(g.n for g in list_of_graphs)
    union_graph = Graph(num_nodes)
    offset = 0 # number of previously already included nodes
    for g in list_of_graphs:
        for tail,head in g.list_edges():
            union_graph.add_edge(tail+offset, head+offset)
        offset += g.n
    return union_graph
    
# SECTION GENERATORS:

def generate_tree_edges(prufer:list,m:int, g:Graph):
    """Generating a labelled tree via Prufer's proof of Cayley's theorem"""
    num_nodes = m + 2
    graph_print = ""

    # Initialize the array of vertices
    vertex_set = [0] * num_nodes

    # Counting Number of occurrences of vertex in code
    for i in range(num_nodes - 2):
        vertex_set[prufer[i]] += 1

    # Find the smallest label not present in prufer[].
    for i in range(num_nodes - 2):
        for j in range(num_nodes):
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
    for i in range(num_nodes):
        if (vertex_set[i] == 0 and j == 0):
            head = i
            j += 1
        elif (vertex_set[i] == 0 and j == 1):
            g.add_edge(head, i)
            graph_print = graph_print + f"{head} {i}\n"
            break

    return g

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
    """When called with n-1 <= m <= (n * (n-1) )//2, this function generates and returns a simple connected graph with n nodes and m edges.
       Otherwise, it explains the problem and terminates the service.
       Generation of the graph: first creates a random labelled tree using Cayley's bijection, and then adds the m-(n-1) additional edges at random."""
    if m > (n * (n-1) )//2:
            TAc.print(LANG.render_feedback("m-too-big", f'Error: m is too big. I can\'t generate a simple graph with m={m} edges over n={n} nodes. Try to give me a smaller value for the argument m.'), "red", ["bold"])
            exit(0)
    if(m < n- 1):
        TAc.print(LANG.render_feedback("m-too-small", f'Error: I can not generate a connected graph over n={n} nodes and with only m={m} edges.'), "yellow", ["bold"])
        exit(0)
    g = Graph(n)

    length = n-2 # m
    arr = [0] * length

    # Generate a random array
    for i in range(length):
        arr[i] = random.randint(0, length + 1) # tolgo il +1?

    g = generate_tree_edges(arr, length, g)

    available_edges = g.list_nonedges()
    # Randomly add edges until you reach m
    for i in range(m-n+1):
        rnd_index = random.randrange(len(available_edges))
        g.add_edge(available_edges[rnd_index][0], available_edges[rnd_index][1])
        del available_edges[rnd_index]
    return g

def generate_disconnected_graph(n:int, m:int, TAc, LANG):
    """Generates a NOT connected graph with n nodes and m edges.
       When called with m <= ((n-1) * (n-2) )//2, such a graph exists and the function can generate and return it.
       Otherwise, the problem is explained and the service is terminated.
       Generation of the graph: by creating two (or more) separated connected graphs."""
    if m > ((n-1) * (n-2) )//2:
            TAc.print(LANG.render_feedback("m-too-big", f'Error: m is too big. I can\'t generate a simple graph with m={m} edges over n={n} nodes. Try to give me a smaller value for the argument m.'), "red", ["bold"])
            exit(0)
    descriptor_list = [] # obvious decomposition in a single connected component
    top_m = m
    top_n = n
    while top_m <= ((top_n-1) * (top_n-2))//2:
        try_n1 = random.randrange(1,(top_n//2))
        try_n2 = top_n - try_n1
        while (try_n1*(try_n1-1)//2 + try_n2*(try_n2-1)//2 < top_m):
            try_n1 -= 1
            try_n2 += 1
        max_try_m1 = try_n1*(try_n1-1)//2
        max_try_m2 = try_n2*(try_n2-1)//2
        flag=True
        while (max_try_m1 + max_try_m2 > top_m):
            if(try_n1 >= try_n2):
                max_try_m1 -=1
            else:
                max_try_m2 -=1

        min_try_m1 = top_m - max_try_m2
        while (min_try_m1 < try_n1-1):
            min_try_m1 +=1
        try_m1 = random.randint(min_try_m1,max_try_m1)
        try_m2 = top_m - try_m1
        descriptor_list.append((try_n1,try_m1))
        descriptor_list.append((try_n2,try_m2))
        top_m = descriptor_list[-1][1]
        top_n = descriptor_list[-1][0]
        if (top_m <= ((top_n-1) * (top_n-2))//2):
            descriptor_list.remove((top_n,top_m))
            
    random.shuffle(descriptor_list)

    list_of_connected_components = []
    for n_tmp,m_tmp in descriptor_list:
        list_of_connected_components.append(generate_connected_graph(n_tmp,m_tmp, TAc, LANG))
    return graph_union(list_of_connected_components)

def generate_graph(n:int, m:int, seed:int, TAc, LANG):
    """Generates the pseudo-random graph <n, m, seed>."""
    random.seed(seed)
    if is_connected_seed(seed): # Generate connected graph
        g = generate_connected_graph(n, m, TAc=TAc, LANG=LANG) 
    else: # Generate NOT connected graph
        g = generate_disconnected_graph(n, m, TAc=TAc, LANG=LANG)
    
    return g

if __name__ == "__main__":

    n=8
    m=11
    grafo= generate_graph(n, m, seed=gen_instance_seed(False), TAc=None, LANG=None)
    print(grafo.to_str())


    print(grafo.is_connected(return_not_connected=True))
    '''

    n=7
    m=10
    grafo,gp = generate_connected_graph(n, m)
    print(gp)
    '''

    
    G = nx.Graph() # For networkx 

    for u, v in grafo.list_edges():
        G.add_edge(u, v)

    nx.draw(G, with_labels = True)
    plt.show()