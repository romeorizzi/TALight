#!/usr/bin/env python3
# LIBRARY: rand_graphs.py   last change: 23-04-2023   author: Romeo Rizzi

WARNING = """this library is common to a few problems:
../matita
../???
Please, keep this in mind in case you want to modify it."""

from sys import stdin, stdout, stderr
import random


class Graph:

    def load_from_stdin(self, input_node_names_start_from = 0, node_weighted = False, edge_weighted = False):
        self.n, self.m = map(int, input().strip().split())
        if node_weighted:
            node_w = map(int, input().strip().split())
        self.E = {}
        if edge_weighted:
            for _ in range(self.m):
                u, v, w = map(int, input().strip().split())
                u -= input_node_names_start_from; v -= input_node_names_start_from
                self.E[ (u, v) ] = w            
        else:
            for _ in range(self.m):
                u, v = map(int, input().strip().split())
                u -= input_node_names_start_from; v -= input_node_names_start_from
                if (u, v) in self.E:
                    self.E[ (u, v) ] += 1
                else:
                    self.E[ (u, v) ] = 1

    def set_up(self, n, E, input_node_names_start_from = 0):
        self.n = n
        self.m = len(E)
        if type(E) == list:
            E = { e:1 for e in E }
        if input_node_names_start_from == 0:
            self.E = E
        else:
            self.E = {}
            for (u, v) in E:
                self.E[ (u -input_node_names_start_from, v -input_node_names_start_from) ] = E[ (u, v) ]

    def rand_directed(self, n, m, loops = False, multi = False):
        if not multi:
            assert m <= n * n if loops else m <= n * (n - 1)
        self.n = n
        self.m = m
        self.E = {}
        if multi:
            f = random.choices
        else:            
            f = random.sample
        for e in f( [ (u, v) for u in range(n) for v in range(n) if loops or u != v ], m):
            self.E[e] = self.E.get(e, 0) + 1


    def shuffle(self, keep_edge_directions = False):
        nodes_perm = list(range(self.n))
        random.shuffle(nodes_perm)
        #print(f"{nodes_perm=}, {self.E=}", file = stderr)
        new_E = {}
        for (u, v) in self.E:
            #print(f"{u=}, {v=}", file = stderr)
            uu, vv = nodes_perm[u], nodes_perm[v]
            if not keep_edge_directions and random.randint(0, 1) == 0:
                uu, vv = vv, uu
            new_E[(uu, vv)] = new_E.get((uu, vv), 0) + self.E[(u, v)]
        self.E = new_E
        return nodes_perm

    def adjacent(self, u, v):
        return (u, v) in self.E or (v, u) in self.E
    
    def is_a_directed_arc(self, u, v):
        return (u, v) in self.E


    def as_str(self, node_names_starting_from = 0):
        ret = f"{str(self.n)} {str(self.m)}"
        for (u, v) in self.E:
            for _ in range(self.E[(u, v)]):
                ret += f"\n{u +node_names_starting_from} {v +node_names_starting_from}"
        return ret

    def display(self, node_names_starting_from = 0, out = stderr):
        print(self.as_str(node_names_starting_from), file = out, flush = True)


    def set_up_star_representation(self, undirected = True):
        self.neigh = [ [] for _ in range(self.n) ]
        i = 0
        for (u, v) in self.E:
          for _ in range(self.E[(u, v)]):
            #print(f"{i=}, {u=}, {v=}")
            self.neigh[u].append( (v, i) )
            if undirected:
                self.neigh[v].append( (u, i) )
            i += 1
        assert i == self.m

if __name__ == "__main__":
  print(WARNING)   
  n, m = map(int, input("N, M = ").strip().split())
  G = Graph()
  G.rand_directed(n, m)
  G.display(node_names_starting_from = 1, out = stderr)
  G.shuffle()
  G.display(node_names_starting_from = 1, out = stderr)
  