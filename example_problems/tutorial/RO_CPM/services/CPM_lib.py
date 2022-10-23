#!/usr/bin/env python3
from sys import stderr
from typing import Optional, List, Dict, Callable

#from RO_verify_submission_gen_prob_lib import verify_submission_gen

instance_objects_spec = [
    ('n',int),
    ('labels','list_of_str'),
    ('arcs','list_of_tuple[str,str,int]'),
    ('arcs_removed','list_of_tuple[str,str,int]'),
    ('arcs_added','list_of_tuple[str,str,int]'),
    ('focus_node',int),
    ('focus_arc','tuple[str,str,int]'),
]
additional_infos_spec=[
    ('partial_to','list_of_tuple[str,int]'),
    ('partial_from','list_of_tuple[str,int]'),
]
answer_objects_spec = {
    'is_a_DAG':bool,
    'cert_YES':'list_of_tuple[str,str,int]',
    'cert_NO':'list_of_tuple[str,str,int]',
    'earliest_time_for_focus_node':int,
    'critical_path_to_focus_node':'list_of_tuple[str,str,int]',
    'nodes_sensible_to_focus_arc':'list_of_tuple[str,str,int]',
    'latest_time_for_focus_node':int,
    'critical_path_from_focus_node':'list_of_tuple[str,str,int]',
    'min_time_to':'list_of_tuple[str,int]',
    'min_time_from':'list_of_tuple[str,int]',
    'latest_time_to':'list_of_tuple[str,int]',
    'critical_path_to':'list_of_tuple[str,list_of_str]',
    'critical_nodes_to':'list_of_tuple[str,list_of_str]',
    'critical_arcs_to':'list_of_tuple[str,list_of_tuple[str,str,int]]',
    'sensible_to_focus_arc':'list_of_tuple[str,bool]',
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
'''
def sum_of_costs_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["costs"], instance["labels"]) if ele in ordered_list_of_elems])

def sum_of_vals_over(instance, ordered_list_of_elems):
    return sum([val for val,ele in zip(instance["vals"], instance["labels"]) if ele in ordered_list_of_elems])
'''

# Una classe per rappresentare un oggetto graph
class Graph:
    # Costruttore
    def __init__(self, arcs, n = 0, labels = [], arcs_removed = [], arcs_added = [], focus_node = '1', focus_arc = ('1','2',5), partial_to = {}, partial_from = {}):
        
        #Assegnamo a V il numero dei vertici
        self.V = n
        
        #Assegnamo a E la lista degli archi
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
        		if(type(head) == type(str)):
        			self.adjList[head].append([tail,delay])
        		else:
        			self.adjList[str(head)].append([str(tail),delay])	
        	
        else:
        	n = len(labels)
        	self.V = n
        	guard = 0
        	# aggiunge archi al graph diretto
        	for (head, tail, delay) in arcs:
        		if guard == 0:
        			self.adjList['0'].append([head,0])
        			guard = 1
        		
        		self.adjList[head].append([tail,delay])
				
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
            time = DFS(graph, trad_rev[u], discovered, departure, time, trad, trad_rev)
 
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
        for i in graph[v]:
            i= i[0]
            if visited[i] == False:
                topologicalSortUtil(i, visited, stack, graph)
 
        # Push current vertex to stack which stores result
        stack.append(v)
 
    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
def topologicalSort(graph):
    # Mark all the vertices as not visited
    visited = [False]*len(graph)
    stack = []

    # Call the recursive helper function to store Topological
    # Sort starting from all vertices one by one
    for i in range(len(graph)):
        if visited[i] == False:
            topologicalSortUtil(i, visited, stack,graph)

    # Print contents of the stack
    print(stack[::-1])  # return list in reverse order
    
    for arc in graph[stack[0]]:
        if arc[0] == stack[-1]:
            return True
    return False

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

def getNeighbors(adjList,node):
    neighbors = []
    for neighbor in adjList[node]:
        neighbors.append(neighbor[0])
    return neighbors
    
def getCostOfNeighbor(adjList,start,end):
    for neigh in adjList[start]:
        if neigh[0] == end:
            return neigh[1]
    return 'inf'

def dijkstra_opt(graph, start_vertex):
    D = {v:[float('inf'),[]] for v in graph.adjList.keys()}
    D[start_vertex][0] = 0
    D[start_vertex][1] = start_vertex
    
    visited = dict()

    pq = PriorityQueue()
    pq.insert((0, start_vertex))

    while not pq.isEmpty():
        (dist, current_vertex) = pq.get()
        visited.update({current_vertex : None})

        for neighbor in graph.adjList.keys():
            neighbors = getNeighbors(graph.adjList,current_vertex)
            if neighbor in neighbors:
                for n in neighbors:
                    if n == neighbor:
                        distance = getCostOfNeighbor(graph.adjList,current_vertex,n)
                        old_cost = D[neighbor][0]
                        new_cost = D[current_vertex][0] + distance
                        if new_cost < old_cost:
                            pq.insert((new_cost, neighbor))
                            D[neighbor][0] = new_cost
                            D[neighbor][1] = D[current_vertex][1]+' '+neighbor
    for key in D.keys():
        D[key] = [D[key][0], D[key][1].split(' ')]
    return D


def getCostOfNeighbor_max(adjList,start,end):
    for neigh in adjList[start]:
        if neigh[0] == end:
            return neigh[1]
    return 0

def dijkstra_max(graph, start_vertex):
    D = {v:[float(0),[]] for v in graph.adjList.keys()}
    D[start_vertex][0] = 0
    D[start_vertex][1] = start_vertex
    
    visited = dict()

    pq = PriorityQueue()
    pq.insert((0, start_vertex))

    while not pq.isEmpty():
        (dist, current_vertex) = pq.get()
        visited.update({current_vertex : None})

        for neighbor in graph.adjList.keys():
            neighbors = getNeighbors(graph.adjList,current_vertex)
            if neighbor in neighbors:
                for n in neighbors:
                    if n == neighbor:
                        distance = getCostOfNeighbor(graph.adjList,current_vertex,n)
                        old_cost = D[neighbor][0]
                        new_cost = D[current_vertex][0] + distance
                        if new_cost > old_cost and neighbor not in D[current_vertex][1]:
                            pq.insert((new_cost, neighbor))
                            D[neighbor][0] = new_cost
                            D[neighbor][1] = D[current_vertex][1]+' '+neighbor
    for key in D.keys():
        D[key] = [D[key][0], D[key][1].split(' ')]
    return D
   

def get_DP_table(G, algo):
    DP_rows={}
    for nodoK in sorted(G.adjList):
        dijks = algo(G,nodoK)
        for key in dijks.keys():
            dijks[key] = dijks[key][0]
        DP_rows[nodoK] = dijks
    return DP_rows

def get_DP_table_path(G,algo):
    DP_rows={}
    for nodoK in sorted(G.adjList):
        dijks = algo(G,nodoK)
        for key in dijks.keys():
            dijks[key] = dijks[key][1]
        DP_rows[nodoK] = dijks
    return DP_rows
    
def min_time_to(table,start,end):
    return table[start][end]
    
def min_time_from(table,start,end):
    return table[end][start]
    
def latest_time_to(table,start,end):
    return table[start][end]
    
def critical_path_to(table,start,end):
    return table[start][end]
    
def critical_nodes_to(table,start,end):
    nodes = critical_path_to(table,start,end)
    nodes.pop(-1)
    return nodes
    
def critical_arcs_to(table,start,end):
    path = critical_path_to(table,start,end)
    arcs = []
    old_node = None
    for node in path:
        if old_node is None:
            old_node = node
            continue
        arcs.append((old_node,node))
        old_node = node
    return arcs
    
def sensible_to_focus_arc(table,start,focus_arc):
    result = dict()
    for key in table.keys():
        arcs = critical_arcs_to(table,start,key)
        result[key] = focus_arc in arcs
    return result


def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    labels = instance["labels"]

    n = len(instance["labels"])
    chk_labels = False
    if n==0:
        chk_labels = True
        n = instance["n"]
        labels = []
        for i in range(1, n+1):
            labels.append(str(i))

    for arc in instance["arcs"]:
        if (arc[0] not in labels or arc[1] not in labels):
            print('ERRORE: Nell\'arco {} in "arcs" è presente un nodo non definito'.format(arc))
            exit(0)
        if(get_nodes_from_arcs(instance["arcs"]).count((arc[0],arc[1])) > 1):
            print('ERRORE: l\'arco {} è ripetuto in "arcs"'.format(arc))
            exit(0)

    for arc in instance["arcs_removed"]:
        if (arc not in instance["arcs"]):
            print('ERRORE: Nell\'arco {} in "arcs_removed" è presente un nodo non definito'.format(arc))
            exit(0)

    for arc in instance["arcs_added"]:
        if (arc not in instance["arcs"]):
            print('ERRORE: Nell\'arco {} in "arcs_added" è presente un nodo non definito'.format(arc))
            exit(0)

    if chk_labels:
        if str(instance["focus_node"]) not in labels:
            print ('ERRORE: Il nodo "focus_node" {} non è definito'.format(instance["focus_node"]))
            exit(0)

    for arc in instance["focus_arc"]:
        if (arc not in instance["arcs"] and arc not in instance["arcs_added"]):
            print('ERRORE: L\'arco {} non è presente in "arcs_added" nè in "arcs"'.format(arc))
            exit(0)
            
'''
        
def solver(input_to_oracle):
    #print(f"input_to_oracle={input_to_oracle}",file=stderr)
    I = input_to_oracle["input_data_assigned"]
    #print(f"Instance={I}",file=stderr)
    n = len(I["labels"])
    LB = I["LB"]
    UB = I["UB"]
    if len(UB)==0:
        LB = [0]*n
        UB = [1]*n

    DPtable_opt_val = [[0 for j in range(I["Knapsack_Capacity"]+1)] for i in range(n+1)]
    DPtable_num_opts = [[1 for j in range(I["Knapsack_Capacity"]+1)] for i in range(n+1)]
    for obj_label,i in zip(I["labels"],range(1,1+n)): # i=object index, but also i=row_index (row_indexes of the DP table start from zero, the first row is already computed as a base case, before entering this for loop)
        obj_cost = I["costs"][i-1]; obj_val = I["vals"][i-1]
        if obj_label in I["forced_in"]:
            LB[i-1] = 1
        if obj_label in I["forced_out"]:
            UB[i-1] = 0
        obj_LB = LB[i-1]; obj_UB = UB[i-1]
        for j in range(I["Knapsack_Capacity"]+1): # j=column_index of the DP table 
            DPtable_opt_val[i][j] = DPtable_opt_val[i-1][j]
            DPtable_num_opts[i][j] = DPtable_num_opts[i-1][j]
            obj_times = 1
            while obj_times <= obj_UB and obj_times*obj_cost <= j:
                #print(f"i={i}, obj_label={obj_label}, obj_cost={obj_cost}, obj_val={obj_val}, j={j}, obj_times={obj_times}",file=stderr)
                if DPtable_opt_val[i][j] == obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                    DPtable_num_opts[i][j] += DPtable_num_opts[i-1][j-obj_times*obj_cost]
                elif DPtable_opt_val[i][j] < obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                    DPtable_opt_val[i][j] = obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]
                    DPtable_num_opts[i][j] = DPtable_num_opts[i-1][j]
                obj_times += 1
        #print(f"DPtable_opt_val={DPtable_opt_val}",file=stderr)
        #print(f"DPtable_num_opts={DPtable_num_opts}",file=stderr)
        
    #print(f"DPtable_opt_val={DPtable_opt_val}",file=stderr)
    #print(f"DPtable_num_opts={DPtable_num_opts}",file=stderr)

    def yield_opt_sols_list(i,j,promise,num_opt_sols_MAX):
        assert promise >= 0 and j >= 0 and i >= 0   
        if i == 0:
            assert promise == 0
            yield []
            return
        obj_label = I["labels"][i-1]
        obj_cost = I["costs"][i-1]; obj_val = I["vals"][i-1]
        obj_LB = LB[i-1]; obj_UB = UB[i-1]
        #print(f'\ni={i}\nj={j}\npromise={promise}\nnum_opt_sols_MAX={num_opt_sols_MAX}\nobj_label={obj_label}\nobj_cost={obj_cost}\nobj_val={obj_val}\nobj_LB={obj_LB}\nobj_UB={obj_UB}', file=stderr)
        for obj_times in range(obj_UB+1):
            if obj_times*obj_cost > j:
                break
            if promise <= obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                assert promise == obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]
                for opt_sol in yield_opt_sols_list(i-1,j-obj_times*obj_cost,promise-obj_times*obj_val,num_opt_sols_MAX):
                    if num_opt_sols_MAX > 0:
                        yield opt_sol + [obj_label]*obj_times
                        num_opt_sols_MAX -= 1

    if n == 0:
        opt_val = 0; num_opt_sols = 1; list_opt_sols = [[]]
    else:
        opt_val=DPtable_opt_val[i][j]; num_opt_sols=DPtable_num_opts[i][j]
    num_opt_sols_MAX=I['CAP_FOR_NUM_OPT_SOLS']
    list_opt_sols = list(yield_opt_sols_list(i,j,promise=opt_val,num_opt_sols_MAX=num_opt_sols_MAX))
    opt_sol = list_opt_sols[0]
    #print(f"opt_sol={opt_sol}\nopt_val={opt_val}\nnum_opt_sols={num_opt_sols}\nDPtable_opt_val={DPtable_opt_val}\nDPtable_num_opts={DPtable_num_opts}\nlist_opt_sols={list_opt_sols}", file=stderr)
    oracle_answers = {}
    for std_name in answer_objects_spec:
        oracle_answers[std_name] = locals()[std_name]
        if std_name in input_to_oracle["request"]:
            ad_hoc_name = input_to_oracle["request"][std_name]
            oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers

#------------------LASCIARE STANDARD-------------------------------------------------------------------------
class verify_submission_problem_specific(verify_submission_gen):
    def __init__(self, SEF,input_data_assigned:Dict, long_answer_dict:Dict, oracle_response:Dict = None):
        super().__init__(SEF,input_data_assigned, long_answer_dict, oracle_response)

    def verify_format(self, SEF):
        if not super().verify_format(SEF):
            return False
        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        if 'num_opt_sols' in self.goals:
            g = self.goals['num_opt_sols']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            if type(g.answ) != list:
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una lista di oggetti (esempio ['{self.I.labels[0]}','{self.I.labels[2]}']). Hai invece immesso `{g.answ}`.")
            for ele in g.answ:
                if ele not in self.I.labels:
                    return SEF.format_NO(g, f"Ogni oggetto che collochi nella lista `{g.alias}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {self.I.labels}.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ammissibilità di `{g.alias}`")
        return True
                
    def set_up_and_cash_handy_data(self):
        if 'opt_sol' in self.goals:
            self.sum_vals = sum([val for ele,cost,val in zip(self.I.labels,self.I.costs,self.I.vals) if ele in self.goals['opt_sol'].answ])
            self.sum_costs = sum([cost for ele,cost,val in zip(self.I.labels,self.I.costs,self.I.vals) if ele in self.goals['opt_sol'].answ])
            
    def verify_feasibility(self, SEF):
        if not super().verify_feasibility(SEF):
            return False
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            for ele in g.answ:
                if ele in self.I.forced_out:
                    return SEF.feasibility_NO(g, f"L'oggetto `{ele}` da tè inserito nella lista `{g.alias}` è tra quelli proibiti. Gli oggetti proibiti per la Richiesta {str(SEF.task_number)}, sono {self.I.forced_out}.")
            for ele in self.I.forced_in:
                if ele not in g.answ:
                    return SEF.feasibility_NO(g, f"Nella lista `{g.alias}` hai dimenticato di inserire l'oggetto `{ele}` che invece è forzato. Gli oggetti forzati per la Richiesta {str(SEF.task_number)} sono {self.I.forced_in}.")
            if self.sum_costs > self.I.Knapsack_Capacity:
                return SEF.feasibility_NO(g, f"La tua soluzione in `{g.alias}` ha costo {self.sum_costs} > Knapsack_Capacity e quindi NON è ammissibile in quanto fora il budget per la Richiesta {str(SEF.task_number)}. La soluzione da tè inserita ricomprende il sottoinsieme di oggetti `{g.alias}`= {g.answ}.")
            SEF.feasibility_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ottimalità di `{g.alias}`")
        return True
                
    def verify_consistency(self, SEF):
        if not super().verify_consistency(SEF):
            return False
        if 'opt_val' in self.goals and 'opt_sol' in self.goals:
            g_val = self.goals['opt_val']; g_sol = self.goals['opt_sol']
            if self.sum_vals != g_val.answ:
                return SEF.consistency_NO(['opt_val','opt_sol'], f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {self.sum_vals}, non {g_val.answ} come hai invece immesso in `{g_val.alias}`. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            SEF.consistency_OK(['opt_val','opt_sol'], f"{g_val.alias}={g_val.answ} = somma dei valori sugli oggetti in `{g_sol.alias}`.", f"resta da stabilire l'ottimalità di `{g_val.alias}` e `{g_sol.alias}`")
        return True

    def verify_optimality(self, SEF):
        if not super().verify_optimality(SEF):
            return False
        true_opt_val = SEF.oracle_dict['opt_val']
        true_opt_sol = SEF.oracle_dict['opt_sol']
        if 'opt_val' in self.goals:
            g_val = self.goals['opt_val']
            if true_opt_val != g_val.answ:
                return SEF.optimality_NO(g_val, f"Il valore ottimo corretto è {true_opt_val} {'>' if true_opt_val != g_val.answ else '<'} {g_val.answ}, che è il valore invece immesso in `{g_val.alias}`. Una soluzione di valore ottimo è {true_opt_sol}.")
            else:
                SEF.optimality_OK(g_val, f"{g_val.alias}={g_val.answ} è effettivamente il valore ottimo.", "")
        if 'opt_sol' in self.goals:
            g_sol = self.goals['opt_sol']
            g_sol_answ = self.goals['opt_sol'].answ
            g_val_answ = sum([val for ele,cost,val in zip(self.I.labels,self.I.costs,self.I.vals) if ele in g_sol_answ])
            assert g_val_answ <= true_opt_val
            if g_val_answ < true_opt_val:
                return SEF.optimality_NO(g_sol, f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {g_val_answ} < {true_opt_val}, valore corretto per una soluzione ottima quale {true_opt_sol}. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            else:
                SEF.optimality_OK(g_sol, f"Confermo l'ottimailtà della soluzione {g_sol.alias}={g_sol.answ}.", "")
        return True
        '''
    
G = Graph([])
G.adjList = {'1': [['4',1]], '2': [['3',3]], '0':[['5',4],['4',15]], '5':[['2',0],['0',6]], '3':[['1',6]], '4':[['0',5],['1',9]]}
    
print(isDAG(G))
print(sensible_to_focus_arc(get_DP_table_path(G,dijkstra_opt),'0',('2','3')))
