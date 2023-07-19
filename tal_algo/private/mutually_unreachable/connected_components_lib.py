#!/usr/bin/env python3
# LIBRARY: connected_components_lib.py   last change: 27-05-2023   author: Romeo Rizzi

from sys import stdin, stdout, stderr
import random

class CC_Graph:

    def load_from_stdin(self):
        self.n, self.m = map(int, input().strip().split())
        self.E = set({})
        for _ in range(self.m):
            u, v = map(int, input().strip().split())
            self.E.add( (u, v) )
            self.E.add( (v, u) )

    def set_up(self, n, E):
        self.n = n
        self.m = len(E)
        self.E = set({})
        for (u, v) in E:
            self.E.add( (u, v) )
            self.E.add( (v, u) )

    def rand_gen(self, n, m, c=None, shuffled=True):
        """generates a random graph with n nodes, m edges and c components. When c is also given, such a graph might not exist, in which case a complaint is risen within one of two asserts terminating the program. Before shuffling of the nodes takes place, the components are intervals over [0, 1, ..., n-1]."""
        #print(f"called rand_gen(self, {n=}, {m=}, {c=}, {shuffled=})", file=stderr)
        max_edges = [0] * (n+1) # max number of edges for simple graph on n nodes  
        min_nodes = [0] * (m+1) # min number of nodes for simple graph with m edges  
        j = 1
        for i in range(1, n + 1):
            max_edges[i] = max_edges[i-1] + i - 1
            while max_edges[i] >= j and j <= m:
                min_nodes[j] = i
                j += 1
        #print(f"{max_edges=}", file=stderr)
        #print(f"{min_nodes=}", file=stderr)
        if c is None:
            c = max(1, n - m)
            next_c = c + 1
            while max_edges[n - (next_c - 1)] >= m:
                c = next_c
                next_c = random.randint(c + 1, min(2*c, n) )
        assert c >= n - m, f"Every undirected simple graph with {n=}, {m=} has more than {c} connected components."
        sizes = [1] * (c-1) + [n - c + 1] # first proposal (always feasible if the input (n,m,c) was feasible) for the sizes (i.e., number of nodes) of the c connected components
        max_m = sum( max_edges[size] for size in sizes )
        margin = max_m - m
        assert margin >= 0, f"Every undirected simple graph with {n=}, {m=} has less than {c} connected components."
        self.n = n; #print(f"{n=}", file=stderr)
        self.m = m; #print(f"{m=}", file=stderr)
        self.c = c; #print(f"{c=}", file=stderr)

        # begin: random walk on the sizes of the connected components
        for _ in range(min(2*m, c*n)):
            i, j = random.sample(range(c), 2)
            if sizes[i] > sizes[j]:
                i, j = j, i
            if sizes[j] - sizes[i] <= 1:
                continue
            if margin + max_edges[sizes[i] + 1] + max_edges[sizes[j] - 1] < max_edges[sizes[i]] + max_edges[sizes[j]]:
                continue
            if margin >= max_edges[sizes[j]] - max_edges[sizes[i]]:
                max_delta = (sizes[j] - sizes[i]) // 2
            else:
                min_sizes_j = min_nodes[max_edges[sizes[j]] - max_edges[sizes[i]] - margin]
                max_delta = sizes[j] - min_sizes_j
            if max_delta < 1:
                #print(f"{max_delta=}, {i=}, {j=}, {sizes=}", file=stderr)
                continue                
            delta = random.randint(1, max_delta)
            max_m -= max_edges[sizes[i]] + max_edges[sizes[j]]
            sizes[i] += delta
            sizes[j] -= delta
            max_m += max_edges[sizes[i]] + max_edges[sizes[j]]
            margin = max_m - m
            #print(f"{max_m=}, {margin=}, {sizes=}", file=stderr)
        # end: random walk on the sizes
        #print(f"{sizes=}", file=stderr)
        
        # begin: bounding the number of edges in each connected component
        max_edge_sizes = [ max_edges[sizes[k]] for k in range(c) ]
        min_edge_sizes = [ sizes[k] - 1 for k in range(c) ]
        #print(f"{min_edge_sizes=}", file=stderr)
        #print(f"{max_edge_sizes=}", file=stderr)
        max_edge_sizes_prefix = [0] * c
        min_edge_sizes_prefix = [0] * c
        max_edge_sizes_prefix[0] = max_edge_sizes[0]
        min_edge_sizes_prefix[0] = min_edge_sizes[0]
        for k in range(c-1):
            max_edge_sizes_prefix[k+1] = max_edge_sizes[k+1] + max_edge_sizes_prefix[k] 
            min_edge_sizes_prefix[k+1] = min_edge_sizes[k+1] + min_edge_sizes_prefix[k]
        # end: bounding the number of edges in each connected component
        #print(f"{min_edge_sizes_prefix=}", file=stderr)
        #print(f"{max_edge_sizes_prefix=}", file=stderr)
        # begin: fixing the number of edges in each connected component
        edge_sizes = [0] * c
        for k in reversed(range(1, c)):
            edge_sizes[k] = random.randint(max(min_edge_sizes[k], m - max_edge_sizes_prefix[k - 1]), min(max_edge_sizes[k], m - min_edge_sizes_prefix[k - 1]))
            m -= edge_sizes[k]
        edge_sizes[0] = m
        # end: fixing the number of edges in each connected component
        #print(f"{edge_sizes=}", file=stderr)
            
        self.E = set({})
        first_node = 0
        for k in range(c):
            next_first_node = first_node + sizes[k]
            #print(f"{first_node=}, {next_first_node=}, {sizes[k]=}, {edge_sizes[k]=}, {edge_sizes[k] - sizes[k] + 1=}", file=stderr)
            for v in range(first_node, next_first_node - 1):
                self.E.add( (v, v + 1) )                
                self.E.add( (v + 1, v) )
                # this Hamilton path is in order to gurantee connectivity
            # now the further edges of component k:
            for u,v in random.sample( [ (u, v) for u in range(first_node, next_first_node) for v in range(first_node, next_first_node) if u < v - 1 ], edge_sizes[k] - sizes[k] + 1):
                self.E.add( (u, v) )
                self.E.add( (v, u) )
            first_node = next_first_node
            #print(f"{self.E=}", file=stderr)
        if shuffled:
            self.shuffle()
        #print("begin: grafo generato", file=stderr)
        #self.display(out = stderr)
        #print("end: grafo generato", file=stderr)
            
    def shuffle(self):
        nodes_perm = list(range(self.n))
        random.shuffle(nodes_perm)
        #print(f"{nodes_perm=}, {self.E=}", file = stderr)
        new_E = set({})
        for (u, v) in self.E:
            #print(f"{u=}, {v=}", file = stderr)
            uu, vv = nodes_perm[u], nodes_perm[v]
            new_E.add( (uu, vv) )
        self.E = new_E
        return nodes_perm

    def adjacent(self, u, v):
        return (u, v) in self.E
    
    def as_str(self, node_names_starting_from = 0):
        ret = f"{str(self.n)} {str(self.m)}"
        for (u, v) in self.E:
            if u < v:
                ret += f"\n{u +node_names_starting_from} {v +node_names_starting_from}"
        return ret

    def display(self, node_names_starting_from = 0, out = stderr):
        print(self.as_str(node_names_starting_from), file = out, flush = True)


    def set_up_star_representation(self):
        self.neigh = [ [] for _ in range(self.n) ]
        for (u, v) in self.E:
            #print(f"{u=}, {v=}")
            self.neigh[u].append(v)
        

    def connected_components(self):
        seen = [False] * self.n
        CC = []
        def dfs(u, C):
            nonlocal seen
            if not seen[u]:
                C.add(u)
                seen[u] = True
                for v in self.neigh[u]:
                     dfs(v, C)
        for v in range(self.n):
            if not seen[v]:
                CC.append(set())
                dfs(v, CC[-1])
        return CC
        
    def print_connected_components(self):
        CC = self.connected_components()
        #print(f"{CC=}", file=stderr)
        print(len(CC))
        for C in CC:
            for v in C:
                print(v, end=" ")
            print()
                
    def check_connected_components(self, CC_given):
        #print(f"entering check_connected_components on a graph with {self.n=},  {self.m=}", file = stderr)
        CC_true = self.connected_components()
        context = f"\nthe input graph instance was:\n{self.as_str()}"
        seen = [None] * self.n
        for i, C_given in enumerate(CC_given):
            problem_with_component = "We met a problem when scanning your component:\n   " + " ".join([str(v) for v in C_given]) + "\n"
            for v in C_given:
                if seen[v] is not None:
                    if seen[v] == i:
                        return False, problem_with_component + f"Indeed, node {v} is included at least twice within it!" + context
                    else:
                        return False, problem_with_component + f"Indeed, node {v} is included also in another component you have given, namely:\n   " + " ".join([str(v) for v in CC_given[seen[v]] ]) + context
                seen[v] = i
            for C_true in CC_true:
                if v in C_true:
                    break
            for u in C_given:
                if u not in C_true:
                    return False, problem_with_component + f"Indeed, nodes {u} and {v} are both included; however, there exists no path between {u} and {v} in the given graph." + context
            if len(C_given) < len(C_true):
                for u in C_true:
                    if u not in C_given:
                        return False, problem_with_component + f"However, this component is not a maximal connected component since it is strictly contained in the following connected component:\n   " + " ".join([str(v) for v in C_true]) + f"\nwhich, contains also the node {u}." + context
        for v in range(self.n):
            if seen[v] is None:
                return False, f"No one of the components you have given contains the node {v}." + context 
        #print(f"returning True on check solution for a graph with {self.n=},  {self.m=}", file = stderr)
        return True, ""


    def check_mutually_unreachable(self, S_risp, s_risp):
        #print(f"entering check_connected_components on a graph with {self.n=},  {self.m=}", file = stderr)
        context = f"\nYou returned the list of nodes:\n   {S_risp}\nas an optimal set S for the input graph instance:\n{self.as_str()}"
        if len(S_risp) < s_risp:
            return False, "An obvious inconsistency: you answered that the optimal cardinality was {s_risp} but returned a set of only {len(S_risp)} < {s_risp} nodes." + context
        if len(S_risp) > s_risp:
            return False, "An obvious inconsistency: you answered that the optimal cardinality was {s_risp} but returned a set of {len(S_risp)} > {s_risp} nodes." + context
        CC_true = self.connected_components()
        component_of_node = [None] * self.n
        for i, C in enumerate(CC_true):
            for v in C:
                component_of_node[v] = i
        already_got_node = [None] * len(CC_true)
        for v in S_risp:
            if already_got_node[component_of_node[v]] is not None:
                if v == already_got_node[component_of_node[v]]:
                    return False, f"Node {v} appears twice within your list S of not mutually unreachable nodes!" + context
                else:
                    return False, f"The nodes in your set S are not mutually unreachable. Indeed, there is a path in the input graph between nodes {v} and {already_got_node[component_of_node[v]]}!" + context
            else:
                already_got_node[component_of_node[v]] = v
        if s_risp < len(CC_true):
            for k in range(len(CC_true)):
                if already_got_node[k] is None:
                    break
            iterator = iter(CC_true[k])
            v = next(iterator, None)
            return False, f"Your set S is not a maximum cardinality set of mutually unreachable nodes. Indeed, it is not even a maximal one since there is no path between node {v} and any of the nodes in your set S. As such, node {v} could be addes to set S to obtain a larger feasible set!" + context
        return True, ""




if __name__ == "__main__":
  n, m, c = 8, 11, None  
  # n, m, c = map(int, input("N, M, num of connected components = ").strip().split())
  G = CC_Graph()
  G.rand_gen(n, m, c, shuffled=False)
  print("graph before shuffling:")
  G.display(out = stderr)
  G.shuffle()
  print("graph after shuffling:")
  G.display(out = stderr)
  print("Decomposes into the following connected components path:")
  G.set_up_star_representation()
  G.print_connected_components()
  
