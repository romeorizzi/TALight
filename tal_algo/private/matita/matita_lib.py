#!/usr/bin/env python3
# LIBRARY: matita_lib.py   last change: 24-04-2023   author: Romeo Rizzi

from sys import stdin, stdout, stderr
import random

from rand_graphs import Graph

class Matita_Graph(Graph):

    # override as_str() method
    def as_str(self, node_names_starting_from = 0):
        ret = f"{str(self.n)} {str(self.m)} {str(self.start +node_names_starting_from)} {str(self.stop +node_names_starting_from)}"
        for (u, v) in self.E:
             for _ in range(self.E[(u, v)]):
                 ret += f"\n{u +node_names_starting_from} {v +node_names_starting_from}"
        return ret

    # override load_from_stdin() method
    def load_from_stdin(self, input_node_names_start_from = 0):
        self.n, self.m, self.start, self.stop = map(int, input().strip().split())
        self.start -= input_node_names_start_from; self.stop -= input_node_names_start_from
        self.E = {}
        for _ in range(self.m):
            u, v = map(int, input().strip().split())
            u -= input_node_names_start_from; v -= input_node_names_start_from
            if (u, v) in self.E:
                self.E[ (u, v) ] += 1
            else:
                self.E[ (u, v) ] = 1

    # extend set_up() method
    def set_up(self, n, E, start, stop, input_node_names_start_from = 0):
        self.start = start - input_node_names_start_from
        self.stop = stop - input_node_names_start_from
        super().set_up(n, E, input_node_names_start_from)

    # extend shuffle method
    def shuffle(self, keep_edge_directions = False):
        nodes_perm = super().shuffle(keep_edge_directions)
        self.start = nodes_perm[self.start]
        self.stop = nodes_perm[self.stop]


    def init_Euler_path_simple(self, n, m, allow_less_edges = True):
        """Quando allow_less_edges=False questa procedura può fallire (brutalmente, con un assert), altrimenti può tornare un grafo con meno archi di quanti richiesti con un WARNING in tal senso su stderr. Tuttavia è improbabile questo succeda per grafi sparsi (ancora più improbabile quando n dispari, dove l'unico modo per bloccarsi è sul nodo 0 avendo esaurito tutti gli archi in esso incidenti). La procedura è molto efficiente quando si richieda di produrre un grafo Euleriano sparso, ma diventa via via più inefficiente (ed a rischio di produrre la situazione di stallo di cui sopra) all'aumentare del parametro m per n fissato."""
        # assert n % 2 == 1
        self.n = n        
        self.m = m
        assert m <= n * (n - 1)
        self.E = {}
        # Inizia prendendo il cammino Hamiltoniano 0,1,...,n-1, per garantire la connessione:
        #path = []
        for i in range(n-1):
            self.E[ (i, i+1) ] = 1
            #path.append(i+1)
        self.start = 0
        curr = n - 1
        # E poi prolunga il cammino con un random walk dalla posizione corrente, evitando di prendere lati già presi. Per accorgerci che siamo bloccati in un nodo utilizziamo il vettore dei gradi:
        d = [2] * n; d[0] = d[n-1] = 1
        for i in range(n-1, m):
            if d[curr] == n - 1:
                assert allow_less_edges
                self.m = len(self.E)
                break                
            next = curr
            while next == curr  or  (curr, next) in self.E  or  (next, curr) in self.E:
                next = random.randrange(n)
            self.E[ (curr, next) ] = 1
            d[curr] += 1; d[next] += 1
            curr = next
            #path.append(next)
            #print(f"{path=}")
        self.stop = curr    

    def solve_matita(self):
        """  adapted and translated in python (2023) from Romeo Rizzi e Andrea Cracco 2016
             Approccio DFS, ma senza ricorsione (uso stack).
        """
        #print(f"entered in solve on a graph with {self.n=},  {self.m=}, {self.start=},  {self.stop=}", file = stderr)
        self.set_up_star_representation()
        #print(f"{self.neigh=}", file = stderr)
        used = [False] * self.m
        reversed_path_as_stack = [self.stop]; last_printed_node = None
        while len(reversed_path_as_stack) > 0:
            v = reversed_path_as_stack[-1]
            while len(self.neigh[v]) > 0:
                if used[self.neigh[v][-1][1]]:
                    self.neigh[v].pop()
                else:
                    next_v = self.neigh[v][-1][0]
                    name_e = self.neigh[v][-1][1]
                    self.neigh[v].pop()
                    used[name_e] = True
                    reversed_path_as_stack.append(next_v)
                    #print(f"{reversed_path_as_stack=}", file = stderr)
                    v = next_v
            if last_printed_node != None:
                print(f"{last_printed_node + 1} {v + 1}")
                #print(f"submitting edge {last_printed_node + 1} {v + 1}", file = stderr)
            last_printed_node = v
            reversed_path_as_stack.pop()
            #print(f"{reversed_path_as_stack=}", file = stderr)
        #print(f"exiting solve on a graph with {self.n=},  {self.m=}", file = stderr)
        
    def check_Eulerian_path(self, path, path_node_names_start_from = 1):
        #print(f"entering check_Eulerian_path on a graph with {self.n=},  {self.m=},  {self.start=},  {self.stop=}", file = stderr)
        curr = self.start + path_node_names_start_from
        used_edges = set({})
        for i in range(1, 1 + self.m):
            u, v = path[i - 1]
            problem_with_edge = f"We have a problem with edge {i}, namely {path[i - 1]},  in your path. It prescribes to move the pencil from node {u} to node {v}, namely {path[i - 1]}. "
            context = "\nThe whole sequence of edge traversals up to here in your path is:\n{path[:i - 1]}\nthe input instance was:\n{self.as_str(node_names_starting_from = 1)}"
            if u != curr:
                #print(f"{u=} != {curr=}", file = stderr)
                return False, problem_with_edge + f"However, the pencil currently is on node {curr}!" + context
            if not self.adjacent(u - path_node_names_start_from, v - path_node_names_start_from):
                #print(f"not self.adjacent({u=}, {v=})", file = stderr)
                return False, problem_with_edge + f"However, the input graph does not contain such an edge!" + context               
            if (u, v) in used_edges:
                #print(f"{(v, u)=} in used_edges", file = stderr)
                return False, problem_with_edge + f"However, this edge of the input graph has already been traversed (in the same direction)!" + context
            if (v, u) in used_edges:
                #print(f"{(v, u)=} in used_edges", file = stderr)
                return False, problem_with_edge + f"However, this edge of the input graph has already been traversed (in the opposite direction)!" + context
            used_edges.add( (u, v) )
            curr = v
            #print(f"the edge {(u, v)} is good", file = stderr)
        if curr != self.stop + path_node_names_start_from:
            #print(f"{curr=} != {self.stop + path_node_names_start_from=}", file = stderr)
            return False, problem_with_edge + f"The problem is that this should be the last edge but it leads to a node ({curr}) that differs from the prescribed destination node ({self.stop})! The whole sequence of nodes visited by your path is:\n{path}\nthe input instance was:\n{self.as_str(node_names_starting_from = 1)}"
        #print(f"returning True on check solution for a graph with {self.n=},  {self.m=}", file = stderr)
        return True, ""




if __name__ == "__main__":
  print(WARNING)   
  n, m = map(int, input("N, M = ").strip().split())
  G = Matita_Graph()
  G.init_Euler_path_simple(n, m)
  G.display(node_names_starting_from = 1, out = stderr)
  G.shuffle()
  G.display(node_names_starting_from = 1, out = stderr)
  print("Admits the following Eulerian path:")
  G.solve_matita()
  
