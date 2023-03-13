#!/usr/bin/env python3
import ast
import os
from sys import stderr
from time import sleep
from typing import Optional, List, Dict, Callable

from services.RO_verify_submission_gen_prob_lib import verify_submission_gen

instance_objects_spec = [
    ('n', str),
    ('labels', list),
    ('arcs',list),
    ('arcs_removed',list),
    ('arcs_added',list),
    ('focus_node', str),
    ('focus_arc',tuple),
]
additional_infos_spec = [
    ('partial_to',list),
    ('partial_from',list),
]
answer_objects_spec = {
    'is_a_DAG': bool,
    'cert_YES': list,
    'cert_NO': list,
    'earliest_time_for_focus_node': int,
    'critical_path_to_focus_node': list,
    'nodes_sensible_to_focus_arc': list,
    'latest_time_for_focus_node': int,
    'critical_path_from_focus_node': list,
    'min_time_to': dict,
    'min_time_from': dict,
    'latest_time_to': dict,
    'critical_path_to': dict,
    'critical_nodes_to': dict,
    'critical_arcs_to': dict,
    'sensible_to_focus_arc': dict,
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
    def __init__(self, arcs, n=0, labels=[], arcs_removed=[], arcs_added=[], focus_node=None, focus_arc=None, partial_to={}, partial_from={}):

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

        if len(labels) == 0:

            # aggiunge archi al graph diretto
            for (head, tail, delay) in arcs:
                if (type(head) == type(str)):
                    self.adjList[head].append([tail, delay])
                else:
                    self.adjList[str(head)].append([str(tail), delay])

        else:
            n = len(labels)
            self.V = n
            guard = 0
            # aggiunge archi al graph diretto
            for (head, tail, delay) in arcs:
                if guard == 0:
                    self.adjList['0'].append([head, 0])
                    guard = 1

                self.adjList[head].append([tail, delay])

# Perform DFS on the graph and set the departure time of all vertices of the graph


def DFS(graph, v, discovered, departure, time, trad, trad_rev):

    # mark the current node as discovered
    discovered[v] = True

    # do for every edge (v, u)
    l = []
    for key in graph.adjList[trad[v]]:
        l.append(key[0])
    for u in l:
        # if `u` is not yet discovered
        if not discovered[trad_rev[u]]:
            time = DFS(graph, trad_rev[u], discovered,
                       departure, time, trad, trad_rev)

    # ready to backtrack
    # set departure time of vertex `v`
    departure[v] = time
    time = time + 1

    return time


def isDAG(graph):

    n = len(graph.adjList)

    trad = {}
    trad_rev = {}

    for i in range(n):
        trad[i] = list(graph.adjList.keys())[i][0]
        trad_rev[list(graph.adjList.keys())[i][0]] = i

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
            l.append(key[0])
        for v in l:

            # Se il tempo di partenza del vertice `v` è maggiore o uguale
            # all'ora di partenza di `u`, formano un ciclo.

            # Si noti che `departure[u]` sarà uguale a `departure[v]`
            # solo se `u = v`, cioè il vertice contiene un arco a se stesso
            if departure[u] <= departure[trad_rev[v]]:
                return False
    # senza cicli
    return True


def topologicalSortUtil(v, visited, stack, graph):

    # Mark the current node as visited.
    visited[v] = True

    # Recur for all the vertices adjacent to this vertex
    for i in getNeighbors(G.adjList, v):
        if visited[i] == False:
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
        neighbors.append(neighbor[0])
    return neighbors


def getCostOfNeighbor(adjList, start, end):
    for neigh in adjList[start]:
        if neigh[0] == end:
            return neigh[1]
    return 'inf'


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

def min_path_from(table, start, end):
    return table[end][start]


def latest_path_to(table, start, end):
    return table[start][end]


def critical_path_to_focus_node(table, start, end):
    return table[start][end]


def critical_arcs_to_node(table, start, end):
    path = critical_path_to_focus_node(table, start, end)
    arcs = []
    old_node = None
    for node in path:
        if old_node is None:
            old_node = node
            continue
        arcs.append((old_node, node))
        old_node = node
    return arcs


def sensible_to_focus_arc(table, start, focus_arc):
    result = dict()
    for key in table.keys():
        arcs = critical_arcs_to_node(table, start, key)
        print(arcs)
        result[key] = focus_arc in arcs
    return result


def nodes_sensible_to_focus_arc(table, start, focus_arc):
    result = []
    sensible_to_focus_arc_v = sensible_to_focus_arc(table, start, focus_arc)
    for k in sensible_to_focus_arc_v.keys():
        if sensible_to_focus_arc_v[k]:
            result.append(k)
    return (result)


def check_instance_consistency(instance):
    # print(f"instance={instance}", file=stderr)
    labels = instance["labels"]

    n = len(instance["labels"])
    chk_labels = False
    if n == 0:
        chk_labels = True
        n = instance["n"]
        labels = []
        for i in range(1, n+1):
            labels.append(str(i))

    for arc in instance["arcs"]:
        if (arc[0] not in labels or arc[1] not in labels):
            print(
                'ERRORE: Nell\'arco {} in "arcs" è presente un nodo non definito'.format(arc))
            exit(0)
        if (get_nodes_from_arcs(instance["arcs"]).count((arc[0], arc[1])) > 1):
            print('ERRORE: l\'arco {} è ripetuto in "arcs"'.format(arc))
            exit(0)

    for arc in instance["arcs_removed"]:
        if (arc not in instance["arcs"]):
            print(
                'ERRORE: Nell\'arco {} in "arcs_removed" è presente un nodo non definito'.format(arc))
            exit(0)

    for arc in instance["arcs_added"]:
        if (arc not in instance["arcs"]):
            print(
                'ERRORE: Nell\'arco {} in "arcs_added" è presente un nodo non definito'.format(arc))
            exit(0)

    if chk_labels:
        if str(instance["focus_node"]) not in labels:
            print('ERRORE: Il nodo "focus_node" {} non è definito'.format(
                instance["focus_node"]))
            exit(0)

    for arc in instance["focus_arc"]:
        if (arc not in instance["arcs"] and arc not in instance["arcs_added"]):
            print(
                'ERRORE: L\'arco {} non è presente in "arcs_added" nè in "arcs"'.format(arc))
            exit(0)
            
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
        res[k] = delay_sum(G, critical_path_to_focus_node(DPT, start, k))
    return res
    
def min_time_from(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = delay_sum(G, min_path_from(DPT, start, k))
    return res
    
def latest_time_to(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = delay_sum(G, latest_path_to(DPT, start, k))
    return res
    
def critical_path_to(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = min_time_to(DPT, start, k)
    return res


def critical_nodes_to(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        nodes = min_time_to(DPT, start, k)
        nodes.pop(-1)
        res[k] = nodes
    return res
    
def critical_arcs_to(G, DPT, start):
    res = dict()
    for k in sorted(G.adjList.keys()):
        res[k] = critical_arcs_to_node(DPT, start, k)
    return res
    

def solver(input_to_oracle: dict) -> dict:
    instance = input_to_oracle['input_data_assigned']
    n = instance['n']
    labels = instance['labels']
    arcs = instance['arcs']
    arcs_removed = instance['arcs_removed']
    arcs_added = instance['arcs_added']
    focus_node = instance['focus_node']
    focus_arc = instance['focus_arc']

    graph = Graph(arcs, n, labels, arcs_removed, arcs_added, focus_node, focus_arc)

    is_a_DAG = isDAG(graph)
    cert_YES = topologicalSort(graph)
    cert_NO = topologicalSort(graph)
    earliest_time_for_focus_node = delay_sum(graph, critical_path_to_focus_node(get_DP_table_path(graph,dijkstra_opt), '0', focus_node))
    critical_path_to_focus_node = critical_path_to_focus_node(get_DP_table_path(graph,dijkstra_opt), '0', focus_node)
    nodes_sensible_to_focus_arc = sensible_to_focus_arc(get_DP_table_path(graph,dijkstra_opt), '0', focus_arc)
    latest_time_for_focus_node = delay_sum(graph, latest_time_to(get_DP_table_path(graph,dijkstra_max), '0', focus_node))
    critical_path_from_focus_node = latest_time_to(get_DP_table_path(G,dijkstra_max), '0', focus_node)
    min_time_to = min_time_to(graph, get_DP_table_path(G,dijkstra_opt), '0')
    min_time_from = min_time_from(graph, get_DP_table_path(graph,dijkstra_opt), '0')
    latest_time_to = latest_time_to(graph, get_DP_table_path(graph,dijkstra_max), '0')
    critical_path_to = critical_path_to(graph, get_DP_table_path(graph,dijkstra_opt), '0')
    critical_nodes_to = critical_nodes_to(graph, get_DP_table_path(graph,dijkstra_opt), '0')
    critical_arcs_to = critical_arcs_to(graph, get_DP_table_path(graph,dijkstra_opt), '0')
    sensible_to_focus_arc = sensible_to_focus_arc(get_DP_table_path(graph,dijkstra_opt), '0', focus_arc)

    print(f"input_to_oracle={input_to_oracle}", file=stderr)
    input_data = input_to_oracle["input_data_assigned"]
    print(f"Instance={input_data}", file=stderr)
    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    print(oracle_answers)
    return oracle_answers

class verify_submission_problem_specific(verify_submission_gen):
    """
    Classe per la verifica delle soluzioni sottomesse dal problem solver.
    """

    def __init__(self, sef, input_data_assigned: Dict, long_answer_dict: Dict, oracle_response: Dict = None):
        super().__init__(sef, input_data_assigned, long_answer_dict, oracle_response)
        self.graph = None

    def verify_format(self, sef):
        """
        Verifica che il formato delle risposte sottomesse dal problem solver sia corretto.
        """
        if not super().verify_format(sef):
            return False

        if 'is_a_DAG' in self.goals:
            is_a_DAG_g = self.goals['is_a_DAG']
            if type(is_a_DAG_g) != bool:
                return sef.format_NO(is_a_DAG_g, f"Come is_a_DAG hai immesso '{is_a_DAG_g}' dove era invece richiesto di immettere un booleano.")
            sef.format_OK(is_a_DAG_g, f"Come is_a_DAG hai immesso un booleano come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'cert_YES' in self.goals:
            cert_YES_g = self.goals['cert_YES']
            if type(cert_YES_g) != list:
                return sef.format_NO(cert_YES_g, f"Come cert_YES hai immesso '{cert_YES_g}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in cert_YES_g):
                return sef.format_NO(cert_YES_g, f"Come cert_YES hai immesso '{cert_YES_g}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(cert_YES_g, f"Come cert_YES hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")
        
        if 'cert_NO' in self.goals:
            cert_NO_g = self.goals['cert_NO']
            if type(cert_NO_g) != list:
                return sef.format_NO(cert_NO_g, f"Come cert_NO hai immesso '{cert_NO_g}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in cert_NO_g):
                return sef.format_NO(cert_NO_g, f"Come cert_NO hai immesso '{cert_NO_g}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(cert_NO_g, f"Come cert_NO hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'earliest_time_for_focus_node' in self.goals:
            earliest_time_for_focus_node_g = self.goals['earliest_time_for_focus_node']
            if type(earliest_time_for_focus_node_g) != int:
                return sef.format_NO(earliest_time_for_focus_node_g, f"Come earliest_time_for_focus_node hai immesso '{earliest_time_for_focus_node_g}' dove era invece richiesto di immettere un valore intero.")
            sef.format_OK(earliest_time_for_focus_node_g, f"Come earliest_time_for_focus_node hai immesso un valore intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_path_to_focus_node' in self.goals:
            critical_path_to_focus_node_g = self.goals['critical_path_to_focus_node']
            if type(critical_path_to_focus_node_g) != list:
                return sef.format_NO(critical_path_to_focus_node_g, f"Come critical_path_to_focus_node hai immesso '{critical_path_to_focus_node_g}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in critical_path_to_focus_node_g):
                return sef.format_NO(critical_path_to_focus_node_g, f"Come critical_path_to_focus_node hai immesso '{critical_path_to_focus_node_g}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(critical_path_to_focus_node_g, f"Come critical_path_to_focus_node hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'nodes_sensible_to_focus_arc' in self.goals:
            nodes_sensible_to_focus_arc_g = self.goals['nodes_sensible_to_focus_arc']
            if type(nodes_sensible_to_focus_arc_g) != list:
                return sef.format_NO(nodes_sensible_to_focus_arc_g, f"Come nodes_sensible_to_focus_arc hai immesso '{nodes_sensible_to_focus_arc_g}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in nodes_sensible_to_focus_arc_g):
                return sef.format_NO(nodes_sensible_to_focus_arc_g, f"Come nodes_sensible_to_focus_arc hai immesso '{nodes_sensible_to_focus_arc_g}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(nodes_sensible_to_focus_arc_g, f"Come nodes_sensible_to_focus_arc hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'latest_time_for_focus_node' in self.goals:
            latest_time_for_focus_node_g = self.goals['latest_time_for_focus_node']
            if type(latest_time_for_focus_node_g) != int:
                return sef.format_NO(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso '{latest_time_for_focus_node_g}' dove era invece richiesto di immettere un valore intero.")
            sef.format_OK(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso un valore intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_path_from_focus_node' in self.goals:
            critical_path_from_focus_node_g = self.goals['critical_path_from_focus_node']
            if type(critical_path_from_focus_node_g) != list:
                return sef.format_NO(critical_path_from_focus_node_g, f"Come critical_path_from_focus_node hai immesso '{critical_path_from_focus_node_g}' dove era invece richiesto di immettere una lista di stringhe.")
            if any(type(node) != str for node in critical_path_from_focus_node_g):
                return sef.format_NO(critical_path_from_focus_node_g, f"Come critical_path_from_focus_node hai immesso '{critical_path_from_focus_node_g}' dove era invece richiesto di immettere una lista di stringhe.")
            sef.format_OK(critical_path_from_focus_node_g, f"Come critical_path_from_focus_node hai immesso una lista di stringhe come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'min_time_to' in self.goals:
            min_time_to_g = self.goals['min_time_to']
            if type(min_time_to_g) != dict:
                return sef.format_NO(min_time_to_g, f"Come min_time_to hai immesso '{min_time_to_g}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in min_time_to_g.keys()):
                return sef.format_NO(min_time_to_g, f"Come chiavi del min_time_to hai immesso '{min_time_to_g.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(delay) != int for delay in min_time_to_g.values()):
                return sef.format_NO(min_time_to_g, f"Come valori del min_time_to hai immesso '{min_time_to_g.values()}' dove era invece richiesto di immettere degli int.")
            sef.format_OK(min_time_to_g, f"Come min_time_to hai immesso un dizionario stringa:intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'min_time_from' in self.goals:
            min_time_from_g = self.goals['min_time_from']
            if type(min_time_from_g) != dict:
                return sef.format_NO(min_time_from_g, f"Come min_time_from hai immesso '{min_time_from_g}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in min_time_from_g.keys()):
                return sef.format_NO(min_time_from_g, f"Come chiavi del min_time_from hai immesso '{min_time_from_g.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(delay) != int for delay in min_time_from_g.values()):
                return sef.format_NO(min_time_from_g, f"Come valori del min_time_from hai immesso '{min_time_from_g.values()}' dove era invece richiesto di immettere degli int.")
            sef.format_OK(min_time_from_g, f"Come min_time_from hai immesso un dizionario stringa:intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'latest_time_to' in self.goals:
            latest_time_to_g = self.goals['latest_time_to']
            if type(latest_time_to_g) != dict:
                return sef.format_NO(latest_time_to_g, f"Come latest_time_to hai immesso '{latest_time_to_g}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in latest_time_to_g.keys()):
                return sef.format_NO(latest_time_to_g, f"Come chiavi del latest_time_to hai immesso '{latest_time_to_g.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(delay) != int for delay in latest_time_to_g.values()):
                return sef.format_NO(latest_time_to_g, f"Come valori del latest_time_to hai immesso '{latest_time_to_g.values()}' dove era invece richiesto di immettere degli int.")
            sef.format_OK(latest_time_to_g, f"Come latest_time_to hai immesso un dizionario stringa:intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_path_to' in self.goals:
            critical_path_to_g = self.goals['critical_path_to']
            if type(critical_path_to_g) != dict:
                return sef.format_NO(critical_path_to_g, f"Come critical_path_to hai immesso '{critical_path_to_g}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in critical_path_to_g.keys()):
                return sef.format_NO(critical_path_to_g, f"Come chiavi hai immesso '{critical_path_to_g.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(path) != list for path in critical_path_to_g.values()):
                return sef.format_NO(critical_path_to_g, f"Come valori hai immesso '{critical_path_to_g.values()}' dove era invece richiesto di immettere una lista.")
            for path in critical_path_to_g.values():
                if any(type(node) != str for node in path):
                    return sef.format_NO(critical_path_to_g, f"Come nodo contenuto nel valore hai immesso valori non di tipo stringa.")
            sef.format_OK(critical_path_to_g, f"Come critical_path_to hai immesso un dizionario come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_nodes_to' in self.goals:
            critical_nodes_to_g = self.goals['critical_nodes_to']
            if type(critical_nodes_to_g) != dict:
                return sef.format_NO(critical_nodes_to_g, f"Come critical_nodes_to hai immesso '{critical_nodes_to_g}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in critical_nodes_to_g.keys()):
                return sef.format_NO(critical_nodes_to_g, f"Come chiavi hai immesso '{critical_nodes_to_g.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(path) != list for path in critical_nodes_to_g.values()):
                return sef.format_NO(critical_nodes_to_g, f"Come valori hai immesso '{critical_nodes_to_g.values()}' dove era invece richiesto di immettere una lista.")
            for path in critical_nodes_to_g.values():
                if any(type(node) != str for node in path):
                    return sef.format_NO(critical_nodes_to_g, f"Come nodo contenuto nel valore hai immesso valori non di tipo stringa.")
            sef.format_OK(critical_nodes_to_g, f"Come critical_nodes_to hai immesso un dizionario come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")

        if 'critical_arcs_to' in self.goals:
            critical_arcs_to_g = self.goals['critical_arcs_to']
            if type(critical_arcs_to_g) != dict:
                return sef.format_NO(critical_arcs_to_g, f"Come critical_arcs_to hai immesso '{critical_arcs_to_g}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in critical_arcs_to_g.keys()):
                return sef.format_NO(critical_arcs_to_g, f"Come chiavi hai immesso '{critical_arcs_to_g.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(path) != list for path in critical_arcs_to_g.values()):
                return sef.format_NO(critical_arcs_to_g, f"Come valori hai immesso '{critical_arcs_to_g.values()}' dove era invece richiesto di immettere una lista.")
            for path in critical_arcs_to_g.values():
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
            if type(sensible_to_focus_arc_g) != dict:
                return sef.format_NO(sensible_to_focus_arc_g, f"Come sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g}' dove era invece richiesto di immettere un dizionario.")
            if any(type(node) != str for node in sensible_to_focus_arc_g.keys()):
                return sef.format_NO(sensible_to_focus_arc_g, f"Come chiavi del sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g.keys()}' dove era invece richiesto di immettere delle stringhe.")
            if any(type(delay) != bool for delay in sensible_to_focus_arc_g.values()):
                return sef.format_NO(sensible_to_focus_arc_g, f"Come valori del sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g.values()}' dove era invece richiesto di immettere dei bool.")
            sef.format_OK(sensible_to_focus_arc_g, f"Come sensible_to_focus_arc hai immesso un dizionario stringa:bool come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi il valore giusto, ma il formato è comunque corretto.")
    
        return True

    def verify_feasibility(self, sef):
        """
        Verifica che le risposte che il problem solver ha inserito siano sensate rispetto all'istanza del problema.
        """
        if not super().verify_feasibility(sef):
            return False
        
        n = self.input_data_assigned['n']
        labels = self.input_data_assigned['labels']
        #arcs = self.input_data_assigned['arcs']
        #arcs_removed = self.input_data_assigned['arcs_removed']
        #arcs_added = self.input_data_assigned['arcs_added']
        #focus_node = self.input_data_assigned['focus_node']
        #focus_arc = self.input_data_assigned['focus_arc']

        if 'cert_YES' in self.goals:
            cert_YES_g = self.goals['cert_YES']
            if any(node not in labels for node in cert_YES_g):
                return sef.feasibility_NO(cert_YES_g, f"Nel cert_YES hai immesso '{cert_YES_g}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(cert_YES_g, f"Nel cert_YES hai immesso correttamente nodi esistenti.")

        if 'cert_NO' in self.goals:
            cert_NO_g = self.goals['cert_NO']
            if any(node not in labels for node in cert_NO_g):
                return sef.feasibility_NO(cert_NO_g, f"Nel cert_NO hai immesso '{cert_NO_g}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(cert_NO_g, f"Nel cert_NO hai immesso correttamente nodi esistenti.")

        if 'earliest_time_to_focus_node' in self.goals:
            earliest_time_to_focus_node_g = self.goals['earliest_time_to_focus_node']
            if earliest_time_to_focus_node_g < 0:
                return sef.feasibility_NO(earliest_time_to_focus_node_g, f"Come earliest_time_to_focus_node hai immesso '{earliest_time_to_focus_node_g}' dove era invece richiesto di immettere un valore intero positivo.")
            sef.feasibility_OK(earliest_time_to_focus_node_g, f"Come earliest_time_to_focus_node hai immesso correttamente un valore intero positivo.")

        if 'latest_time_for_focus_node' in self.goals:
            latest_time_for_focus_node_g = self.goals['latest_time_for_focus_node']
            if latest_time_for_focus_node_g < 0:
                return sef.feasibility_NO(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso '{latest_time_for_focus_node_g}' dove era invece richiesto di immettere un valore intero positivo.")
            sef.feasibility_OK(latest_time_for_focus_node_g, f"Come latest_time_for_focus_node hai immesso correttamente un valore intero positivo.")

        if 'critical_path_to_focus_node' in self.goals:
            critical_path_to_focus_node_g = self.goals['critical_path_to_focus_node']
            if any(node not in labels for node in critical_path_to_focus_node_g):
                return sef.feasibility_NO(critical_path_to_focus_node_g, f"Nel critical_path_to_focus_node hai immesso '{critical_path_to_focus_node_g}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(critical_path_to_focus_node_g, f"Nel critical_path_to_focus_node hai immesso correttamente nodi esistenti.")

        if 'nodes_sensible_to_focus_arc' in self.goals:
            nodes_sensible_to_focus_arc_g = self.goals['nodes_sensible_to_focus_arc']
            if any(node not in labels for node in nodes_sensible_to_focus_arc_g):
                return sef.feasibility_NO(nodes_sensible_to_focus_arc_g, f"Nel nodes_sensible_to_focus_arc hai immesso '{nodes_sensible_to_focus_arc_g}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(nodes_sensible_to_focus_arc_g, f"Nel nodes_sensible_to_focus_arc hai immesso correttamente nodi esistenti.")

        if 'critical_path_from_focus_node' in self.goals:
            critical_path_from_focus_node_g = self.goals['critical_path_from_focus_node']
            if any(node not in labels for node in critical_path_from_focus_node_g):
                return sef.feasibility_NO(critical_path_from_focus_node_g, f"Nel critical_path_from_focus_node hai immesso '{critical_path_from_focus_node_g}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(critical_path_from_focus_node_g, f"Nel critical_path_from_focus_node hai immesso correttamente nodi esistenti.")

        if 'min_time_to' in self.goals:
            min_time_to_g = self.goals['min_time_to']
            if any(node not in labels for node in min_time_to_g.keys()):
                return sef.feasibility_NO(min_time_to_g, f"Nel min_time_to hai immesso '{min_time_to_g}' dove sono presenti nodi non esistenti.")
            if any(delay < 0 for delay in min_time_to_g.values()):
                return sef.feasibility_NO(min_time_to_g, f"Nel min_time_to hai immesso '{min_time_to_g}' dove sono presenti delay negativi.")
            sef.feasibility_OK(min_time_to_g, f"Nel min_time_to hai immesso correttamente nodi esistenti con delay positivi")
            
        if 'min_time_from' in self.goals:
            min_time_from_g = self.goals['min_time_from']
            if any(node not in labels for node in min_time_from_g.keys()):
                return sef.feasibility_NO(min_time_from_g, f"Nel min_time_from hai immesso '{min_time_from_g}' dove sono presenti nodi non esistenti.")
            if any(delay < 0 for delay in min_time_from_g.values()):
                return sef.feasibility_NO(min_time_from_g, f"Nel min_time_from hai immesso '{min_time_from_g}' dove sono presenti delay negativi.")
            sef.feasibility_OK(min_time_from_g, f"Nel min_time_from hai immesso correttamente nodi esistenti con delay positivi")

        if 'latest_time_to' in self.goals:
            latest_time_to_g = self.goals['latest_time_to']
            if any(node not in labels for node in latest_time_to_g.keys()):
                return sef.feasibility_NO(latest_time_to_g, f"Nel latest_time_to hai immesso '{latest_time_to_g}' dove sono presenti nodi non esistenti.")
            if any(delay < 0 for delay in latest_time_to_g.values()):
                return sef.feasibility_NO(latest_time_to_g, f"Nel latest_time_to hai immesso '{latest_time_to_g}' dove sono presenti delay negativi.")
            sef.feasibility_OK(latest_time_to_g, f"Nel latest_time_to hai immesso correttamente nodi esistenti con delay positivi")

        if 'critical_path_to' in self.goals:
            critical_path_to_g = self.goals['critical_path_to']
            if any(node not in labels for node in critical_path_to_g.keys()):
                return sef.feasibility_NO(critical_path_to_g, f"Nel critical_path_to hai immesso '{critical_path_to_g}' dove sono presenti nodi non esistenti.")
            for path in critical_path_to_g.values():
               if any(node not in labels for node in path):
                    return sef.feasibility_NO(critical_path_to_g, f"Nel critical_path_to hai immesso '{critical_path_to_g}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(critical_path_to_g, f"Come critical_path_to hai immesso correttamente nodi esistenti.")

        if 'critical_nodes_to' in self.goals:
            critical_nodes_to_g = self.goals['critical_nodes_to']
            if any(node not in labels for node in critical_nodes_to_g.keys()):
                return sef.feasibility_NO(critical_nodes_to_g, f"Nel critical_nodes_to hai immesso '{critical_nodes_to_g}' dove sono presenti nodi non esistenti.")
            for path in critical_nodes_to_g.values():
               if any(node not in labels for node in path):
                    return sef.feasibility_NO(critical_nodes_to_g, f"Nel critical_nodes_to hai immesso '{critical_nodes_to_g}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(critical_nodes_to_g, f"Come critical_nodes_to hai immesso correttamente nodi esistenti.")

        if 'critical_arcs_to' in self.goals:
            critical_arcs_to_g = self.goals['critical_arcs_to']
            if any(node not in labels for node in critical_arcs_to_g.keys()):
                return sef.feasibility_NO(critical_arcs_to_g, f"Come chiavi hai immesso '{critical_arcs_to_g.keys()}' dove sono presenti nodi non esistenti.")
            for path in critical_arcs_to_g.values():
                for tup in path:
                    if tup[0] not in labels or tup[1] not in labels:
                        return sef.feasibility_NO(critical_arcs_to_g, f"All'interno delle tuple ci sono nodi non esistenti.")
            sef.feasibility_OK(critical_arcs_to_g, f"Nel critical_arcs_to hai immesso correttamente nodi esistenti.")

        if 'sensible_to_focus_arc' in self.goals:
            sensible_to_focus_arc_g = self.goals['sensible_to_focus_arc']
            if any(node not in labels for node in sensible_to_focus_arc_g.keys()):
                return sef.feasibility_NO(sensible_to_focus_arc_g, f"Nel sensible_to_focus_arc hai immesso '{sensible_to_focus_arc_g.keys()}' dove sono presenti nodi non esistenti.")
            sef.feasibility_OK(sensible_to_focus_arc_g, f"Nel sensible_to_focus_arc hai immesso correttamente solo nodi esistenti.")

        return True

    def verify_consistency(self, sef):
        """
        Verifica che le risposte inserite dall'utente siano consistenti tra di loro.
        """
        if not super().verify_consistency(sef):
            return False

        edges = ast.literal_eval(self.I.edges)

        # la soluzione ottima opt_sol deve avere lo stesso peso dichiarato in opt_val
        if 'opt_sol' in self.goals and 'opt_val' in self.goals:
            opt_sol_g = self.goals['opt_sol']
            opt_val_g = self.goals['opt_val']
            opt_sol_answ = ast.literal_eval(opt_sol_g.answ)
            if (tot := sum([edges[i][1] for i in opt_sol_answ])) != opt_val_g.answ:
                return sef.consistency_NO(['opt_val', 'opt_sol'], f"La somma dei pesi degli archi in '{opt_sol_g.alias}' è {tot}, che è diverso dal valore immesso in '{opt_val_g.alias}' ({opt_val_g.answ}).")
            sef.consistency_OK(['opt_sol', 'opt_val'], f"Il peso totale di '{opt_sol_g.alias}' è effettivamente {tot}, come immesso in '{opt_val_g.alias}'.", f"Ora resta da verificare l'ottimalità di entrambi.")

        # tutte gli mst della lista list_opt_sols devono avere lo stesso peso
        if 'list_opt_sols' in self.goals:
            list_opt_sols_g = self.goals['list_opt_sols']
            answ = ast.literal_eval(list_opt_sols_g.answ)
            answ_no_reps = []
            # verifica che in list_op_sols non ci siano delle soluzioni ripetute
            for tree in answ:
                new_tree = set(tree)
                if new_tree not in answ_no_reps:
                    answ_no_reps.append(new_tree)
                else:
                    return sef.consistency_NO(['list_opt_sols'], f"All'interno di '{list_opt_sols_g.alias}' sono presenti delle soluzioni ripetute, pertanto la lista delle soluzioni non è valida.")
            # verifica che le soluzioni in list_opt_sols abbiano lo stesso peso
            sols_weights = [sum([edges[i][1] for i in tree]) for tree in answ]
            if len(set(sols_weights)) != 1:
                return sef.consistency_NO(['list_opt_sols'], f"Non tutte le soluzioni in '{list_opt_sols_g.alias}' hanno lo stesso peso, pertanto la lista delle soluzioni non è valida.")
            sef.consistency_OK(['list_opt_sols'], f"Tutte le soluzioni in '{self.goals}' hanno lo stesso peso.", f"Ora resta da verificare l'ottimalità.")

        # verifica che list_opt_sols contenga lo stesso numero di soluzioni dichiarate in num_opt_sols
        if 'list_opt_sols' in self.goals and 'num_opt_sols' in self.goals:
            list_opt_sols_g = self.goals['list_opt_sols']
            num_opt_sols_g = self.goals['num_opt_sols']
            list_opt_sols_answ = ast.literal_eval(list_opt_sols_g.answ)
            if num_opt_sols_g.answ != len(list_opt_sols_answ):
                return sef.consistency_NO(['list_opt_sols', 'num_opt_sols'], f"Come '{list_opt_sols_g.alias}' hai inserito '{list_opt_sols_g.answ}', ma essa presenta un numero di soluzioni diverso dal valore '{num_opt_sols_g.alias}' immesso, {num_opt_sols_g.answ}.")
            sef.consistency_OK(['list_opt_sols', 'opt_val'], f"Il numero di soluzioni in '{list_opt_sols_g.alias}' corrisponde al valore {num_opt_sols_g.answ} inserito in '{num_opt_sols_g.alias}'.", f"Ora resta da verificare l'ottimalità.")

        # il peso di ogni soluzione in list_opt_sols deve essere quello dichiarato in opt_val
        if 'list_opt_sols' in self.goals and 'opt_val' in self.goals:
            list_opt_sols_g = self.goals['list_opt_sols']
            opt_val_g = self.goals['opt_val']
            list_opt_sols_answ = ast.literal_eval(list_opt_sols_g.answ)
            sols_weights = [sum([edges[i][1] for i in tree]) for tree in list_opt_sols_answ]
            if any(weight != opt_val_g.answ for weight in sols_weights):
                return sef.consistency_NO(['list_opt_sols', 'opt_val'], f"Il peso totale di alcune delle soluzioni in '{list_opt_sols_g.alias}' e il valore di '{opt_val_g.alias}', {opt_val_g.answ}, non corrispondono.")
            sef.consistency_OK(['list_opt_sols', 'opt_val'], f"Il peso totale di ogni soluzione in '{list_opt_sols_g.alias}' corrisponde al valore {opt_val_g.answ} inserito in '{opt_val_g.alias}'.", f"Ora resta da verificare l'ottimalità.")
       
        # se si dichiara un edge_profile devono essere presenti i relativi certificati
        if 'edge_profile' in self.goals:
            edge_profile_g = self.goals['edge_profile']
            if edge_profile_g.answ in ['in_all', 'in_some_but_not_in_all'] and 'edgecut_cert' not in self.goals and 'cutshore_cert' not in self.goals:
                return sef.consistency_NO(['edge_profile', 'edgecut_cert', 'cutshore_cert'], f"Come {edge_profile_g.alias} hai inserito {edge_profile_g.answ}, ma non hai inserito né un cutshore_cert né un edgecut_cert, pertanto '{edge_profile_g.alias}' non può essere certificata.")
            sef.consistency_OK(['edge_profile', 'edgecut_cert', 'cutshore_cert'], f"Hai inserito i certificati adatti al {edge_profile_g.alias} dichiarato.", f"Ora resta da verificare la correttezza.")
            if edge_profile_g.answ == 'in_no' and 'cyc_cert' not in self.goals:
                return sef.consistency_NO(['edge_profile', 'edgecut_cert', 'cutshore_cert'], f"Come {edge_profile_g.alias} hai inserito {edge_profile_g.answ}, ma non hai inserito un cyc_cert, pertanto {edge_profile_g.alias} non può essere certificato.")
            sef.consistency_OK(['edge_profile', 'cyc_cert'], f"Hai inserito i certificati adatti al {edge_profile_g.alias} dichiarato.", f"Ora resta da verificare la correttezza.")

        # edgecut_cert e cutshore_cert devono esprimere lo stesso cut del grafo
        if 'edgecut_cert' in self.goals and 'cutshore_cert' in self.goals:
            edgecut_cert_g = self.goals['edgecut_cert']
            cutshore_cert_g = self.goals['cutshore_cert']
            edgecut_cert = ast.literal_eval(edgecut_cert_g.answ)
            cutshore_cert = ast.literal_eval(cutshore_cert_g.answ)
            if any(((u in cutshore_cert) == (v in cutshore_cert)) for u, v in [list(edges[i][0]) for i in edgecut_cert]):
                # dopo aver estratto gli archi dell'edgecut dalla lista degli edges, verifica che ognuno di questi archi non colleghino due nodi nella stessa shore
                return sef.consistency_NO(['edgecut_cert', 'cutshore_cert'], f"{cutshore_cert_g.answ} e {edgecut_cert_g.answ} non corrispondono allo stesso cut del grafo.")
            sef.consistency_OK(['edgecut_cert', 'cutshore_cert'], f"{cutshore_cert_g.answ} e {edgecut_cert_g.answ} corrispondono allo stesso cut.", f"Ora resta da verificare la correttezza.")

        return True

    def verify_optimality(self, sef):
        """
        Verifica che le risposte inserite dell'utente siano quelle corrette
        """
        if not super().verify_optimality(sef):
            return False

        edges = ast.literal_eval(self.I.edges)
        forbidden_edges = ast.literal_eval(self.I.forbidden_edges)
        forced_edges = ast.literal_eval(self.I.forced_edges)
        query_edge = self.I.query_edge

        # verifica che opt_val sia effettivamente ottimo
        if 'opt_val' in self.goals:
            opt_val_g = self.goals['opt_val']
            true_answ = sef.oracle_dict['opt_val']
            if opt_val_g.answ != true_answ:
                return sef.optimality_NO(opt_val_g, f"Come '{opt_val_g.alias}' ha inserito '{opt_val_g.answ}', tuttavia esso non è il valore minimo possibile, {true_answ}, pertanto il valore non è corretto.")
            sef.optimality_OK(opt_val_g, f"'{opt_val_g.alias}'={true_answ} è effettivamente il valore ottimo.", "")

        # verifica che la soluzione opt_sol sia una delle possibili soluzioni ottime
        if 'opt_sol' in self.goals:
            opt_sol_g = self.goals['opt_sol']
            answ = ast.literal_eval(opt_sol_g.answ)
            list_opt_sols = [set(tree) for tree in self.graph.all_mst(forced_edges, forbidden_edges)]
            if set(answ) not in list_opt_sols:
                return sef.optimality_NO(opt_sol_g, f"Come '{opt_sol_g.alias}' hai inserito {opt_sol_g.answ}, ma essa non è tra le soluzioni ottime, pertanto la soluzione inserita non è corretta.")
            sef.optimality_OK(opt_sol_g, f"{opt_sol_g.alias}={opt_sol_g.answ} é effettivamente una possibile soluzione ottima.", "")

        # a questo punto che ho controllato che le soluzioni dello studente sono tutte diverse e ammissibili e ottime controllare che siano in numero sufficiente.
        if 'num_opt_sols' in self.goals:
            num_opt_sols_g = self.goals['num_opt_sols']
            true_answ = sef.oracle_dict['num_opt_sols']
            if not (self.I.cap_for_num_sols <= num_opt_sols_g.answ or not self.I.cap_for_num_sols <= true_answ) and num_opt_sols_g.answ <= true_answ:
                return sef.optimality_NO(num_opt_sols_g, f"Il valore {num_opt_sols_g.answ} inserito in '{num_opt_sols_g.alias}' differisce dal numero di soluzioni ottime corretto ({true_answ}). {'Il numero di soluzioni trovato non è quello massimo ma è sufficientemente ampio per questo esercizio.' if num_opt_sols_g.answ < true_answ else ''}")
            sef.optimality_OK(num_opt_sols_g, f"'{num_opt_sols_g.alias}' = {num_opt_sols_g.answ} è effettivamente il numero corretto di soluzioni ottime.", "")

        # verifica che la lista delle soluzioni sia corretta (in numero e ottimalità)
        if 'list_opt_sols' in self.goals:
            list_opt_sols_g = self.goals['list_opt_sols']
            answ = ast.literal_eval(list_opt_sols_g.answ)
            if len(answ) < self.I.cap_for_num_sols:
                return sef.optimality_NO(list_opt_sols_g, f"In '{list_opt_sols_g.alias}' hai inserito un numero di soluzioni pari a {len(answ)}, ma il questo numero non è sufficiente.")
            true_list_opt_sols = [set(tree) for tree in self.graph.all_mst(self.I.forced_edges, self.I.forbidden_edges)]
            for tree in answ:
                if set(tree) not in true_list_opt_sols:
                    return sef.optimality_NO(list_opt_sols_g, f"Come '{list_opt_sols_g.alias}' hai inserito {list_opt_sols_g.answ}, ma alcune delle soluzioni al suo interno non sono ottimali.")
            sef.optimality_OK(list_opt_sols_g, f"Come {list_opt_sols_g.alias} hai inserito {list_opt_sols_g.answ}, ed effettivamente questa rappresenta una lista di soluzioni ottimali sufficientemente numerosa.", "")

        # verifica che edge profile sia corretto con relativi certificati
        if 'edge_profile' in self.goals:
            # Controlliamo solo il certificato e diamo informazione solo di King Arthur. (Ossia: o diciamo che il certificato è stato verificato ed è corretto oppure esprimiamo nello specifico che problemi ci siano nel certificato. Poi, eventualmente, verifichiamo la coerenza tra i certificati forniti (ove corretti) e la catalogazione consegnata.)
            edge_profile_g = self.goals['edge_profile']
            if edge_profile_g.answ == 'in_all':
                if 'edgecut_cert' in self.goals:
                    edgecut_cert_g = self.goals['edgecut_cert']
                    edgecut_cert_answ: list = ast.literal_eval(edgecut_cert_g.answ)
                    if any([w <= edges[query_edge][2] for _, _, w, _ in list(filter(lambda x: x[3] in edgecut_cert_answ, edges))]):
                        # ogni peso dell'edgecut sia <= query_edge
                        return sef.optimality_NO(edge_profile_g, f"Secondo il certificato {edgecut_cert_g.alias}, il {edge_profile_g.alias} non è l'arco strettamente minore.")
                    sef.optimality_OK(edge_profile_g, f"Il certificato {edgecut_cert_g.alias} effettivamente dimostra che {edge_profile_g.alias} deve appartenere a tutte le soluzioni ottime.", f"Tuttavia non ho modo di dirti su il '{edge_profile_g.alias}' che hai inserito sia quello corretto.")
                if 'cutshore_cert' in self.goals:
                    cutshore_cert_g = self.goals['cutshore_cert']
                    cutshore_cert_answ: list = ast.literal_eval(cutshore_cert_g.answ)
                    if any([w <= edges[query_edge][2] for u, v, w, l in edges if ((u in cutshore_cert_answ) ^ (v in cutshore_cert_answ)) and l != query_edge]):
                        # arco con peso minore
                        return sef.optimality_NO(edge_profile_g, f"Secondo il certificato {cutshore_cert_g.alias}, il '{edge_profile_g.alias}' non è l'arco strettamente minore.")
                    sef.optimality_OK(edge_profile_g, f"Il certificato {cutshore_cert_g.alias} effettivamente dimostra che '{edge_profile_g.alias}' deve appartenere a tutte le soluzioni ottime.", f"Tuttavia non ho modo di dirti su il '{edge_profile_g.alias}' che hai inserito sia quello corretto.")
            if edge_profile_g.answ == 'in_some_but_not_in_all':
                if 'edgecut_cert' in self.goals:
                    edgecut_cert_g = self.goals['edgecut_cert']
                    edgecut_cert_answ: list = ast.literal_eval(edgecut_cert_g.answ)
                    edgecut_cert_answ.remove(query_edge)
                    if any([w < edges[query_edge][2] for _, _, w, _ in list(filter(lambda x: x[3] in edgecut_cert_answ, edges))]):
                        # query_edge non è uno dei pesi minori
                        return sef.optimality_NO(edge_profile_g, f"Secondo il certificato {edgecut_cert_g.alias}, il {edge_profile_g.alias} non è uno degli archi di peso minimo. pertanto il certificato non dimostra la tua risposta per '{edge_profile_g.alias}' ({edge_profile_g.answ}).")
                    sef.optimality_OK(edge_profile_g, f"Il certificato {edgecut_cert_g.alias} effettivamente dimostra che {edge_profile_g.alias} appartiene ad alcune delle soluzioni ottime.", f"Tuttavia non ho modo di dirti su il '{edge_profile_g.alias}' che hai inserito sia quello corretto.")
                if 'cutshore_cert' in self.goals:
                    cutshore_cert_g = self.goals['cutshore_cert']
                    cutshore_cert_answ: list = ast.literal_eval(cutshore_cert_g.answ)
                    if any([w < edges[query_edge][2] for u, v, w, l in edges if ((u in cutshore_cert_answ) ^ (v in cutshore_cert_answ)) and l != query_edge]):
                        # query_edge non è uno dei pesi minori
                        return sef.optimality_NO(edge_profile_g, f"Secondo il certificato {cutshore_cert_g.alias}, il {edge_profile_g.alias} non è l'arco di peso strettamente minore.")
                    sef.optimality_OK(edge_profile_g, f"Il certificato {cutshore_cert_g.alias} effettivamente dimostra che {edge_profile_g.alias} appartiene ad alcune delle soluzioni ottime.", f"Tuttavia non ho modo di dirti su il '{edge_profile_g.alias}' che hai inserito sia quello corretto.")
            if edge_profile_g.answ == 'in_no':
                if 'cyc_cert' in self.goals:
                    cyc_cert_g = self.goals['cyc_cert']
                    cyc_cert_answ: list = ast.literal_eval(cyc_cert_g.answ)
                    if any([w >= edges[query_edge][2] for _, _, w, _ in list(filter(lambda x: x[3] in cyc_cert_answ, edges))]):
                        # query_edge è quello strettamente maggiore nel ciclo
                        return sef.optimality_NO(edge_profile_g, f"Secondo il certificato {cyc_cert_g.alias}, il {edge_profile_g.alias} non è l'arco strettamente maggiore.")
                    sef.optimality_OK(edge_profile_g, f"Il certificato {cyc_cert_g.alias} effettivamente dimostra che {edge_profile_g.alias} non appartiene a nessuna delle soluzioni ottime.", f"Tuttavia non ho modo di dirti su il '{edge_profile_g.alias}' che hai inserito sia quello corretto.")

        return True

# G = Graph([])
# G.adjList = {'1': [['4', 1]], '2': [['3', 3]], '0': [['5', 4], ['4', 15]], '5': [
#    ['2', 0], ['0', 6]], '3': [['1', 6]], '4': [['0', 5], ['1', 9]]}

# print(isDAG(G))
# print(delay_sum(G, latest_time_to(get_DP_table_path(G,dijkstra_max), '0', '4')))
