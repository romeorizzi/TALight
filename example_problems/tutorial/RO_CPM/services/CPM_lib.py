#!/usr/bin/env python3
import ast
import os
from sys import stderr
from time import sleep
from typing import Optional, List, Dict, Callable

from RO_verify_submission_gen_prob_lib import verify_submission_gen

instance_objects_spec = [
    ('n', int),
    ('labels', 'list_of_str'),
    ('arcs', 'list_of_tuple_of'),
    ('arcs_removed', 'list_of_tuple_of'),
    ('arcs_added', 'list_of_tuple_of'),
    ('focus_node', str),
    ('focus_arc', 'tuple_of'),
]
additional_infos_spec = [
    ('partialDPtable_to', 'yaml'),
    ('partialDPtable_from', 'yaml'),
    ('DPtableFrom', 'yaml'), 
    ('DPtableTo', 'yaml'), 
]
answer_objects_spec = {
    'is_a_DAG': bool,
    'cert_YES': 'list_of_str',
    'cert_NO': 'list_of_str',
    'earliest_time_for_focus_node': int,
    'critical_path_to_focus_node': 'list_of_str',
    'nodes_sensible_to_focus_arc': 'list_of_str',
    'latest_time_for_focus_node': int,
    'critical_path_from_focus_node': 'list_of_str',
    'min_time_to': 'yaml',
    'min_time_from': 'yaml',
    'latest_time_to': 'yaml',
    'critical_path_to': 'yaml',
    'critical_nodes_to': 'yaml',
    'critical_arcs_to': 'yaml',
    'sensible_to_focus_arc': 'yaml',
}
answer_objects_implemented = [
    'is_a_DAG',
    'cert_YES',
    'cert_NO',
    'earliest_time_for_focus_node',
    'critical_path_to_focus_node',
    'nodes_sensible_to_focus_arc',
    'latest_time_for_focus_node',
    'critical_path_from_focus_node',
    'min_time_to',
    'min_time_from',
    'latest_time_to',
    'critical_path_to',
    'critical_nodes_to',
    'critical_arcs_to',
    'sensible_to_focus_arc',
]


# Una classe per rappresentare un oggetto graph
class Graph:
    # Costruttore
    def __init__(self, arcs, n, labels, arcs_removed, arcs_added, focus_node, focus_arc):

        if type(arcs) == str:
            arcs = ast.literal_eval(arcs)

        if type(arcs_removed) == str:
            arcs_removed = ast.literal_eval(arcs_removed)

        if type(arcs_added) == str:
            arcs_added = ast.literal_eval(arcs_added)

        # Assegnamo a V il numero dei vertici
        self.V = n

        # Assegnamo a E la lista degli archi
        self.E = arcs

        # Un elenco di elenchi per rappresentare un elenco di adiacenze
        self.adjList = dict()

        # gestione degli archi rimossi sul grafo D'
        for arc in arcs_removed:            
            arcs.remove(arc)

        # gestione degli archi aggiunti sul grafo D'
        for arc in arcs_added:
            arcs.append(arc)

        # archi aggiornati del grafo D'
        self.E1 = arcs

        # Valori di default iniziali
        self.arcs_rem = arcs_removed
        self.arcs_add = arcs_added
        self.focus_n = focus_node
        self.focus_a = focus_arc

        if len(labels) == 0 or labels == '[]':

            # aggiunge archi al graph diretto
            for (head, tail, delay) in arcs:
                head = str(head)
                tail = str(tail)
                delay = int(delay)
                if(head not in self.adjList.keys()):
                    self.adjList[head]=[[tail, delay]]
                else:
                    self.adjList[head].append([tail, delay])

            
            for (head, tail, delay) in arcs:
                head = str(head)
                tail = str(tail)
                delay = int(delay)
                if(tail not in self.adjList.keys()):
                    self.adjList[tail]=[[tail, 0]]

        else:
            n = len(labels)
            self.V = n
            # aggiunge archi al graph diretto
            for (head, tail, delay) in arcs:
                if(head not in self.adjList.keys()):
                    self.adjList[head]=[[tail, delay]]
                else:
                    self.adjList[head].append([tail, delay])

            
            for (head, tail, delay) in arcs:
                head = str(head)
                tail = str(tail)
                delay = int(delay)
                if(tail not in self.adjList.keys()):
                    self.adjList[tail]=[[tail, 0]]

# Perform DFS on the graph and set the departure time of all vertices of the graph


def DFS(graph, v, discovered, departure, time, trad, trad_rev):

    # mark the current node as discovered
    discovered[v] = True

    # do for every edge (v, u)
    l = []
    for key in graph.adjList[trad[v]]:
        if len(key) > 0:
            l.append(key[0])
    for u in l:
        # if `u` is not yet discovered
        if str(u) in trad_rev.keys() and not discovered[trad_rev[str(u)]]:
            time = DFS(graph, trad_rev[u], discovered,
                       departure, time, trad, trad_rev)

    # ready to backtrack
    # set departure time of vertex `v`
    departure[v] = time
    time = time + 1

    return time
    
def get_nodes_from_arcs(arcs):
    lst = []
    for arc in arcs:
        lst.append((arc[0],arc[1]))
    return lst


def isDAG(graph):

    n = len(graph.adjList)

    trad = {}
    trad_rev = {}

    for i in range(n):
        trad[i] = list(graph.adjList.keys())[i]
        trad_rev[list(graph.adjList.keys())[i]] = i

    # tiene traccia del rilevamento o meno di un vertice
    discovered = [False] * n

    # tiene traccia dell'ora di partenza di un vertice in DFS
    departure = [None] * n

    time = 0

    # Esegui l'attraversamento DFS da tutti i vertici sconosciuti
    # per visitare tutte le componenti connesse di un grafo
    for i in range(n):
        if not discovered[i]:
            time = DFS(graph, i, discovered, departure, time, trad, trad_rev)

    # controlla se il dato graph diretto è DAG o meno
    for u in range(n):

        # controlla se (u, v) forma un back-edge.
        l = []
        for key in graph.adjList[trad[u]]:
            if len(key) > 0:
                l.append(key[0])
        for v in l:

            # Se il tempo di partenza del vertice `v` è maggiore o uguale
            # all'ora di partenza di `u`, formano un ciclo.

            # Si noti che `departure[u]` sarà uguale a `departure[v]`
            # solo se `u = v`, cioè il vertice contiene un arco a se stesso
            if str(v) in trad_rev.keys() and departure[u] <= departure[trad_rev[str(v)]]:
                return False
    # senza cicli
    return True


def topologicalSortUtil(v, visited, stack, graph):

    # Mark the current node as visited.
    visited[v] = True

    # Recur for all the vertices adjacent to this vertex
    for i in getNeighbors(graph.adjList, v):
        if i in visited and visited[i] == False:
            topologicalSortUtil(i, visited, stack, graph)

    # Push current vertex to stack which stores result
    stack.append(v)

    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()


def topologicalSort(graph):
    # Mark all the vertices as not visited
    visited = dict()
    for k in graph.adjList.keys():
        visited[k] = False
    stack = []

    # Call the recursive helper function to store Topological
    # Sort starting from all vertices one by one
    for i in graph.adjList.keys():
        if visited[i] == False:
            topologicalSortUtil(i, visited, stack, graph)

    # Print contents of the stack
    #print(stack[::-1])  # return list in reverse order

    for arc in graph.adjList[stack[0]]:
        if len(arc) > 0:
            if arc[0] != stack[-1]:
                return (True, stack[::-1])
    if graph.adjList[stack[0]] == []:
        return (True, stack[::-1])
    return (False, stack[::-1])


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def get(self):
        retVal = self.queue[0]
        self.queue.remove(retVal)
        return retVal

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            max_val = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max_val]:
                    max_val = i
            item = self.queue[max_val]
            del self.queue[max_val]
            return item
        except IndexError:
            print()
            exit()


def getNeighbors(adjList, node):
    neighbors = []
    for neighbor in adjList[node]:
        if len(neighbor) > 0:
            neighbors.append(neighbor[0])
    return neighbors


def getCostOfNeighbor(adjList, start, end):
    for neigh in adjList[start]:
        if neigh[0] == end:
            return neigh[1]
    return 'inf'

#Algoritmo per trovare i percorsi minimi
def dijkstra_opt(graph, start_vertex): 
    D = {v: [float('inf'), []] for v in graph.adjList.keys()}
    D[start_vertex][0] = 0
    D[start_vertex][1] = start_vertex

    visited = dict()

    pq = PriorityQueue()
    pq.insert((0, start_vertex))

    while not pq.isEmpty():
        (dist, current_vertex) = pq.get()
        visited.update({current_vertex: None})

        for neighbor in graph.adjList.keys():
            neighbors = getNeighbors(graph.adjList, current_vertex)
            if neighbor in neighbors:
                for n in neighbors:
                    if n == neighbor:
                        distance = getCostOfNeighbor(
                            graph.adjList, current_vertex, n)
                        old_cost = D[neighbor][0]
                        new_cost = D[current_vertex][0] + distance
                        if new_cost < old_cost:
                            pq.insert((new_cost, neighbor))
                            D[neighbor][0] = new_cost
                            D[neighbor][1] = D[current_vertex][1]+' '+neighbor
    for key in D.keys():
        if D[key][1] != []:
            D[key] = [D[key][0], D[key][1].split(' ')]
    return D

def getCostOfNeighbor_max(adjList,start,end):
    for neigh in adjList[start]:
        if neigh[0] == end:
            return neigh[1]
    return 0

#Algoritmo per calcolare il percorso più lungo tra nodi (senza cicli)
def dijkstra_max(graph, start_vertex):
    D = {v: [float(0), []] for v in graph.adjList.keys()}
    D[start_vertex][0] = 0
    D[start_vertex][1] = start_vertex

    visited = dict()

    pq = PriorityQueue()
    pq.insert((0, start_vertex))

    while not pq.isEmpty():
        (dist, current_vertex) = pq.get()
        visited.update({current_vertex: None})

        for neighbor in graph.adjList.keys():
            neighbors = getNeighbors(graph.adjList, current_vertex)
            if neighbor in neighbors:
                for n in neighbors:
                    if n == neighbor:
                        distance = getCostOfNeighbor(
                            graph.adjList, current_vertex, n)
                        old_cost = D[neighbor][0]
                        new_cost = D[current_vertex][0] + distance
                        if new_cost > old_cost and neighbor not in D[current_vertex][1]:
                            pq.insert((new_cost, neighbor))
                            D[neighbor][0] = new_cost
                            D[neighbor][1] = D[current_vertex][1]+' '+neighbor
    for key in D.keys():
        if D[key][1] != []:
            D[key] = [D[key][0], D[key][1].split(' ')]
    return D


def get_DP_table(G, algo):
    DP_rows = {}
    for nodoK in sorted(G.adjList):
        dijks = algo(G, nodoK)
        for key in dijks.keys():
            dijks[key] = dijks[key][0]
        DP_rows[nodoK] = dijks
    return DP_rows


def get_DP_table_path(G, algo):
    DP_rows = {}
    for nodoK in sorted(G.adjList):
        dijks = algo(G, nodoK)
        for key in dijks.keys():
            dijks[key] = dijks[key][1]
        DP_rows[nodoK] = dijks
    return DP_rows

def path_from(table, start, end):
    start = str(start)
    end = str(end)
    if start in table.keys() and end in table.keys():
        return table[end][start]
    else:
        return {}


def path_to(table, start, end):
    start = str(start)
    end = str(end)
    if start in table.keys() and end in table.keys():
        return table[start][end]
    else:
        return {}

#Restituisce gli archi da attraversare nel percorso tra start ed end nella table
def critical_arcs_to_node(table, start, end):
    path = path_to(table, start, end)
    arcs = []
    old_node = None
    for node in path:
        if old_node is None:
            old_node = node
            continue
        arcs.append((old_node, node))
        old_node = node
    return arcs

#Restituisce il dizionario dei nodi con associato True o False se tale nodo viene raggiunto tramite il focus_arc
def f_sensible_to_focus_arc(table, start, focus_arc):
    focus_arc = focus_arc[:-1]
    result = dict()
    for key in table.keys():
        arcs = critical_arcs_to_node(table, start, key)
        result[key] = focus_arc in arcs
    return result

#Restituisce la lista dei nodi che sono sensible to focus arc
def f_nodes_sensible_to_focus_arc(table, start, focus_arc):
    result = []
    sensible_to_focus_arc_v = f_sensible_to_focus_arc(table, start, focus_arc)
    for k in sensible_to_focus_arc_v.keys():
        if sensible_to_focus_arc_v[k]:
            result.append(k)
    return (result)
          
#Calcola la somma dei delay nel percorrere il path nel graph  
def delay_sum(graph, path):
    adjList = graph.adjList
    prec = None
    result = 0
    for node in path:
        if prec is not None:
            for arcAdj in adjList[prec]:
                if arcAdj[0] == node:
                    result += arcAdj[1]
        prec = node
    return result
    

def min_time_to(G: Graph, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = delay_sum(G, path_to(DPT, start, k))
    return res
    

def f_min_time_from(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = delay_sum(G, path_from(DPT, start, k))
    return res
    

def f_latest_time_to(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = delay_sum(G, path_to(DPT, start, k))
    return res
    

def f_critical_path_to(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = path_to(DPT, start, k)
    return res


def f_critical_nodes_to(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        nodes = path_to(DPT, start, k)
        if len(nodes) > 0:
            nodes.pop(-1)
        res[k] = nodes
    return res
    

def f_critical_arcs_to(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = critical_arcs_to_node(DPT, start, k)
    return res


def coalesce(a ,b):
    if a is not None:
        return a
    return b


def check_instance_consistency(instance):
    # print(f"instance={instance}", file=stderr)
    labels = instance["labels"]
    n = len(instance["labels"])
    chk_labels = True

    if n == 0:
        chk_labels = False
        n = instance["n"]
        labels = []
        for i in range(0, n+1):
            labels.append(str(i))

    for arc in instance["arcs"]:
        if arc is not None and len(arc) > 1:
            if (arc[0] not in labels or arc[1] not in labels):
                print(
                    'ERRORE: Nell\'arco {} in "arcs" è presente un nodo non definito'.format(arc))
                exit(0)
            if (get_nodes_from_arcs(instance["arcs"]).count((arc[0], arc[1])) > 1):
                print('ERRORE: l\'arco {} è ripetuto in "arcs"'.format(arc))
                exit(0)

    for arc in instance["arcs_removed"]:

        if len(arc) > 3:
            newarc = []
            newarc.append(str(arc[1]))
            newarc.append(str(arc[3]))
            newarc.append(int(arc[5]))
            arc = tuple(newarc)
        print(arc)

        if (arc not in instance["arcs"]):
            print(
                'ERRORE: Nell\'arco {} in "arcs_removed" è presente un nodo non definito'.format(arc))
            exit(0)

    for arc in instance["arcs_added"]:

        if len(arc) > 3:
            newarc = []
            newarc.append(str(arc[1]))
            newarc.append(str(arc[3]))
            newarc.append(int(arc[5]))
            arc = tuple(newarc)

        if (arc not in instance["arcs"]):
            print(
                'ERRORE: Nell\'arco {} in "arcs_added" è presente un arco non definito'.format(arc))
            exit(0)

    if chk_labels:
        if int(instance["focus_node"]) > len(labels)-1:
            print('ERRORE: Il nodo "focus_node" {} non è definito'.format(
                instance["focus_node"]))
            exit(0)

    if len(instance["focus_arc"]) > 3:
        arc = []
        arc.append(str(instance["focus_arc"][1]))
        arc.append(str(instance["focus_arc"][3]))
        arc.append(int(instance["focus_arc"][5]))
        arc = tuple(arc)
    else:
        arc = instance["focus_arc"]

    if (arc not in instance["arcs"] and arc not in instance["arcs_added"]):
        print(
            'ERRORE: L\'arco {} non è presente in "arcs_added" nè in "arcs"'.format(arc))
        exit(0)
    

def solver(input_to_oracle: dict) -> dict:

    instance = input_to_oracle['input_data_assigned']
    n = instance['n']
    labels = instance['labels']
    arcs = instance['arcs']
    arcs_removed = instance['arcs_removed']
    arcs_added = instance['arcs_added']
    if len(labels) > 0:
        focus_node = labels[int(instance['focus_node'])]
    else:
        focus_node = instance['focus_node']
    focus_arc = instance['focus_arc']

    graph = Graph(arcs, n, labels, arcs_removed, arcs_added, focus_node, focus_arc)

    default_node = list(graph.adjList.keys())[0]

    is_a_DAG = isDAG(graph)
    cert_YES = topologicalSort(graph)[1]
    cert_NO = topologicalSort(graph)[1]
    earliest_time_for_focus_node = delay_sum(graph, path_to(get_DP_table_path(graph,dijkstra_opt), default_node, focus_node))
    critical_path_to_focus_node = path_to(get_DP_table_path(graph,dijkstra_opt), default_node, focus_node)
    nodes_sensible_to_focus_arc = f_nodes_sensible_to_focus_arc(get_DP_table_path(graph,dijkstra_opt), default_node, focus_arc)
    latest_time_for_focus_node = delay_sum(graph, path_to(get_DP_table_path(graph,dijkstra_max), default_node, focus_node))
    critical_path_from_focus_node = path_to(get_DP_table_path(graph,dijkstra_max), default_node, focus_node)
    min_time_to = get_DP_table_path(graph,dijkstra_opt)
    min_time_from = f_min_time_from(graph, get_DP_table_path(graph,dijkstra_opt), default_node)
    latest_time_to = f_latest_time_to(graph, get_DP_table_path(graph,dijkstra_max), default_node)
    critical_path_to = f_critical_path_to(graph, get_DP_table_path(graph,dijkstra_opt), default_node)
    critical_nodes_to = f_critical_nodes_to(graph, get_DP_table_path(graph,dijkstra_opt), default_node)
    critical_arcs_to = f_critical_arcs_to(graph, get_DP_table_path(graph,dijkstra_opt), default_node)
    sensible_to_focus_arc = f_sensible_to_focus_arc(get_DP_table_path(graph,dijkstra_opt), default_node, focus_arc)

    #print(f"input_to_oracle={input_to_oracle}", file=stderr)
    input_data = input_to_oracle["input_data_assigned"]
    #print(f"Instance={input_data}", file=stderr)
    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers


class verify_submission_problem_specific(verify_submission_gen):
    """
    Classe per la verifica delle soluzioni sottomesse dal problem solver.
    """

    def __init__(self, sef, input_data_assigned: Dict = {}, long_answer_dict: Dict = {}, oracle_response: Dict = None):
        super().__init__(sef, input_data_assigned, long_answer_dict, oracle_response)
        self.graph = Graph(input_data_assigned['arcs'], input_data_assigned['n'], input_data_assigned['labels'], input_data_assigned['arcs_removed'], input_data_assigned['arcs_added'], input_data_assigned['focus_node'], input_data_assigned['focus_arc'])
        self.input_data_assigned = input_data_assigned

    def verify_format(self, sef):
        """
        Verifica che il formato delle risposte sottomesse dal problem solver sia corretto.
        """
        if not super().verify_format(sef):
            return False

        if 'is_a_DAG' in self.goals:
            is_a_DAG_g = self.goals['is_a_DAG']
            if type(is_a_DAG_g.answ) != bool:
                return sef.format_NO(is_a_DAG_g, f"Come is_a_DAG hai immesso '{is_a_DAG_g.answ}' dove era invece richiesto di immettere un booleano.")
            sef.format_OK(is_a_DAG_g, f"Come is_a_DAG hai immesso un booleano come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'cert_YES' in self.goals:
            cert_YES_g = self.goals['cert_YES']
            if type(cert_YES_g.answ) != list:
                return sef.format_NO(cert_YES_g, f"Come cert_YES hai immesso '{cert_YES_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in cert_YES_g.answ):
                return sef.format_NO(cert_YES_g, f"Come cert_YES hai immesso '{cert_YES_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(cert_YES_g, f"Come cert_YES hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")
        
        if 'cert_NO' in self.goals:
            cert_NO_g = self.goals['cert_NO']
            if type(cert_NO_g.answ) != list:
                return sef.format_NO(cert_NO_g, f"Come cert_NO hai immesso '{cert_NO_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in cert_NO_g.answ):
                return sef.format_NO(cert_NO_g, f"Come cert_NO hai immesso '{cert_NO_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(cert_NO_g, f"Come cert_NO hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'earliest_time_for_focus_node' in self.goals:
            earliest_time_for_focus_node_g = self.goals['earliest_time_for_focus_node']
            if type(earliest_time_for_focus_node_g.answ) != int:
                return sef.format_NO(earliest_time_for_focus_node_g, f"Come earliest_time_for_focus_node hai immesso '{earliest_time_for_focus_node_g.answ}' dove era invece richiesto di immettere un valore intero.")
            sef.format_OK(earliest_time_for_focus_node_g, f"Come earliest_time_for_focus_node hai immesso un valore intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_path_to_focus_node' in self.goals:
            critical_path_to_focus_node_g = self.goals['critical_path_to_focus_node']
            if type(critical_path_to_focus_node_g.answ) != list:
                return sef.format_NO(critical_path_to_focus_node_g, f"Come critical_path_to_focus_node hai immesso '{critical_path_to_focus_node_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in critical_path_to_focus_node_g.answ):
                return sef.format_NO(critical_path_to_focus_node_g, f"Come critical_path_to_focus_node hai immesso '{critical_path_to_focus_node_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(critical_path_to_focus_node_g, f"Come critical_path_to_focus_node hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'nodes_sensible_to_focus_arc' in self.goals:
            nodes_sensible_to_focus_arc_g = self.goals['nodes_sensible_to_focus_arc']
            if type(nodes_sensible_to_focus_arc_g.answ) != list:
                return sef.format_NO(nodes_sensible_to_focus_arc_g, f"Come nodes_sensible_to_focus_arc hai immesso '{nodes_sensible_to_focus_arc_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in nodes_sensible_to_focus_arc_g.answ):
                return sef.format_NO(nodes_sensible_to_focus_arc_g, f"Come nodes_sensible_to_focus_arc hai immesso '{nodes_sensible_to_focus_arc_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(nodes_sensible_to_focus_arc_g, f"Come nodes_sensible_to_focus_arc hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'latest_time_for_focus_node' in self.goals:
            latest_time_for_focus_node_g = self.goals['latest_time_for_focus_node']
            if type(latest_time_for_focus_node_g.answ) != int:
                return sef.format_NO(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso '{latest_time_for_focus_node_g.answ}' dove era invece richiesto di immettere un valore intero.")
            sef.format_OK(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso un valore intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_path_from_focus_node' in self.goals:
            critical_path_from_focus_node_g = self.goals['critical_path_from_focus_node']
            if type(critical_path_from_focus_node_g) != list:
                return sef.format_NO(critical_path_from_focus_node_g, f"Come critical_path_from_focus_node hai immesso '{critical_path_from_focus_node_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in critical_path_from_focus_node_g):
                return sef.format_NO(critical_path_from_focus_node_g, f"Come critical_path_from_focus_node hai immesso '{critical_path_from_focus_node_g.answ}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(critical_path_from_focus_node_g, f"Come critical_path_from_focus_node hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'min_time_to' in self.goals:
            min_time_to_g = self.goals['min_time_to']
            if type(min_time_to_g.answ) != dict:
                return sef.format_NO(min_time_to_g, f"Come min_time_to hai immesso '{min_time_to_g.answ}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in min_time_to_g.answ.keys()):
                return sef.format_NO(min_time_to_g, f"Come chiavi del min_time_to hai immesso '{min_time_to_g.answ.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(delay) != int for delay in min_time_to_g.answ.values()):
                return sef.format_NO(min_time_to_g, f"Come valori del min_time_to hai immesso '{min_time_to_g.answ.values()}' dove era invece richiesto di immettere degli int.")
            sef.format_OK(min_time_to_g, f"Come min_time_to hai immesso un dizionario stringa:intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'min_time_from' in self.goals:
            min_time_from_g = self.goals['min_time_from']
            if type(min_time_from_g.answ) != dict:
                return sef.format_NO(min_time_from_g, f"Come min_time_from hai immesso '{min_time_from_g.answ}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in min_time_from_g.answ.keys()):
                return sef.format_NO(min_time_from_g, f"Come chiavi del min_time_from hai immesso '{min_time_from_g.answ.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(delay) != int for delay in min_time_from_g.answ.values()):
                return sef.format_NO(min_time_from_g, f"Come valori del min_time_from hai immesso '{min_time_from_g.answ.values()}' dove era invece richiesto di immettere degli int.")
            sef.format_OK(min_time_from_g, f"Come min_time_from hai immesso un dizionario stringa:intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'latest_time_to' in self.goals:
            latest_time_to_g = self.goals['latest_time_to']
            if type(latest_time_to_g.answ) != dict:
                return sef.format_NO(latest_time_to_g, f"Come latest_time_to hai immesso '{latest_time_to_g.answ}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in latest_time_to_g.answ.keys()):
                return sef.format_NO(latest_time_to_g, f"Come chiavi del latest_time_to hai immesso '{latest_time_to_g.answ.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(delay) != int for delay in latest_time_to_g.answ.values()):
                return sef.format_NO(latest_time_to_g, f"Come valori del latest_time_to hai immesso '{latest_time_to_g.answ.values()}' dove era invece richiesto di immettere degli int.")
            sef.format_OK(latest_time_to_g, f"Come latest_time_to hai immesso un dizionario stringa:intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_path_to' in self.goals:
            critical_path_to_g = self.goals['critical_path_to']
            if type(critical_path_to_g.answ) != dict:
                return sef.format_NO(critical_path_to_g, f"Come critical_path_to hai immesso '{critical_path_to_g.answ}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in critical_path_to_g.answ.keys()):
                return sef.format_NO(critical_path_to_g, f"Come chiavi hai immesso '{critical_path_to_g.answ.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(path) != list for path in critical_path_to_g.answ.values()):
                return sef.format_NO(critical_path_to_g, f"Come valori hai immesso '{critical_path_to_g.answ.values()}' dove era invece richiesto di immettere una lista.")
            for path in critical_path_to_g.answ.values():
                if any(type(node) != str for node in path):
                    return sef.format_NO(critical_path_to_g, f"Come nodo contenuto nel valore hai immesso valori non di tipo stringa.")
            sef.format_OK(critical_path_to_g, f"Come critical_path_to hai immesso un dizionario come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_nodes_to' in self.goals:
            critical_nodes_to_g = self.goals['critical_nodes_to']
            if type(critical_nodes_to_g.answ) != dict:
                return sef.format_NO(critical_nodes_to_g, f"Come critical_nodes_to hai immesso '{critical_nodes_to_g.answ}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in critical_nodes_to_g.answ.keys()):
                return sef.format_NO(critical_nodes_to_g, f"Come chiavi hai immesso '{critical_nodes_to_g.answ.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(path) != list for path in critical_nodes_to_g.answ.values()):
                return sef.format_NO(critical_nodes_to_g, f"Come valori hai immesso '{critical_nodes_to_g.answ.values()}' dove era invece richiesto di immettere una lista.")
            for path in critical_nodes_to_g.answ.values():
                if any(type(node) != str for node in path):
                    return sef.format_NO(critical_nodes_to_g, f"Come nodo contenuto nel valore hai immesso valori non di tipo stringa.")
            sef.format_OK(critical_nodes_to_g, f"Come critical_nodes_to hai immesso un dizionario come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_arcs_to' in self.goals:
            critical_arcs_to_g = self.goals['critical_arcs_to']
            if type(critical_arcs_to_g.answ) != dict:
                return sef.format_NO(critical_arcs_to_g, f"Come critical_arcs_to hai immesso '{critical_arcs_to_g.answ}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in critical_arcs_to_g.answ.keys()):
                return sef.format_NO(critical_arcs_to_g, f"Come chiavi hai immesso '{critical_arcs_to_g.answ.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(path) != list for path in critical_arcs_to_g.answ.values()):
                return sef.format_NO(critical_arcs_to_g, f"Come valori hai immesso '{critical_arcs_to_g.answ.values()}' dove era invece richiesto di immettere una lista.")
            for path in critical_arcs_to_g.answ.values():
                if any(type(tup) != tuple for tup in path):
                    return sef.format_NO(critical_arcs_to_g, f"Gli archi contenuti nella lista non sono tutti tuple.")
                for tup in path:
                    if len(tup) != 2:
                        return sef.format_NO(critical_arcs_to_g, f"Non tutte le tuple hanno lunghezza 2.")
                    if type(tup[0]) != str or type(tup[1]) != str:
                        return sef.format_NO(critical_arcs_to_g, f"All'interno delle tuple non ci sono solo stringhe.")
            sef.format_OK(critical_arcs_to_g, f"Come critical_arcs_to hai immesso un dizionario come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'sensible_to_focus_arc' in self.goals:
            sensible_to_focus_arc_g = self.goals['sensible_to_focus_arc']
            if type(sensible_to_focus_arc_g.answ) != dict:
                return sef.format_NO(sensible_to_focus_arc_g, f"Come sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g.answ}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in sensible_to_focus_arc_g.answ.keys()):
                return sef.format_NO(sensible_to_focus_arc_g, f"Come chiavi del sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g.answ.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(delay) != bool for delay in sensible_to_focus_arc_g.answ.values()):
                return sef.format_NO(sensible_to_focus_arc_g, f"Come valori del sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g.answ.values()}' dove era invece richiesto di immettere dei bool.")
            sef.format_OK(sensible_to_focus_arc_g, f"Come sensible_to_focus_arc hai immesso un dizionario stringa:bool come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")
    
        return True

    def verify_feasibility(self, sef):
        """
        Verifica che le risposte che il problem solver ha inserito siano sensate rispetto all'istanza del problema.
        """
        if not super().verify_feasibility(sef):
            return False

        labels = self.input_data_assigned['labels']

        if 'cert_YES' in self.goals:
            cert_YES_g = self.goals['cert_YES']
            if any(node not in labels for node in cert_YES_g.answ):
                return sef.feasibility_NO(cert_YES_g, f"Nel cert_YES hai immesso '{cert_YES_g.answ}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(cert_YES_g, f"Nel cert_YES hai immesso correttamente nodi esistenti.")

        if 'cert_NO' in self.goals:
            cert_NO_g = self.goals['cert_NO']
            if any(node not in labels for node in cert_NO_g.answ):
                return sef.feasibility_NO(cert_NO_g, f"Nel cert_NO hai immesso '{cert_NO_g.answ}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(cert_NO_g, f"Nel cert_NO hai immesso correttamente nodi esistenti.")

        if 'earliest_time_to_focus_node' in self.goals:
            earliest_time_to_focus_node_g = self.goals['earliest_time_to_focus_node']
            if earliest_time_to_focus_node_g.answ < 0:
                return sef.feasibility_NO(earliest_time_to_focus_node_g, f"Come earliest_time_to_focus_node hai immesso '{earliest_time_to_focus_node_g.answ}' dove era invece richiesto di immettere un valore intero positivo.")
            sef.feasibility_OK(earliest_time_to_focus_node_g, f"Come earliest_time_to_focus_node hai immesso correttamente un valore intero positivo.")

        if 'latest_time_for_focus_node' in self.goals:
            latest_time_for_focus_node_g = self.goals['latest_time_for_focus_node']
            if latest_time_for_focus_node_g.answ < 0:
                return sef.feasibility_NO(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso '{latest_time_for_focus_node_g.answ}' dove era invece richiesto di immettere un valore intero positivo.")
            sef.feasibility_OK(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso correttamente un valore intero positivo.", "")

        if 'critical_path_to_focus_node' in self.goals:
            critical_path_to_focus_node_g = self.goals['critical_path_to_focus_node']
            if any(node not in labels for node in critical_path_to_focus_node_g.answ):
                return sef.feasibility_NO(critical_path_to_focus_node_g, f"Nel critical_path_to_focus_node hai immesso '{critical_path_to_focus_node_g.answ}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(critical_path_to_focus_node_g, f"Nel critical_path_to_focus_node hai immesso correttamente nodi esistenti.")

        if 'nodes_sensible_to_focus_arc' in self.goals:
            nodes_sensible_to_focus_arc_g = self.goals['nodes_sensible_to_focus_arc']
            if any(node not in labels for node in nodes_sensible_to_focus_arc_g.answ):
                return sef.feasibility_NO(nodes_sensible_to_focus_arc_g, f"Nel nodes_sensible_to_focus_arc hai immesso '{nodes_sensible_to_focus_arc_g.answ}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(nodes_sensible_to_focus_arc_g, f"Nel nodes_sensible_to_focus_arc hai immesso correttamente nodi esistenti.")

        if 'critical_path_from_focus_node' in self.goals:
            critical_path_from_focus_node_g = self.goals['critical_path_from_focus_node']
            if any(node not in labels for node in critical_path_from_focus_node_g.answ):
                return sef.feasibility_NO(critical_path_from_focus_node_g, f"Nel critical_path_from_focus_node hai immesso '{critical_path_from_focus_node_g.answ}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(critical_path_from_focus_node_g, f"Nel critical_path_from_focus_node hai immesso correttamente nodi esistenti.")

        if 'min_time_to' in self.goals:
            min_time_to_g = self.goals['min_time_to']
            if any(node not in labels for node in min_time_to_g.answ.keys()):
                return sef.feasibility_NO(min_time_to_g, f"Nel min_time_to hai immesso '{min_time_to_g.answ}' dove sono presenti nodi non esistenti.")
            if any(delay < 0 for delay in min_time_to_g.answ.values()):
                return sef.feasibility_NO(min_time_to_g, f"Nel min_time_to hai immesso '{min_time_to_g.answ}' dove sono presenti delay negativi.")
            sef.feasibility_OK(min_time_to_g, f"Nel min_time_to hai immesso correttamente nodi esistenti con delay positivi","")
            
        if 'min_time_from' in self.goals:
            min_time_from_g = self.goals['min_time_from']
            if any(node not in labels for node in min_time_from_g.answ.keys()):
                return sef.feasibility_NO(min_time_from_g, f"Nel min_time_from hai immesso '{min_time_from_g.answ}' dove sono presenti nodi non esistenti.")
            if any(delay < 0 for delay in min_time_from_g.answ.values()):
                return sef.feasibility_NO(min_time_from_g, f"Nel min_time_from hai immesso '{min_time_from_g.answ}' dove sono presenti delay negativi.")
            sef.feasibility_OK(min_time_from_g, f"Nel min_time_from hai immesso correttamente nodi esistenti con delay positivi","")

        if 'latest_time_to' in self.goals:
            latest_time_to_g = self.goals['latest_time_to']
            if any(node not in labels for node in latest_time_to_g.answ.keys()):
                return sef.feasibility_NO(latest_time_to_g, f"Nel latest_time_to hai immesso '{latest_time_to_g.answ}' dove sono presenti nodi non esistenti.")
            if any(delay < 0 for delay in latest_time_to_g.answ.values()):
                return sef.feasibility_NO(latest_time_to_g, f"Nel latest_time_to hai immesso '{latest_time_to_g.answ}' dove sono presenti delay negativi.")
            sef.feasibility_OK(latest_time_to_g, f"Nel latest_time_to hai immesso correttamente nodi esistenti con delay positivi","")

        if 'critical_path_to' in self.goals:
            critical_path_to_g = self.goals['critical_path_to']
            if any(node not in labels for node in critical_path_to_g.answ.keys()):
                return sef.feasibility_NO(critical_path_to_g, f"Nel critical_path_to hai immesso '{critical_path_to_g.answ}' dove sono presenti nodi non esistenti.")
            for path in critical_path_to_g.answ.values():
               if any(node not in labels for node in path):
                    return sef.feasibility_NO(critical_path_to_g, f"Nel critical_path_to hai immesso '{critical_path_to_g.answ}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(critical_path_to_g, f"Come critical_path_to hai immesso correttamente nodi esistenti.","")

        if 'critical_nodes_to' in self.goals:
            critical_nodes_to_g = self.goals['critical_nodes_to']
            if any(node not in labels for node in critical_nodes_to_g.answ.keys()):
                return sef.feasibility_NO(critical_nodes_to_g, f"Nel critical_nodes_to hai immesso '{critical_nodes_to_g.answ}' dove sono presenti nodi non esistenti.")
            for path in critical_nodes_to_g.answ.values():
               if any(node not in labels for node in path):
                    return sef.feasibility_NO(critical_nodes_to_g, f"Nel critical_nodes_to hai immesso '{critical_nodes_to_g.answ}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(critical_nodes_to_g, f"Come critical_nodes_to hai immesso correttamente nodi esistenti.","")

        if 'critical_arcs_to' in self.goals:
            critical_arcs_to_g = self.goals['critical_arcs_to']
            if any(node not in labels for node in critical_arcs_to_g.answ.keys()):
                return sef.feasibility_NO(critical_arcs_to_g, f"Come chiavi hai immesso '{critical_arcs_to_g.answ.keys()}' dove sono presenti nodi non esistenti.")
            for path in critical_arcs_to_g.answ.values():
                for tup in path:
                    if tup[0] not in labels or tup[1] not in labels:
                        return sef.feasibility_NO(critical_arcs_to_g, f"All'interno delle tuple ci sono nodi non esistenti.")
            sef.feasibility_OK(critical_arcs_to_g, f"Nel critical_arcs_to hai immesso correttamente nodi esistenti.","")

        if 'sensible_to_focus_arc' in self.goals:
            sensible_to_focus_arc_g = self.goals['sensible_to_focus_arc']
            if any(node not in labels for node in sensible_to_focus_arc_g.answ.keys()):
                return sef.feasibility_NO(sensible_to_focus_arc_g, f"Nel sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g.answ.keys()}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(sensible_to_focus_arc_g, f"Nel sensible_to_focus_arc hai immesso correttamente solo nodi esistenti.","")

        return True

    def verify_consistency(self, sef):
        """
        Verifica che le risposte inserite dall'utente siano consistenti tra di loro.
        """
        if not super().verify_consistency(sef):
            return False
        
        focus_node = self.input_data_assigned['focus_node']

        if 'cert_YES' in self.goals and 'cert_NO' in self.goals:
            cert_YES_g = self.goals['cert_YES']
            cert_NO_g = self.goals['cert_NO']
            if len(coalesce(cert_YES_g.answ, [])) > 0 and len(coalesce(cert_NO_g.answ, [])) > 0:
                return sef.consistency_NO("Hai inserito sia cert_YES che cert_NO, non è consistente.")
            sef.consistency_OK("Le risposte inserite per cert_YES e cert_NO sono consistenti.")

        if 'earliest_time_for_focus_node' in self.goals and 'critical_path_to_focus_node' in self.goals:
            earliest_time_for_focus_node_g = self.goals['earliest_time_for_focus_node']
            critical_path_to_focus_node_g = self.goals['critical_path_to_focus_node']
            if earliest_time_for_focus_node_g.answ != delay_sum(critical_path_to_focus_node_g.answ):
                return sef.consistency_NO("La somma dei pesi degli archi del critical_path_to_focus_node non corrisponde al earliest_time_for_focus_node che hai inserito.")
            sef.consistency_OK("earliest_time_for_focus_node e somma dei pesi degli archi del critical_path_to_focus_node corrispondono.")

        if 'latest_time_for_focus_node' in self.goals and 'critical_path_from_focus_node' in self.goals:
            latest_time_for_focus_node_g = self.goals['latest_time_for_focus_node']
            critical_path_from_focus_node_g = self.goals['critical_path_from_focus_node']
            if latest_time_for_focus_node_g.answ != delay_sum(critical_path_from_focus_node_g.answ):
                return sef.consistency_NO("La somma dei pesi degli archi del critical_path_from_focus_node non corrisponde al latest_time_for_focus_node che hai inserito.")
            sef.consistency_OK("latest_time_for_focus_node e somma dei pesi degli archi del critical_path_from_focus_node corrispondono.")

        if 'min_time_to' in self.goals and 'critical_path_to_focus_node' in self.goals:
            min_time_to_g = self.goals['min_time_to']
            critical_path_to_focus_node_g = self.goals['critical_path_to_focus_node']
            if min_time_to_g.answ[focus_node] != delay_sum(critical_path_to_focus_node_g.answ):
                return sef.consistency_NO("La somma dei pesi degli archi del critical_path_to_focus_node non corrisponde al valore nella DP table min_time_to.")
            sef.consistency_OK("La somma dei pesi degli archi del critical_path_to_focus_node corrisponde al valore nella DP table min_time_to.")

        if 'latest_time_to' in self.goals and 'critical_path_from_focus_node' in self.goals:
            latest_time_to_g = self.goals['latest_time_to']
            critical_path_from_focus_node_g = self.goals['critical_path_from_focus_node']
            if latest_time_to_g.answ[focus_node] != delay_sum(critical_path_from_focus_node_g.answ):
                return sef.consistency_NO("La somma dei pesi degli archi del critical_path_from_focus_node non corrisponde al valore nella DP table latest_time_to.")
            sef.consistency_OK("La somma dei pesi degli archi del critical_path_from_focus_node corrisponde al valore nella DP table latest_time_to.")

        if 'critical_path_to' in self.goals and 'critical_path_to_focus_node' in self.goals:
            critical_path_to_g.answ = self.goals['critical_path_to']
            critical_path_from_focus_node_g.answ = self.goals['critical_path_to_focus_node']
            if critical_path_to_g.answ[focus_node] != critical_path_to_focus_node_g.answ:
                return sef.consistency_NO("Il critical_path_to_focus_node non corrisponde al relativo valore nella DP table critical_path_to.")
            sef.consistency_OK("Il critical_path_to_focus_node corrisponde al relativo valore nella DP table critical_path_to.")

        if 'critical_nodes_to' in self.goals and 'critical_path_to_focus_node' in self.goals:
            critical_nodes_to_g = self.goals['critical_nodes_to']
            critical_path_from_focus_node_g = self.goals['critical_path_to_focus_node']
            critical_path_from_focus_node_g.answ.pop(-1)
            if critical_nodes_to_g.answ[focus_node] != critical_path_to_focus_node_g.answ:
                return sef.consistency_NO("Il critical_path_to_focus_node non corrisponde alla DP table critical_nodes_to.")
            sef.consistency_OK("Il critical_path_to_focus_node corrisponde alla DP table critical_nodes_to.")

        return True

    def verify_optimality(self, sef):
        """
        Verifica che le risposte inserite dell'utente siano quelle corrette
        """
        if not super().verify_optimality(sef):
            return False

        # verifica che opt_val sia effettivamente ottimo
        if 'is_a_DAG' in self.goals:
            is_a_DAG_g = self.goals['is_a_DAG']
            if is_a_DAG_g.answ != isDAG(self.graph):
                return sef.optimality_NO(is_a_DAG_g, f"Come is_a_DAG ha inserito '{is_a_DAG_g}', la risposta però è errata.")
            sef.optimality_OK(is_a_DAG_g, f"'{is_a_DAG_g.answ}' è la risposta corretta.",'')

        if 'cert_YES' in self.goals:
            cert_YES_g = self.goals['cert_YES']
            if cert_YES_g.answ != topologicalSort(self.graph)[1] or True != topologicalSort(self.graph)[0]:
                return sef.optimality_NO(cert_YES_g, f"Come cert_YES ha inserito '{cert_YES_g}', non è però la risposta corretta.")
            sef.optimality_OK(cert_YES_g, f"'{cert_YES_g.answ}' è la risposta corretta.",'')


        if 'cert_NO' in self.goals:
            cert_NO_g = self.goals['cert_NO']
            if cert_NO_g.answ != topologicalSort(self.graph)[1] or True == topologicalSort(self.graph)[0]:
                return sef.optimality_NO(cert_NO_g, f"Come cert_NO ha inserito '{cert_NO_g}', non è però la risposta corretta.")
            sef.optimality_OK(cert_NO_g, f"'{cert_NO_g.answ}' è la risposta corretta.",'')

        if 'earliest_time_to_focus_node' in self.goals:
            earliest_time_to_focus_node_g = self.goals['earliest_time_to_focus_node']
            if earliest_time_to_focus_node_g.answ != delay_sum(self.graph, path_to(get_DP_table_path(graph,dijkstra_opt), '0', self.graph.focus_n)):
                return sef.optimality_NO(earliest_time_to_focus_node_g, f"Come earliest_time_to_focus_node hai immesso '{earliest_time_to_focus_node_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(earliest_time_to_focus_node_g, f"Come earliest_time_to_focus_node hai immesso la soluzione ottima.",'')

        if 'latest_time_for_focus_node' in self.goals:
            latest_time_for_focus_node_g = self.goals['latest_time_for_focus_node']
            if latest_time_for_focus_node_g.answ != delay_sum(self.graph, path_to(get_DP_table_path(self.graph,dijkstra_max), '0', self.graph.focus_n)):
                return sef.optimality_NO(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso '{latest_time_for_focus_node_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso la soluzione ottima.",'')

        if 'critical_path_to_focus_node' in self.goals:
            critical_path_to_focus_node_g = self.goals['critical_path_to_focus_node']
            if critical_path_to_focus_node(get_DP_table_path(self.graph, dijkstra_opt), '0', self.graph.focus_n) != critical_path_to_focus_node_g.answ:
                return sef.optimality_NO(critical_path_to_focus_node_g, f"Nel critical_path_to_focus_node hai immesso '{critical_path_to_focus_node_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(critical_path_to_focus_node_g, f"Nel critical_path_to_focus_node hai immesso la soluzione ottima.",'')

        if 'nodes_sensible_to_focus_arc' in self.goals:
            nodes_sensible_to_focus_arc_g = self.goals['nodes_sensible_to_focus_arc']
            if sensible_to_focus_arc(get_DP_table_path(self.graph, dijkstra_opt), '0', self.graph.focus_a) != nodes_sensible_to_focus_arc_g.answ:
                return sef.optimality_NO(nodes_sensible_to_focus_arc_g, f"Nel nodes_sensible_to_focus_arc hai immesso '{nodes_sensible_to_focus_arc_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(nodes_sensible_to_focus_arc_g, f"Nel nodes_sensible_to_focus_arc hai immesso la soluzione ottima.",'')

        if 'critical_path_from_focus_node' in self.goals:
            critical_path_from_focus_node_g = self.goals['critical_path_from_focus_node']
            if path_to(get_DP_table_path(self.graph,dijkstra_max), '0', self.graph.self.graph.focus_n) != critical_path_from_focus_node_g.answ:
                return sef.optimality_NO(critical_path_from_focus_node_g, f"Nel critical_path_from_focus_node hai immesso '{critical_path_from_focus_node_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(critical_path_from_focus_node_g, f"Nel critical_path_from_focus_node hai immesso la soluzione ottima.",'')

        if 'min_time_to' in self.goals:
            min_time_to_g = self.goals['min_time_to']
            if min_time_to(self.graph, get_DP_table_path(self.graph,dijkstra_opt), '0') != min_time_to_g.answ:
                return sef.optimality_NO(min_time_to_g, f"Nel min_time_to hai immesso '{min_time_to_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(min_time_to_g, f"Nel min_time_to hai immesso la soluzione ottima",'')
            
        if 'min_time_from' in self.goals:
            min_time_from_g = self.goals['min_time_from']
            if min_time_from(self.graph, get_DP_table_path(self.graph, dijkstra_opt), '0') != min_time_from_g.answ:
                return sef.optimality_NO(min_time_from_g, f"Nel min_time_from hai immesso '{min_time_from_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(min_time_from_g, f"Nel min_time_from hai immesso la soluzione ottima",'')

        if 'latest_time_to' in self.goals:
            latest_time_to_g = self.goals['latest_time_to']
            if f_latest_time_to(self.graph, get_DP_table_path(self.graph, dijkstra_max), '0') != latest_time_to_g.answ:
                return sef.optimality_NO(latest_time_to_g, f"Nel latest_time_to hai immesso '{latest_time_to_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(latest_time_to_g, f"Nel latest_time_to hai immesso la soluzione ottima",'')

        if 'critical_path_to' in self.goals:
            critical_path_to_g = self.goals['critical_path_to']
            if critical_path_to(self.graph, get_DP_table_path(self.graph, dijkstra_opt), '0') != critical_path_to_g.answ:
                return sef.optimality_NO(critical_path_to_g, f"Nel critical_path_to hai immesso '{critical_path_to_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(critical_path_to_g, f"Come critical_path_to hai immesso la soluzione ottima.",'')

        if 'critical_nodes_to' in self.goals:
            critical_nodes_to_g = self.goals['critical_nodes_to']
            if critical_nodes_to(self.graph, get_DP_table_path(self.graph,dijkstra_opt), '0') != critical_nodes_to_g.answ:
                return sef.optimality_NO(critical_nodes_to_g, f"Nel critical_nodes_to hai immesso '{critical_nodes_to_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(critical_nodes_to_g, f"Come critical_nodes_to hai immesso la soluzione ottima.",'')

        if 'critical_arcs_to' in self.goals:
            critical_arcs_to_g = self.goals['critical_arcs_to']
            if critical_arcs_to(self.graph, get_DP_table_path(self.graph,dijkstra_opt), '0') != critical_arcs_to_g.answ:
                return sef.optimality_NO(critical_arcs_to_g, f"Come chiavi hai immesso '{critical_arcs_to_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(critical_arcs_to_g, f"Nel critical_arcs_to hai immesso la soluzione ottima.",'')

        if 'sensible_to_focus_arc' in self.goals:
            sensible_to_focus_arc_g = self.goals['sensible_to_focus_arc']
            if sensible_to_focus_arc(get_DP_table_path(self.graph,dijkstra_opt), '0', self.focus_arc) != sensible_to_focus_arc_g.answ:
                return sef.optimality_NO(sensible_to_focus_arc_g, f"Nel sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g.answ}' ma non è il risultato ottimo.")
            sef.optimality_OK(sensible_to_focus_arc_g, f"Nel sensible_to_focus_arc hai immesso la soluzione ottima.",'')

        return True
