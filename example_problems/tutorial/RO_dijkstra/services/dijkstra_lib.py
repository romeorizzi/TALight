import ast
import networkx as nx
from sys import stderr
from typing import Dict
from RO_verify_submission_gen_prob_lib import verify_submission_gen

# specifiche dell'istanza del problema
instance_objects_spec = [
    ('n', int),                     # numero di nodi
    ('m', int),                     # numero di archi
    ('s', int),                     # indice nodo sorgente
    ('t', int),                     # indice nodo terminazione
    ('edges', str),                 # lista degli archi
    ('query_edge', int),            # indice arco da analizzare
    ('CAP_FOR_NUM_SOLS', int),      # limite al numero di soluzioni ammissibili sottomesse
    ('CAP_FOR_NUM_OPT_SOLS', int)   # limite al numero di soluzioni ottime sottomesse
]

additional_infos_spec=[]

required_objects_spec = [
    ('n', int),                     # numero di nodi
    ('m', int),                     # numero di archi
    ('s', int),                     # indice nodo sorgente
    ('t', int),                     # indice nodo terminazione
    ('edges', str),                 # lista degli archi
    ('query_edge', int),            # indice arco da analizzare
    ('CAP_FOR_NUM_SOLS', int),      # limite al numero di soluzioni ammissibili sottomesse
    ('CAP_FOR_NUM_OPT_SOLS', int)   # limite al numero di soluzioni ottime sottomesse
]

# specifiche delle risposte dell'utente
answer_objects_spec = {
    'opt_dist' : int,                       # minima distanza s ->-> t
    'opt_dists' : str,                      # lista delle distanze s ->-> v, per ogni v
    'opt_path' : str,                       # lista degli archi da percorrere per completare il tragitto s ->-> t
    'opt_tree' : str,                       # albero dei cammini minimi s ->-> v, per ogni v
    'num_opt_paths' : int,                  # numero di cammini a distanza minima differenti
    'num_opt_trees' : int,                  # numero di alberi dei cammini minimi differenti
    'list_opt_paths' : str,                 # lista di tutti i cammini minimi differenti
    'list_opt_trees' : str,                 # lista di tutti gli alberi dei cammini minimi differenti
    'edge_profile' : str,                   # risultato dell'analisi sul query edge
    'nodes_relying_on_query_edge' : str     # lista dei nodi la cui distanza da s dipende dal query edge
}

# lista delle soluzioni implementate
answer_objects_implemented = [
    'opt_dist',
    'opt_dists',
    'opt_path',
    'opt_tree',
    'num_opt_paths',
    'num_opt_trees',
    'list_opt_paths',
    'list_opt_trees',
    'edge_profile',
    'nodes_relying_on_query_edge'
]

limits = {
    'CAP_FOR_NUM_SOLS' : 100,
    'CAP_FOR_NUM_OPT_SOLS' : 100
}

def check_instance_parameters_and_types(instance):
    # Verifico la presenza di tutti i parametri previsti per la definizione dell'istanza e la correttezza del relativo tipo 
    try:
        for obj in required_objects_spec:
            key = obj[0]
            T = obj[1]
            if key not in instance.keys():
                return False
            if type(instance[key]) != T:
                return False
        return True
    except:
        return False

def check_raw_edge_list_consistency(raw_edges):
    # Verifico che ogni arco fornito nell'istanza abbia il giusto numero di elementi a rappresentarlo e la struttura corretta
    # (({int, int}), int)
    try:
        raw_edge_list = ast.literal_eval(raw_edges)
        for raw_edge in raw_edge_list:
            if type(raw_edge) != tuple:
                return False
            edge = raw_edge[0]
            if type(edge) == set or type(edge) == tuple:
                edge = list(edge)
            else:
                return False
            if len(edge) + len(raw_edge) != 4:
                return False
            if not ((type(raw_edge[1]) == int) and (type(edge[0]) == int) and (type(edge[1]) == int)):
                return False
        return True
    except:
        return False

def process_raw_list_to_get_edge_list(raw_edge_list: list) -> list:
    # Processo l'elenco di archi fornito nell'istanza e lo strutturo come lista in cui ogni elemento è nella forma:
    # (u, v, w, c) u nodo sorgente, v nodo destinazione, w lunghezza dell'arco, c = 1 arco nato dal collasso di un arco non diretto
    
    edge_list = []
    for raw_edge in raw_edge_list:
        edge = raw_edge[0]
        w = raw_edge[1]
        if type(edge) == set:
            directed = False
            edge = list(edge)
        else:
            directed = True
        u = edge[0]
        v = edge[1]

        if not directed:
            if len([x for x in edge_list if (x[0] == u and x[1] == v) or (x[0] == v and x[1] == u)]) != 0:
                print(f"Errore: un arco {u} - {v} è già presente nel grafo in istanza.")
                exit(0)
        else:
            if len([x for x in edge_list if (x[0] == u and x[1] == v)]) != 0:
                print(f"Errore: un arco diretto {u} - {v} è già presente nel grafo in istanza.")
                exit(0)
            if len([x for x in edge_list if (x[0] == v and x[1] == u)]) > 1:
                print(f"Errore: più di due archi diretti tra i nodi {u} - {v} sono privi di senso.")
                exit(0)

        edge_list.append((u,v,w,0))
        if not directed:
            edge_list.append((v,u,w,1))
    
    return edge_list

def rec_dfs(visited, s, edge_list):
    # DFS ricorsiva
    visited.add(s)
    reachable_vertexes = [v[1] for v in edge_list if v[0] == s and v[1] not in visited]
    for v in reachable_vertexes:
        if v not in visited:
            visited = rec_dfs(visited, v, edge_list)
    return visited

def DFS(s, edge_list):
    # Semplice implementazione dell'algoritmo di visita DFS, restituisco la lista di nodi visitati a partire da s, con una singola visita DFS
    visited = set()
    visited = rec_dfs(visited, s, edge_list)
    return visited

def check_connectivity(s, n, edge_list):
    # Verifico che non esistano nodi NON raggiungibili a partire da s
    if len(DFS(s, edge_list)) != n:
        return False
    else:
        return True
    
def process_raw_list_to_get_edge_list_with_directions(raw_edge_list: list) -> list:
    # Processo l'elenco di archi fornito nell'istanza e lo strutturo come lista in cui ogni elemento è nella forma:
    # (u, v, w, d) u nodo sorgente, v nodo destinazione, w lunghezza dell'arco, d = 1 arco diretto
    
    edge_list = []
    for raw_edge in raw_edge_list:
        edge = raw_edge[0]
        w = raw_edge[1]
        if type(edge) == set:
            d = 0
            edge = list(edge)
        else:
            d = 1
        u = edge[0]
        v = edge[1]

        edge_list.append((u,v,w,d))
    
    return edge_list

def process_raw_list_to_get_condensed_edge_list(raw_edge_list: list) -> list:
    # Processo l'elenco di archi fornito nell'istanza e lo strutturo come lista in cui ogni elemento è nella forma:
    # (u, v, w) u nodo sorgente, v nodo destinazione, w lunghezza dell'arco
    
    edge_list = []
    for raw_edge in raw_edge_list:
        edge = raw_edge[0]
        w = raw_edge[1]
        if type(edge) == set:
            edge = list(edge)
        u = edge[0]
        v = edge[1]

        edge_list.append((u,v,w))
    
    return edge_list
    
def check_path(s, t, path, edge_list):
    # Verifica che il cammino sia ammissibile, e quindi che non ci siano "salti"
    edge_list = process_raw_list_to_get_edge_list_with_directions(edge_list)

    ending = s
    for e in path:
        edge = edge_list[e]
        if edge[0] == ending:
            ending = edge[1]
        else:
            if edge[3] == 1:
                return False
            else:
                if edge[1] == ending:
                    ending = edge[0]
                else:
                    return False
    
    if ending == t: return True
    else: return False

def check_tree_connectivity(tree: list, edge_list: list, n: int, s: int) -> bool:
    # Verifica se l'albero è connesso tramite archi ammissibili

    edge_list = process_raw_list_to_get_edge_list(edge_list)
    for i in range(n):
        if i == s: continue
        if len([x for x in edge_list if x[0] == tree[i] and x[1] == i]) == 0:
            return False
    return True

def check_tree(tree: list, edge_list: list, n: int, s: int) -> bool:
    # Verifica che la lista in input sia effettivamente un albero e non una foresta

    if not any(v == s for v in tree): # il nodo radice è scollegato
        return False
    
    for i in range(n):
        if i == s: continue
        for j in range(n):
            if j == s: continue
            if i == j: continue
            if (tree[i] == j and tree[j] == i):
                return False

    edge_list = process_raw_list_to_get_edge_list(edge_list)

    _tree = nx.MultiGraph()
    _tree.add_nodes_from(list(range(n)))
    for i in range(1,n):
        if tree[i] == -1:
            return False
        else:
            _tree.add_edge(tree[i], i)

    return nx.is_tree(_tree)

def compute_length_from_tree(tree: list, edge_list: list, t: int) -> int:
    # Permette di calcolare il cammino minimo s -> t nell'albero tree
    # restituito come lista di archi da attraversare
    it = t
    length = 0

    while tree[it] != -1:
        e_ = [x for x in edge_list if x[0] == tree[it] and x[1] == it and x[2] == min(x[2] for x in edge_list if x[0] == tree[it] and x[1] == it)][0]
        length = length + e_[2]
        it = tree[it]

    return length

def compute_edge_seq_from_tree(tree: list, edge_list: list, condensed_edges: list, t: int) -> list:
    # Permette di calcolare il cammino s -> t nell'albero tree
    # restituito come lista di archi da attraversare
    it = t
    shortest_path = []

    while tree[it] != -1:
        e_ = [x for x in edge_list if x[0] == tree[it] and x[1] == it and x[2] == min(x[2] for x in edge_list if x[0] == tree[it] and x[1] == it)][0]
        if e_[3] == 1:
            e = condensed_edges.index((e_[1], e_[0], e_[2]))
        else:
            e = condensed_edges.index(e_[:-1])
        tmp = shortest_path.copy()
        shortest_path = [e]
        shortest_path.extend(tmp)
        it = tree[it]

    return shortest_path

def compute_edges_in_tree(tree: list, edge_list: list, condensed_edges: list, n: int) -> list:
    # Permette di calcolare quali archi sono coinvolti nella formazione dell'albero tree

    edge_in_tree = []

    for i in range(1,n):
        e_ = [x for x in edge_list if x[0] == tree[i] and x[1] == i and x[2] == min(x[2] for x in edge_list if x[0] == tree[i] and x[1] == i)][0]
        if e_[3] == 1:
            e = condensed_edges.index((e_[1], e_[0], e_[2]))
        else:
            e = condensed_edges.index(e_[:-1])
        edge_in_tree.append(e)
    
    return edge_in_tree

def check_instance_consistency(instance: dict) -> None:
    # Verifico che l'istanza immessa dal problem maker sia aderente a ciò che si è stabilito

    #print(f"Instance={instance}", file=stderr)

    if not check_instance_parameters_and_types(instance):
        print(f"Errore: l'istanza {instance} non presenta tutti i parametri richiesti per il problema selezionato, oppure sussiste incongruenza su almeno un tipo relativamente a quelli previsti.")
        exit(0)
    
    n = instance['n']
    m = instance['m']
    s = instance['s']
    t = instance['t']
    edges = instance['edges']
    query_edge = instance['query_edge']
    cap_num_sols = instance['CAP_FOR_NUM_SOLS']
    cap_num_opt_sols = instance['CAP_FOR_NUM_OPT_SOLS']

    if not check_raw_edge_list_consistency(edges):
        print(f"Errore: la lista di archi {edges} non soddisfa la struttura definita per il problema selezionato.")
        exit(0)

    raw_edge_list = ast.literal_eval(edges)
    # Ora so che la lista di archi passata in istanza ha la struttura corretta, quindi la posso processare
    edge_list = process_raw_list_to_get_edge_list(raw_edge_list)

    if n <= 0:
        print(f"Errore: il numero di nodi ('n'= {n}) è minore o uguale a 0.")
        exit(0)
    if m <= 0:
        print(f"Errore: il numero di archi ('m'= {m}) è minore o uguale a 0.")
        exit(0)
    if m != len(raw_edge_list):
        print(f"Errore: il numero di archi ('m'= {m}) differisce dalla lunghezza ({len(raw_edge_list)}) della lista 'edges'.")
        exit(0)
    if not 0 <= s < n:
        print(f"Errore: il nodo di origine {s} fuoriesce dall'intervallo ammesso [0,n) = [0,{n}).")
        exit(0)
    if not 0 <= t < n:
        print(f"Errore: il nodo di destinazione {t} fuoriesce dall'intervallo ammesso [0,n) = [0,{n}).")
        exit(0)
    for idx, (u, v, w, d) in enumerate(edge_list):
        if not 0 <= u < n:
            print(f"Errore: l'estremo {u} dell'arco {idx} fuoriesce dall'intervallo ammesso [0,n)=[0,{n}).")
            exit(0)
        if not 0 <= v < n:
            print(f"Errore: l'estremo {v} dell'arco {idx} fuoriesce dall'intervallo ammesso [0,n)=[0,{n}).")
            exit(0)
        if u == v:
            print(f"Errore: gli estremi dell'arco {u} - {v} sono uguali, ma il grafo non può contenere auto-loop.")
            exit(0)
        if w <= 0:
            print(f"Errore: l'arco {idx} ha lunghezza {w} minore o uguale a 0.")
            exit(0)
        # Per come costruisco la lista di archi i successivi due controlli non sono realmente necessari
        if d != 0 and d != 1:
            print(f"Errore: l'arco {idx} è di una tipologia non riconosciuta.")
            exit(0)
        if d == 1:
            if len([(e[0], e[1]) for e in edge_list if (e[0] == v and e[1] == u and e[2] == w and e[3] == 0)]) != 1:
                print(f"Errore: l'arco {idx} non diretto da {u} a {v} prevede l'esistenza di un arco corrispettivo univoco da {v} ad {u}, che tuttavia non è presente.")
                exit(0)
    if not 0 <= query_edge < m:
        print(f"Errore: il 'query_edge' ({query_edge}) fuoriesce dall'intervallo ammesso [0,m) = [0,{m}).")
        exit(0)
    if not check_connectivity(s, n, edge_list):
        print(f"Errore: ci sono nodi non raggiungibili a partire da s.")
        exit(0)
    if cap_num_sols > limits['CAP_FOR_NUM_SOLS']:
        print(f"Errore: non è consentito settare 'CAP_FOR_NUM_SOLS' a {cap_num_sols} > {limits['CAP_FOR_NUM_SOLS']}.")
        exit(0)
    if cap_num_opt_sols > limits['CAP_FOR_NUM_OPT_SOLS']:
        print(f"Errore: non è consentito settare 'CAP_FOR_NUM_OPT_SOLS' a {cap_num_opt_sols} > {limits['CAP_FOR_NUM_OPT_SOLS']}.")
        exit(0)

class Graph:
    # Classe per grafi pesati misti, con possibili archi anti-paralleli.

    n : int = 0
    s : int = 0
    t : int = 0
    edges : list[tuple] = []
    original_edges : list = []
    condensed_edges : list[tuple] = []
    shortest_path_tree : list[int] = []
    all_shortest_path_trees : list[list] = []
    shortest_path : list[int] = []
    all_shortest_paths : list[list] = []
    min_distances : list[int] = []
    min_distance : int = 0

    def __init__(self, vertices: int) -> None:
        self.n = vertices   # numero di vertici
        self.edges = []     # lista degli archi collassata (solo archi diretti) [(u, v, weight, collapsed), ...]
                            # collapsed = 1 se l'arco è frutto del collasso di un arco non diretto
        self.condensed_edges = []       # lista degli archi originale [(u, v, weight), ...]

    def add_edge(self, u: int, v: int, weight: int, collapsed: int) -> None:
        # Permette di aggiungere un arco al grafo

        self.edges.append((u, v, weight, collapsed))

    def add_edge_list(self, edge_list: list) -> None:
        # Permette di aggiungere più archi contemporaneamente

        for (u, v, w, c) in edge_list:
            self.add_edge(u, v, w, c)

        self.condensate_edge_list()

    def condensate_edge_list(self) -> None:
        # Permette di condensare la lista di archi in una in cui possono esistere archi non diretti

        tmp_condensed = self.edges.copy()
        edges_to_remove = [x for x in self.edges if x[3] == 1]

        for e in edges_to_remove:
            tmp_condensed.remove(e)

        self.condensed_edges = []
        for e in tmp_condensed:
            self.condensed_edges.append(e[:-1])

    def set_original_edges(self, original_edge_list: list):
        # Permette di salvare la lista originale di archi data in istanza
        self.original_edges = original_edge_list

    def set_starting_vertex(self, s: int) -> None:
        # Permette di impostare il nodo sorgente

        self.s = s

    def set_ending_vertex(self, t: int) -> None:
        # Permette di impostare il nodo di terminazione

        self.t = t

    def compute_path_from_tree(self, tree) -> list:
        # Permette di calcolare il cammino minimo s -> t nell'albero tree
        # restituito come lista di archi da attraversare
        it = self.t
        shortest_path = []

        while tree[it] != -1:
            e_ = [x for x in self.edges if x[0] == tree[it] and x[1] == it and x[2] == min(x[2] for x in self.edges if x[0] == tree[it] and x[1] == it)][0]
            if e_[3] == 1:
                e = self.condensed_edges.index((e_[1], e_[0], e_[2]))
            else:
                e = self.condensed_edges.index(e_[:-1])
            tmp = shortest_path.copy()
            shortest_path = [e]
            shortest_path.extend(tmp)
            it = tree[it]

        return shortest_path

    def indexes(self, list : list, x : int) -> list:
        # Permette di calcolare gli indici di tutte le occorenze di x in list
        tmp = 0
        start = 0
        indexes = []
        while tmp != -1:
            try:
                tmp = list.index(x,start)
                start = tmp + 1
                indexes.append(tmp)
            except:
                tmp = -1

        return indexes

    def get_min_dist_not_explored_vertex(self, distances, not_explored) -> int:
        # Permette di calcolare il nodo non ancora esplorato a distanza minima da s
        not_explored_dist = [distances[x] for x in not_explored]
        min_dist = min(not_explored_dist)
        idxs = self.indexes(distances, min_dist)

        for idx in idxs:
            if idx in not_explored: return idx

    def compute_dijkstra(self) -> None:
        # Calcola un albero dei cammini minimi, il percorso minimo tra s e t che compare
        # nell'albero e la distanza minima tra s e tutti gli altri nodi del grafo
        # if self.n == 0:
        #     print(f"Errore: grafo vuoto, non è possibile calcolare un albero di cammini minimi.")
        #     exit(0)
        # if len(self.edges) == 0:
        #     print(f"Errore: lista degli archi non inizializzata, non è possibile calcolare un albero di cammini minimi.")
        #     exit(0)

        shortest_path_tree = []

        # Calcolo un valore massimo per la distanza tra 2 nodi come m * maxlength + 1
        MAX = max([x[2] for x in self.edges]) * len(self.condensed_edges) + 1
        # Inizializzo p(v) per ogni vertice
        p = [MAX for _ in range(self.n)]
        p[self.s] = 0

        shortest_path_tree = [-1 for _ in range(self.n)]
        not_explored = list(range(self.n))

        while len(not_explored) != 0:
            min_dist_vertex = self.get_min_dist_not_explored_vertex(p, not_explored)
            suitable_edges = [x for x in self.edges if x[0] == min_dist_vertex and x[1] in not_explored]

            for (u, v, w, _) in suitable_edges:
                if p[v] > p[u] + w:
                    p[v] = p[u] + w
                    shortest_path_tree[v] = u

            not_explored.remove(min_dist_vertex)

        shortest_path = self.compute_path_from_tree(shortest_path_tree)

        self.shortest_path_tree = shortest_path_tree
        self.shortest_path = shortest_path
        self.min_distances = p
        self.min_distance = p[self.t]

    def get_shortest_path_tree(self) -> list:
        # Restituisce l'albero dei cammini minimi radicato in s precedentemente calcolato
        # come lista t in cui t[i] è il padre del nodo i nell'albero
        
        return self.shortest_path_tree

    def get_all_shortest_path_trees(self) -> list[list]:
        min_dists = self.min_distances
        min_dists_for_selection = min_dists.copy()
        MAX = max(min_dists_for_selection) + 1
        explored = []
        already_seen = []
        all_shortest_path_trees = [[-1 for _ in range(self.n)]]

        while len(explored) != self.n:
            s = min_dists_for_selection.index(min(min_dists_for_selection))
            min_dists_for_selection[s] = MAX
            explored.append(s)
            out_edges = [x for x in self.edges if x[0] == s and (min_dists[s] + x[2]) == min_dists[x[1]]]
            not_seen = [x[1] for x in out_edges if x[1] not in already_seen]
            seen = [x[1] for x in out_edges if x[1] in already_seen]
            for v in not_seen:
                already_seen.append(v)
                for tree in all_shortest_path_trees:
                    tree[v] = s
            for v in seen:
                for tree in all_shortest_path_trees.copy():
                    tmp_tree = tree.copy()
                    tmp_tree[v] = s
                    if tmp_tree not in all_shortest_path_trees: all_shortest_path_trees.append(tmp_tree)


        # seed_list = [self.shortest_path_tree]
        # not_explored = list(range(self.n))

        # seed_list, not_explored = self.compute_all_shortest_path_trees(seed_list, self.t, not_explored)
        
        # while len(not_explored) != 0:
        #     seed_list, not_explored = self.compute_all_shortest_path_trees(seed_list, not_explored[0], not_explored)

        self.all_shortest_path_trees = all_shortest_path_trees
        return self.all_shortest_path_trees

    def compute_all_shortest_path_trees(self, seed_list, t, not_explored) -> list[list]:
        if t != self.s and t in not_explored:
            if len(not_explored) != 0:
                not_explored.remove(t)
            min_dists = self.min_distances
            for tree in seed_list.copy():
                t_parent = tree[t]
                suitable_parents = [x[0] for x in self.edges if x[0] != t_parent and x[1] == t and (min_dists[x[0]] + x[2]) == min_dists[t]]
                for p in suitable_parents:
                    tmp_tree = tree.copy()
                    tmp_tree[t] = p
                    if tmp_tree not in seed_list: seed_list.append(tmp_tree)
                seed_list, not_explored = self.compute_all_shortest_path_trees(seed_list, t_parent, not_explored)

        return seed_list, not_explored
    
    def get_num_shortest_path_trees(self) -> int:
        # Ritorna il numero di alberi dei cammini minimi per il grafo in esame

        return len(self.all_shortest_path_trees)
    
    def get_shortest_path(self) -> list:
        # Restituisce il cammino minimo che da s conduce a t
        # come lista di archi da percorrere

        return self.shortest_path
    
    def get_all_shortest_paths(self) -> list[list]:
        # Restituisce la lista di tutti i cammini minimi che da s conducono a t
        # come lista di cammini minimi
        all_shortest_paths = []

        for tree in self.all_shortest_path_trees:
            tmp_shortest_path = self.compute_path_from_tree(tree)
            if tmp_shortest_path not in all_shortest_paths: all_shortest_paths.append(tmp_shortest_path)

        self.all_shortest_paths = all_shortest_paths
        return self.all_shortest_paths
    
    def get_num_shortest_paths(self) -> int:
        # Ritorna il numero di cammini minimi da s a t

        return len(self.all_shortest_paths)

    def get_shortest_path_length(self) -> int:
        # Ritorna la lunghezza del cammino minimo tra s e t

        return self.min_distance
    
    def get_all_shortest_path_lengths(self) -> list:
        # Ritorna la lista di tutte le distanze minime
        # come lista d in cui d[i] corrisponde alla distanza minima tra s e i

        return self.min_distances
    
    def compute_edge_profile(self, query_edge) -> str:
        # Ritorna "in_all" se il query edge è presente in tutti gli SPT, 
        # "in_no" se non è presente in nessuno, 
        # "in_some_but_not_in_all" se è presente in alcuni, ma ne esiste almeno uno in cui non è presente
        at_least_one = False
        at_least_one_not = False
        u, v, w = self.condensed_edges[query_edge]

        for tree in self.all_shortest_path_trees:
            if tree[v] == u or tree[u] == v:
                if at_least_one_not: return "in_some_but_not_in_all"
                if not at_least_one: at_least_one = True
            else:
                if at_least_one: return "in_some_but_not_in_all"
                if not at_least_one_not: at_least_one_not = True
        if at_least_one: return "in_all"
        else: return "in_no"

    def get_nodes_relying_on_query_edge(self, query_edge) -> list:
        tmp_graph = Graph(self.n)
        tmp_edges = self.original_edges.copy()
        tmp_edges.pop(query_edge)

        # se sto per rimuovere l'unico nodo del grafo, restituisco {v} \ s
        if len(tmp_edges) == 0:
            nodes_relying_on_query_edge = list(range(self.n))
            nodes_relying_on_query_edge.pop(self.s)
            return nodes_relying_on_query_edge
        
        tmp_graph.add_edge_list(process_raw_list_to_get_edge_list(tmp_edges))
        tmp_graph.set_starting_vertex(self.s)
        tmp_graph.set_ending_vertex(self.t)
        tmp_graph.compute_dijkstra()

        new_min_distances = tmp_graph.get_all_shortest_path_lengths()
        nodes_relying_on_query_edge = []
        for idx, i in enumerate(self.min_distances):
            if i != new_min_distances[idx]:
                nodes_relying_on_query_edge.append(idx)
        return nodes_relying_on_query_edge

def solver(input_to_oracle: dict) -> dict:
    instance = input_to_oracle['input_data_assigned']
    n = instance['n']
    m = instance['m']
    s = instance['s']
    t = instance['t']
    edges = instance['edges']
    query_edge = instance['query_edge']
    cap_num_sols = instance['CAP_FOR_NUM_SOLS']
    cap_num_opt_sols = instance['CAP_FOR_NUM_OPT_SOLS']

    edge_list = process_raw_list_to_get_edge_list(ast.literal_eval(edges))
    
    graph = Graph(n)
    graph.add_edge_list(edge_list)
    graph.set_original_edges(ast.literal_eval(edges))
    graph.set_starting_vertex(s)
    graph.set_ending_vertex(t)

    graph.compute_dijkstra()

    opt_tree = graph.get_shortest_path_tree()
    opt_path = graph.get_shortest_path()

    opt_dist = graph.get_shortest_path_length()
    opt_dists = graph.get_all_shortest_path_lengths()

    all_shortest_path_trees = graph.get_all_shortest_path_trees()
    all_shortest_paths = graph.get_all_shortest_paths()
    # riduciamo il numero di soluzioni da visualizzare
    list_opt_trees = all_shortest_path_trees[:cap_num_opt_sols]
    list_opt_paths = all_shortest_paths[:cap_num_opt_sols]

    num_opt_paths = graph.get_num_shortest_paths()
    num_opt_trees = graph.get_num_shortest_path_trees()

    edge_profile = graph.compute_edge_profile(query_edge)
    nodes_relying_on_query_edge = graph.get_nodes_relying_on_query_edge(query_edge)

    #print(f"input_to_oracle={input_to_oracle}", file=stderr)
    input_data = input_to_oracle["input_data_assigned"]
    #print(f"Requests={input_to_oracle['request']}")
    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    #print(f"oracle_answers={oracle_answers}", file=stderr)
    return oracle_answers

class verify_submission_problem_specific(verify_submission_gen):
    #Classe per la verifica delle soluzioni sottomesse dal problem solver.
    
    def __init__(self, sef, input_data_assigned: Dict, long_answer_dict: Dict, oracle_response: Dict = None):
        super().__init__(sef, input_data_assigned, long_answer_dict, oracle_response)
        self.graph = None

    def set_up_and_cash_handy_data(self):
        self.graph = Graph(self.I.n)
        self.graph.add_edge_list(process_raw_list_to_get_edge_list(ast.literal_eval(self.I.edges)))
        self.graph.set_original_edges(ast.literal_eval(self.I.edges))
        self.graph.set_starting_vertex(self.I.s)
        self.graph.set_ending_vertex(self.I.t)
        self.graph.compute_dijkstra()

    def verify_format(self, sef):
        #Verifica che il formato delle risposte sottomesse dal problem solver sia corretto.

        if not super().verify_format(sef):
            return False
        
        if 'opt_dist' in self.goals:
            opt_dist_g = self.goals['opt_dist']
            if type(opt_dist_g.answ) != int:
                return sef.format_NO(opt_dist_g, f"Come '{opt_dist_g.alias}' hai immesso '{opt_dist_g.answ}' dove era invece richiesto di immettere un intero.")
            sef.format_OK(opt_dist_g, f"Come '{opt_dist_g.alias}' hai immesso un valore intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")

        if 'opt_dists' in self.goals:
            opt_dists_g = self.goals['opt_dists']
            if type(opt_dists_g.answ) != list:
                return sef.format_NO(opt_dists_g, f"Come '{opt_dists_g.alias}' hai immesso '{opt_dists_g.answ}' dove era invece richiesto di immettere una lista di distanze opt_dists, dove opt_dists[u] = x se la minima distanza tra il nodo di partenza e il nodo u è pari ad x.")
            if any([type(value) != int for value in opt_dists_g.answ]):
                return sef.format_NO(opt_dists_g, f"Come '{opt_dists_g.alias}' hai immesso '{opt_dists_g.answ}' dove era invece richiesto di immettere una lista di distanze opt_dists, dove opt_dists[u] = x se la minima distanza tra il nodo di partenza e il nodo u è pari ad x. Ogni distanza deve essere rappresentata da un valore INTERO.")
            sef.format_OK(opt_dists_g, f"Come '{opt_dists_g.alias}' hai immesso una lista di distanze, come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")
        
        if 'opt_path' in self.goals:
            opt_path_g = self.goals['opt_path']
            if type(opt_path_g.answ) != list:
                return sef.format_NO(opt_path_g, f"Come '{opt_path_g.alias}' hai immesso '{opt_path_g.answ}' dove era invece richiesto di immettere una lista di archi. Una lista di archi è costituita da una lista di indici riferiti all'elenco degli archi nell'istanza del problema.")
            if any([type(value) != int for value in opt_path_g.answ]):
                return sef.format_NO(opt_path_g, f"Come '{opt_path_g.alias}' hai immesso '{opt_path_g.answ}' dove era invece richiesto di immettere una lista di archi. Una lista di archi è costituita da una lista di indici riferiti all'elenco degli archi nell'istanza del problema. Ogni indice deve essere rappresentato da un valore INTERO.")
            sef.format_OK(opt_path_g, f"Come '{opt_path_g.alias}' hai immesso una lista di archi, come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")
        
        if 'opt_tree' in self.goals:
            opt_tree_g = self.goals['opt_tree']
            if type(opt_tree_g.answ) != list:
                return sef.format_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso '{opt_tree_g.answ}' dove era invece richiesto di immettere una lista di nodi tree, dove tree[v] = u se nell'albero dei cammini minimi tree, il padre del nodo v è il nodo u.")
            if any([type(value) != int for value in opt_tree_g.answ]):
                return sef.format_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso '{opt_tree_g.answ}' dove era invece richiesto di immettere una lista di nodi tree, dove tree[v] = u se nell'albero dei cammini minimi tree, il padre del nodo v è il nodo u. Ogni nodo deve essere rappresentato da un valore INTERO.")
            sef.format_OK(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso una lista di nodi, come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")
        
        if 'num_opt_paths' in self.goals:
            num_opt_paths_g = self.goals['num_opt_paths']
            if type(num_opt_paths_g.answ) != int:
                return sef.format_NO(num_opt_paths_g, f"Come '{num_opt_paths_g.alias}' hai immesso '{num_opt_paths_g.answ}' dove era invece richiesto di immettere un intero.")
            sef.format_OK(num_opt_paths_g, f"Come '{num_opt_paths_g.alias}' hai immesso un valore intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")
        
        if 'num_opt_trees' in self.goals:
            num_opt_trees_g = self.goals['num_opt_trees']
            if type(num_opt_trees_g.answ) != int:
                return sef.format_NO(num_opt_trees_g, f"Come '{num_opt_trees_g.alias}' hai immesso '{num_opt_trees_g.answ}' dove era invece richiesto di immettere un intero.")
            sef.format_OK(num_opt_trees_g, f"Come '{num_opt_trees_g.alias}' hai immesso un valore intero come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")
        
        if 'list_opt_paths' in self.goals:
            list_opt_paths_g = self.goals['list_opt_paths']
            if type(list_opt_paths_g.answ) != list:
                return sef.format_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso '{list_opt_paths_g.answ}' dove era invece richiesto di immettere una lista di cammini. Un cammino è una lista di archi, che è a sua volta costituita da una lista di indici riferiti all'elenco degli archi nell'istanza del problema.")
            for path in list_opt_paths_g.answ:
                if type(path) != list:
                    return sef.format_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso '{list_opt_paths_g.answ}' dove era invece richiesto di immettere una lista di cammini. Un cammino è una lista di archi, che è a sua volta costituita da una lista di indici riferiti all'elenco degli archi nell'istanza del problema.")
                if any([type(value) != int for value in path]):
                    return sef.format_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso '{list_opt_paths_g.answ}' dove era invece richiesto di immettere una lista di cammini. Un cammino è una lista di archi, che è a sua volta costituita da una lista di indici riferiti all'elenco degli archi nell'istanza del problema. Ogni indice deve essere rappresentato da un valore INTERO.")
            sef.format_OK(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso una lista di cammini, come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")
        
        if 'list_opt_trees' in self.goals:
            list_opt_trees_g = self.goals['list_opt_trees']
            if type(list_opt_trees_g.answ) != list:
                return sef.format_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso '{list_opt_trees_g.answ}' dove era invece richiesto di immettere una lista di alberi. Un albero è una lista di nodi tree, dove tree[v] = u se nell'albero dei cammini minimi tree, il padre del nodo v è il nodo u.")
            for tree in list_opt_trees_g.answ:
                if type(tree) != list:
                    return sef.format_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso '{list_opt_trees_g.answ}' dove era invece richiesto di immettere una lista di alberi. Un albero è una lista di nodi tree, dove tree[v] = u se nell'albero dei cammini minimi tree, il padre del nodo v è il nodo u.")
                if any([type(value) != int for value in tree]):
                    return sef.format_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso '{list_opt_trees_g.answ}' dove era invece richiesto di immettere una lista di alberi. Un albero è una lista di nodi tree, dove tree[v] = u se nell'albero dei cammini minimi tree, il padre del nodo v è il nodo u. Ogni nodo deve essere rappresentato da un valore INTERO.")
            sef.format_OK(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso una lista di alberi, come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")
        
        if 'edge_profile' in self.goals:
            edge_profile_g = self.goals['edge_profile']
            if type(edge_profile_g.answ) != str:
                return sef.format_NO(edge_profile_g, f"Come '{edge_profile_g.alias}' hai immesso '{edge_profile_g.answ}' dove era invece richiesto di immettere una stringa.")
            if edge_profile_g.answ not in ['in_all', 'in_no', 'in_some_but_not_in_all']:
                return sef.format_NO(edge_profile_g, f"Come '{edge_profile_g.alias}' hai immesso '{edge_profile_g.answ}', che non compare tra le uniche risposte accettate: 'in_all', 'in_no', 'in_some_but_not_in_all'.")
            sef.format_OK(edge_profile_g, f"Come '{edge_profile_g.alias}' hai immesso una stringa valida come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")
        
        if 'nodes_relying_on_query_edge' in self.goals:
            nodes_relying_g = self.goals['nodes_relying_on_query_edge']
            if type(nodes_relying_g.answ) != list:
                return sef.format_NO(nodes_relying_g, f"Come '{nodes_relying_g.alias}' hai immesso '{nodes_relying_g.answ}' dove era invece richiesto di immettere una lista di nodi.")
            if any([type(value) != int for value in nodes_relying_g.answ]):
                return sef.format_NO(nodes_relying_g, f"Come '{nodes_relying_g.alias}' hai immesso '{nodes_relying_g.answ}' dove era invece richiesto di immettere una lista di nodi. Ogni nodo deve essere rappresentato da un valore INTERO.")
            sef.format_OK(nodes_relying_g, f"Come '{nodes_relying_g.alias}' hai immesso una lista di nodi, come richiesto.", f"Ovviamente durante lo svolgimento dell'esame non è dato sapere se il valore immesso sia quello corretto, ma il formato è conforme a quanto atteso.")

        return True

    def verify_feasibility(self, sef):
        #Verifica che le risposte che il problem solver ha inserito siano ammissibili rispetto all'istanza del problema.

        if not super().verify_feasibility(sef):
            return False

        n = self.I.n
        m = self.I.m
        s = self.I.s
        t = self.I.t
        edges = ast.literal_eval(self.I.edges)

        if 'opt_dist' in self.goals:
            opt_dist_g = self.goals['opt_dist']
            if opt_dist_g.answ < 0:
                return sef.feasibility_NO(opt_dist_g, f"Come '{opt_dist_g.alias}' hai immesso {opt_dist_g.answ}, ma il valore ottimo non può essere minore di 0.")
            sef.feasibility_OK(opt_dist_g, f"Come '{opt_dist_g.alias}' hai immesso un valore di lunghezza valido.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        if 'opt_dists' in self.goals:
            opt_dists_g = self.goals['opt_dists']
            if len(opt_dists_g.answ) != n:
                return sef.feasibility_NO(opt_dists_g, f"Come '{opt_dists_g.alias}' hai immesso {opt_dists_g.answ} di lunghezza {len(opt_dists_g.answ)}, ma il numero di nodi nel grafo è {n}.")
            if any(d < 0 for d in opt_dists_g.answ):
                return sef.feasibility_NO(opt_dists_g, f"Come '{opt_dists_g.alias}' hai immesso {opt_dists_g.answ}, ma il valore ottimo non può essere minore di 0.")
            if opt_dists_g.answ[s] != 0:
                return sef.feasibility_NO(opt_dists_g, f"Come '{opt_dists_g.alias}' hai immesso {opt_dists_g.answ}, ma la distanza del nodo di origine {s} non può essere diversa da 0.")
            sef.feasibility_OK(opt_dists_g, f"Come '{opt_dists_g.alias}' hai immesso una lista di lunghezze valida.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        if 'opt_path' in self.goals:
            opt_path_g = self.goals['opt_path']
            if not all(0 <= e < m for e in opt_path_g.answ):
                return sef.feasibility_NO(opt_path_g, f"Come '{opt_path_g.alias}' hai immesso {opt_path_g.answ}, ma al suo interno sono presenti indici di archi inesistenti.")
            if len(opt_path_g.answ) != len(set(opt_path_g.answ)):
                return sef.feasibility_NO(opt_path_g, f"Come '{opt_path_g.alias}' hai immesso {opt_path_g.answ}, ma al suo interno sono presenti degli indici ripetuti.")
            if not check_path(s, t, opt_path_g.answ, edges):
                return sef.feasibility_NO(opt_path_g, f"Come '{opt_path_g.alias}' hai immesso {opt_path_g.answ}, che non è un percorso ammesso dal nodo {s} al nodo {t}.")
            sef.feasibility_OK(opt_path_g, f"Come '{opt_path_g.alias}' hai immesso un cammino valido.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")
       
        if 'opt_tree' in self.goals:
            opt_tree_g = self.goals['opt_tree']
            if not all(-1 <= v < n for v in opt_tree_g.answ):
                return sef.feasibility_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso {opt_tree_g.answ}, ma al suo interno sono presenti indici di nodi inesistenti.")
            if len(opt_tree_g.answ) != n:
                return sef.feasibility_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso {opt_tree_g.answ} che contiene {len(opt_tree_g.answ)} elementi, ma il grafo è composto da {n} nodi.")
            if len([x for x in opt_tree_g.answ if x == -1]) != 1:
                return sef.feasibility_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso {opt_tree_g.answ}, ma al suo interno è presente un numero errato di nodi di origine, contrassegnati dal valore -1.")
            if opt_tree_g.answ.index(-1) != s:
                return sef.feasibility_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso {opt_tree_g.answ}, ma al suo interno risulta esserci una radice diversa da quella attesa.")
            if not check_tree_connectivity(opt_tree_g.answ, edges, n, s):
                return sef.feasibility_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso {opt_tree_g.answ}, ma una delle relazioni padre - figlio non risulta valida (Non esiste un arco che la produca).")
            if not check_tree(opt_tree_g.answ, edges, n, s):
                return sef.feasibility_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso {opt_tree_g.answ}, ma questo non risulta essere un albero valido.")
            sef.feasibility_OK(opt_tree_g, f"Come '{opt_tree_g.alias}' hai immesso un albero valido.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")
         
        if 'num_opt_paths' in self.goals:
            num_opt_paths_g = self.goals['num_opt_paths']
            if num_opt_paths_g.answ < 0:
                return sef.feasibility_NO(num_opt_paths_g, f"Come '{num_opt_paths_g.alias}' hai immesso {num_opt_paths_g.answ}, ma il valore non può essere minore di 0.")
            sef.feasibility_OK(num_opt_paths_g, f"Come '{num_opt_paths_g.alias}' hai immesso un valore valido per il numero di soluzioni.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")
    
        if 'num_opt_trees' in self.goals:
            num_opt_trees_g = self.goals['num_opt_trees']
            if num_opt_trees_g.answ < 0:
                return sef.feasibility_NO(num_opt_trees_g, f"Come '{num_opt_trees_g.alias}' hai immesso {num_opt_trees_g.answ}, ma il valore non può essere minore di 0.")
            sef.feasibility_OK(num_opt_trees_g, f"Come '{num_opt_trees_g.alias}' hai immesso un valore valido per il numero di soluzioni.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        if 'list_opt_paths' in self.goals:
            list_opt_paths_g = self.goals['list_opt_paths']
            if len(list_opt_paths_g.answ) == 0:
                return sef.feasibility_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso {list_opt_paths_g.answ}, ma una lista vuota non è ammissibile.")
            for answ in list_opt_paths_g.answ:
                if not all(0 <= e < m for e in answ):
                    return sef.feasibility_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso {list_opt_paths_g.answ}, ma in almeno un cammino sono presenti indici di archi inesistenti.")
                if len(answ) != len(set(answ)):
                    return sef.feasibility_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso {list_opt_paths_g.answ}, ma in almeno un cammino sono presenti degli indici ripetuti.")
                if not check_path(s, t, answ, edges):
                    return sef.feasibility_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso {list_opt_paths_g.answ}, ma in almeno un cammino è contenuto un percorso non ammesso dal nodo {s} al nodo {t}.")
            if len(list_opt_paths_g.answ) != self.I.CAP_FOR_NUM_SOLS and self.graph.get_num_shortest_paths() >= self.I.CAP_FOR_NUM_SOLS:
                return sef.feasibility_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso {list_opt_paths_g.answ}, ma il numero di cammini presenti all'interno è diverso da quello limite prestabilito.")
            sef.feasibility_OK(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' hai immesso una lista di cammini valida.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")
        
        if 'list_opt_trees' in self.goals:
            list_opt_trees_g = self.goals['list_opt_trees']
            if len(list_opt_trees_g.answ) == 0:
                return sef.feasibility_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso {list_opt_trees_g.answ}, ma una lista vuota non è ammissibile.")
            for answ in list_opt_trees_g.answ:
                if not all(-1 <= v < n for v in answ):
                    return sef.feasibility_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso {list_opt_trees_g.answ}, ma in almeno un albero sono presenti indici di nodi inesistenti.")
                if len(answ) != n:
                    return sef.feasibility_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso {list_opt_trees_g.answ}, ma in almeno un albero non sono indicati tutti e soli i nodi genitori.")
                if len([x for x in answ if x == -1]) != 1:
                    return sef.feasibility_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso {list_opt_trees_g.answ}, ma in almeno un albero è presente un numero errato di nodi di origine, contrassegnati dal valore -1.")
                if answ.index(-1) != s:
                    return sef.feasibility_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso {list_opt_trees_g.answ}, ma in almeno un albero risulta esserci una radice diversa da quella attesa.")
                if not check_tree_connectivity(answ, edges, n, s):
                    return sef.feasibility_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso {list_opt_trees_g.answ}, ma in almeno un albero una delle relazioni padre - figlio non risulta valida (Non esiste un arco che la produca).")
                if not check_tree(answ, edges, n, s):
                    return sef.feasibility_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso {list_opt_trees_g.answ}, ma almeno un albero non risulta essere valido.")
            if len(list_opt_trees_g.answ) != self.I.CAP_FOR_NUM_SOLS and self.graph.get_num_shortest_path_trees() >= self.I.CAP_FOR_NUM_SOLS:
                return sef.feasibility_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso {list_opt_trees_g.answ}, ma il numero di alberi presenti all'interno è diverso da quello limite prestabilito.")
            sef.feasibility_OK(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' hai immesso una lista di alberi valida.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")
               
        if 'nodes_relying_on_query_edge' in self.goals:
            nodes_relying_g = self.goals['nodes_relying_on_query_edge']
            if len(nodes_relying_g.answ) != 0:
                if not all(0 <= v < n for v in nodes_relying_g.answ):
                    return sef.feasibility_NO(nodes_relying_g, f"Come '{nodes_relying_g.alias}' hai immesso {nodes_relying_g.answ}, ma al suo interno sono presenti indici di nodi inesistenti.")
                if len(nodes_relying_g.answ) != len(set(nodes_relying_g.answ)):
                    return sef.feasibility_NO(nodes_relying_g, f"Come '{nodes_relying_g.alias}' hai immesso {nodes_relying_g.answ}, ma al suo interno sono presenti dei nodi ripetuti.")
            sef.feasibility_OK(nodes_relying_g, f"Come '{nodes_relying_g.alias}' hai immesso una lista di nodi valida.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        return True

    def verify_consistency(self, sef):

        #Verifica che le risposte inserite dall'utente siano consistenti tra di loro.

        if not super().verify_consistency(sef):
            return False

        n = self.I.n
        m = self.I.m
        s = self.I.s
        t = self.I.t
        cap_for_num_sols = self.I.CAP_FOR_NUM_SOLS
        query_edge = self.I.query_edge
        edges = ast.literal_eval(self.I.edges)
        edge_list = process_raw_list_to_get_edge_list_with_directions(edges) # qui esistono anche archi non diretti, sono gli archi di partenza
        edge_list_only_directed = process_raw_list_to_get_edge_list(edges)
        condensed_edge_list = process_raw_list_to_get_condensed_edge_list(edges)

        if 'opt_dist' in self.goals:
            opt_dist_g = self.goals['opt_dist']

            # il cammino minimo (o i cammini minimi) tra s e t devono avere lunghezza pari alla distanza minima segnalata
            if 'opt_path' in self.goals:
                opt_path_g = self.goals['opt_path']
                if (tot := sum([edge_list[x][2] for x in opt_path_g.answ])) != opt_dist_g.answ:
                    return sef.consistency_NO(['opt_dist', 'opt_path'], f"La somma dei pesi degli archi in '{opt_path_g.alias}' è {tot}, che è diverso dal valore immesso in '{opt_dist_g.alias}' ({opt_dist_g.answ}).")
                sef.consistency_OK(['opt_path', 'opt_dist'], f"La lunghezza totale di '{opt_path_g.alias}' è effettivamente {tot}, come immesso in '{opt_dist_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")
            if 'list_opt_paths' in self.goals:
                list_opt_path_g = self.goals['list_opt_paths']
                for path in list_opt_path_g.answ:
                    if (tot := sum([edge_list[x][2] for x in path])) != opt_dist_g.answ:
                        return sef.consistency_NO(['opt_dist', 'list_opt_paths'], f"In uno dei cammini in '{list_opt_path_g.alias}' la somma dei pesi degli archi è {tot}, che è diverso dal valore immesso in '{opt_dist_g.alias}' ({opt_dist_g.answ}).")
                sef.consistency_OK(['list_opt_paths', 'opt_dist'], f"Il peso di tutti i cammini in '{list_opt_path_g.alias}' è effettivamente {tot}, come immesso in '{opt_dist_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

            # l'albero dei cammini minimi (o gli alberi dei cammini minimi) devono essere tali da presentare la stessa distanza minima segnalata
            if 'opt_tree' in self.goals:
                opt_tree_g = self.goals['opt_tree']
                if (tot := compute_length_from_tree(opt_tree_g.answ,edge_list_only_directed,t)) != opt_dist_g.answ:
                    return sef.consistency_NO(['opt_dist', 'opt_tree'], f"La somma dei pesi degli archi del cammino dal nodo {s} al nodo {t} in '{opt_tree_g.alias}' è {tot}, che è diverso dal valore immesso in '{opt_dist_g.alias}' ({opt_dist_g.answ}).")
                sef.consistency_OK(['opt_tree', 'opt_dist'], f"La lunghezza totale del cammino dal nodo {s} al nodo {t} in '{opt_tree_g.alias}' è effettivamente {tot}, come immesso in '{opt_dist_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")
            if 'list_opt_trees' in self.goals:
                list_opt_trees_g = self.goals['list_opt_trees']
                for tree in list_opt_trees_g.answ:
                    if (tot := compute_length_from_tree(tree,edge_list_only_directed,t)) != opt_dist_g.answ:
                        return sef.consistency_NO(['opt_dist', 'list_opt_trees'], f"In uno degli alberi in '{list_opt_trees_g.alias}' la lunghezza del cammino dal nodo {s} al nodo {t} è {tot}, che è diverso dal valore immesso in '{opt_dist_g.alias}' ({opt_dist_g.answ}).")
                sef.consistency_OK(['list_opt_trees', 'opt_dist'], f"La lunghezza di tutti i cammini dal nodo {s} al nodo {t} in '{list_opt_trees_g.alias}' è effettivamente {tot}, come immesso in '{opt_dist_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

            # se entrambe specificate, la distanza minima deve corrispondere nella lista delle distanze minime
            if 'opt_dists' in self.goals:
                opt_dists_g = self.goals['opt_dists']
                if opt_dists_g.answ[t] != opt_dist_g.answ:
                    return sef.consistency_NO(['opt_dist', 'opt_dists'], f"Nella lista di distanze '{opt_dists_g.alias}' la distanza del nodo {t} dal nodo {s} è pari a {opt_dists_g.answ[t]}, che è diverso dal valore immesso in '{opt_dist_g.alias}' ({opt_dist_g.answ}).")
                sef.consistency_OK(['opt_dists', 'opt_dist'], f"La distanza dal nodo {s} al nodo {t} immessa in '{opt_dists_g.alias}' corrisponde a quella immessa in '{opt_dist_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        # controllo che le distanze indicate in opt_dists corrispondano a quelle ricavate dall'albero opt_tree
        if 'opt_tree' in self.goals and 'opt_dists' in self.goals:
            opt_tree_g = self.goals['opt_tree']
            opt_dists_g = self.goals['opt_dists']
            for i in range(n):
                if i != s:
                    path_to_i_length = compute_length_from_tree(opt_tree_g.answ, edge_list_only_directed, i)
                    if path_to_i_length != opt_dists_g.answ[i]:
                        return sef.consistency_NO(['opt_tree', 'opt_dists'], f"L'albero inserito in '{opt_tree_g.alias}' presenta un cammino dal nodo {s} al nodo {i} che non corrisponde in lunghezza alla distanza specificata in '{opt_dists_g.alias}'.")
            sef.consistency_OK(['opt_tree', 'opt_dists'], f"Tutte i cammini in '{opt_tree_g.alias}' presentano la medesima lunghezza immessa in '{opt_dists_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")


        # controllo che non ci siano alberi ripetuti e che le distanze dal nodo s di tutti i nodi del grafo siano mantenute di albero in albero
        if 'list_opt_trees' in self.goals:
            list_opt_trees_g = self.goals['list_opt_trees']
            opt_trees_seen = []
            for tree in list_opt_trees_g.answ:
                if tree in opt_trees_seen:
                    return sef.consistency_NO(['list_opt_trees'], f"All'interno di '{list_opt_trees_g.alias}' sono presenti delle soluzioni ripetute, pertanto la lista delle soluzioni non è valida.")
                else:
                    opt_trees_seen.append(tree)
            for i in range(n):
                if i != s:
                    path_to_i_lengths = [compute_length_from_tree(tree, edge_list_only_directed, i) for tree in list_opt_trees_g.answ]
                    if len(set(path_to_i_lengths)) != 1:
                        return sef.consistency_NO(['list_opt_trees'], f"Uno stesso cammino non conserva sempre la medesima lunghezza in '{list_opt_trees_g.alias}', pertanto la lista delle soluzioni non è valida.")
                    if 'opt_dists' in self.goals:
                        opt_dists_g = self.goals['opt_dists']
                        if path_to_i_lengths[0] != opt_dists_g.answ[i]:
                            return sef.consistency_NO(['list_opt_trees', 'opt_dists'], f"Uno degli alberi in '{list_opt_trees_g.alias}' presenta un cammino dal nodo {s} al nodo {i} che non corrisponde in lunghezza alla distanza specificata in '{opt_dists_g.alias}', pertanto la lista delle soluzioni non è valida.")
            sef.consistency_OK(['list_opt_trees'], f"Tutte i possibili cammini conservano la medesima lunghezza in ogni albero in '{list_opt_trees_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")
        
        # controllo che non ci siano cammini ripetuti e che le lunghezze siano sempre uguali
        if 'list_opt_paths' in self.goals:
            list_opt_path_g = self.goals['list_opt_paths']
            opt_paths_seen = []
            for path in list_opt_path_g.answ:
                if path in opt_paths_seen:
                    return sef.consistency_NO(['list_opt_paths'], f"All'interno di '{list_opt_path_g.alias}' sono presenti delle soluzioni ripetute, pertanto la lista delle soluzioni non è valida.")
                else:
                    opt_paths_seen.append(path)
            all_lengths = [sum([edge_list[x][2] for x in path]) for path in list_opt_path_g.answ]    
            if len(set(all_lengths)) != 1:
                return sef.consistency_NO(['list_opt_paths'], f"Non tutti i cammini in '{list_opt_path_g.alias}' conservano la stessa lunghezza, pertanto la lista delle soluzioni non è valida.")
            sef.consistency_OK(['list_opt_paths'], f"Tutti i cammini in '{list_opt_path_g.alias}' hanno la stessa lunghezza.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        # controllo che per ogni cammino inserito, ci sia una corrispondenza in almeno un albero
        # if 'list_opt_paths' in self.goals and 'list_opt_trees' in self.goals:
        #     list_opt_path_g = self.goals['list_opt_paths']
        #     list_opt_trees_g = self.goals['list_opt_trees']

        #     opt_paths_seen = []
        #     for tree in list_opt_trees_g.answ:
        #         path = compute_edge_seq_from_tree(tree, edge_list_only_directed,condensed_edge_list,t)
        #         if path in list_opt_path_g.answ and path not in opt_paths_seen:
        #             opt_paths_seen.append(path)
        #     if len(opt_paths_seen) != len(list_opt_path_g.answ):
        #         return sef.consistency_NO(['list_opt_paths', 'list_opt_trees'], f"Non tutti i cammini in '{list_opt_path_g.alias}' sono contenuti in un albero che compare in '{list_opt_trees_g.alias}', pertanto la lista delle soluzioni non è valida.")
        #     sef.consistency_OK(['list_opt_paths', 'list_opt_trees'], f"Tutti i cammini in '{list_opt_path_g.alias}' hanno un albero che li contenga in '{list_opt_trees_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        # controllo che l'edge profile sia compatibile con alberi, cammini e nodes_relying_on_query_edge
        if 'edge_profile' in self.goals:
            edge_profile_g = self.goals['edge_profile']

            trees = []
            g_list = ['edge_profile']
            if 'list_opt_trees' in self.goals:
                list_opt_trees_g = self.goals['list_opt_trees']
                trees = list_opt_trees_g.answ
                g_list.append('list_opt_trees')
            if 'opt_tree' in self.goals:
                opt_tree_g = self.goals['opt_tree']
                if opt_tree_g.answ not in trees:
                    trees.append(opt_tree_g.answ)
                g_list.append('opt_tree')

            for tree in trees:
                path = compute_edges_in_tree(tree, edge_list_only_directed,condensed_edge_list,n)
                if query_edge not in path:
                    if edge_profile_g.answ == 'in_all':
                        return sef.consistency_NO(g_list, f"In '{edge_profile_g.alias}' hai inserito '{edge_profile_g.answ}', ma almeno uno degli alberi immessi non contiene il query edge, pertanto la lista delle soluzioni non è valida.")
                else:
                    if edge_profile_g.answ == 'in_no':
                        return sef.consistency_NO(g_list, f"In '{edge_profile_g.alias}' hai inserito '{edge_profile_g.answ}', ma almeno uno degli alberi immessi contiene il query edge, pertanto la lista delle soluzioni non è valida.")
            sef.consistency_OK(g_list, f"In '{edge_profile_g.alias}' hai inserito una soluzione compatibile con gli alberi immessi.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

            if 'nodes_relying_on_query_edge' in self.goals:
                nodes_relying_on_query_edge_g = self.goals['nodes_relying_on_query_edge']

                if edge_profile_g.answ == 'in_no' and len(nodes_relying_on_query_edge_g.answ) != 0:
                    return sef.consistency_NO(['edge_profile', 'nodes_relying_on_query_edge'], f"In '{edge_profile_g.alias}' hai inserito '{edge_profile_g.answ}', ma la lista di nodi che dipendono dal nodo di query non è vuota, pertanto la soluzione non è valida.")
                sef.consistency_OK(['edge_profile', 'nodes_relying_on_query_edge'], f"In '{edge_profile_g.alias}' hai inserito una soluzione compatibile con la lista di nodi immessa per '{nodes_relying_on_query_edge_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        # verifica che list_opt_paths contenga lo stesso numero di soluzioni dichiarate in num_opt_paths
        if 'list_opt_paths' in self.goals and 'num_opt_paths' in self.goals:
            list_opt_paths_g = self.goals['list_opt_paths']
            num_opt_paths_g = self.goals['num_opt_paths']
            if num_opt_paths_g.answ <= cap_for_num_sols:
                if num_opt_paths_g.answ != len(list_opt_paths_g.answ):
                    return sef.consistency_NO(['list_opt_paths', 'num_opt_paths'], f"Come '{list_opt_paths_g.alias}' hai inserito '{list_opt_paths_g.answ}', ma essa presenta un numero di soluzioni diverso dal valore '{num_opt_paths_g.alias}' immesso, {num_opt_paths_g.answ}.")
                sef.consistency_OK(['list_opt_paths', 'num_opt_paths'], f"Il numero di soluzioni in '{list_opt_paths_g.alias}' corrisponde al valore {num_opt_paths_g.answ} inserito in '{num_opt_paths_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        # verifica che list_opt_trees contenga lo stesso numero di soluzioni dichiarate in num_opt_trees
        if 'list_opt_trees' in self.goals and 'num_opt_trees' in self.goals:
            list_opt_trees_g = self.goals['list_opt_trees']
            num_opt_trees_g = self.goals['num_opt_trees']
            if num_opt_trees_g.answ <= cap_for_num_sols:
                if num_opt_trees_g.answ != len(list_opt_trees_g.answ):
                    return sef.consistency_NO(['list_opt_trees', 'num_opt_trees'], f"Come '{list_opt_trees_g.alias}' hai inserito '{list_opt_trees_g.answ}', ma essa presenta un numero di soluzioni diverso dal valore '{num_opt_trees_g.alias}' immesso, {num_opt_trees_g.answ}.")
                sef.consistency_OK(['list_opt_trees', 'num_opt_trees'], f"Il numero di soluzioni in '{list_opt_trees_g.alias}' corrisponde al valore {num_opt_trees_g.answ} inserito in '{num_opt_trees_g.alias}'.", f"Tuttavia, in sede di esame non è dato sapere se il valore inserito sia quello ottimo.")

        return True

    def verify_optimality(self, sef):

        #Verifica che le risposte inserite dell'utente siano quelle corrette

        if not super().verify_optimality(sef):
            return False

        s = self.I.s
        t = self.I.t
        query_edge = self.I.query_edge

        # verifica che opt_dist sia effettivamente la distanza minima 
        if 'opt_dist' in self.goals:
            opt_dist_g = self.goals['opt_dist']
            #true_answ = sef.oracle_dict['opt_dist']
            true_answ = self.graph.get_shortest_path_length()
            if opt_dist_g.answ != true_answ:
                return sef.optimality_NO(opt_dist_g, f"Come '{opt_dist_g.alias}' ha inserito '{opt_dist_g.answ}', tuttavia esso non è la distanza minima tra il nodo {s} e il nodo {t} (che in realtà è {true_answ}), pertanto il valore non è ottimo.")
            sef.optimality_OK(opt_dist_g, f"'{opt_dist_g.alias}'={true_answ} è effettivamente il valore ottimo.", f"")

        # verifica che opt_dists sia effettivamente la lista di distanze minime 
        if 'opt_dists' in self.goals:
            opt_dists_g = self.goals['opt_dists']
            #true_answ = sef.oracle_dict['opt_dists']
            true_answ = self.graph.get_all_shortest_path_lengths()
            for idx, i in enumerate(opt_dists_g.answ):
                if i != true_answ[idx]:
                    return sef.optimality_NO(opt_dists_g, f"Come '{opt_dists_g.alias}' ha inserito '{opt_dists_g.answ}', tuttavia esso non contiene le distanze minime dal nodo {s}, pertanto il valore non è ottimo.")
            sef.optimality_OK(opt_dists_g, f"'{opt_dists_g.alias}'={true_answ} è effettivamente il risultato ottimo.", f"")

        list_true_paths_trees = self.graph.get_all_shortest_path_trees()
        list_true_paths = self.graph.get_all_shortest_paths()

        # verifico che opt_path sia effettivamente uno dei cammini minimi
        if 'opt_path' in self.goals:
            opt_path_g = self.goals['opt_path']
            if opt_path_g.answ not in list_true_paths:
                return sef.optimality_NO(opt_path_g, f"Come '{opt_path_g.alias}' ha inserito '{opt_path_g.answ}', tuttavia esso non è uno dei cammini minimi dal nodo {s} al nodo {t}, pertanto la soluzione non è ottima.")
            sef.optimality_OK(opt_path_g, f"'{opt_path_g.alias}'={opt_path_g.answ} è effettivamente un risultato ottimo.", f"")

        # verifico che opt_tree sia effettivamente un albero dei cammini minimi
        if 'opt_tree' in self.goals:
            opt_tree_g = self.goals['opt_tree']
            if opt_tree_g.answ not in list_true_paths_trees:
                return sef.optimality_NO(opt_tree_g, f"Come '{opt_tree_g.alias}' ha inserito '{opt_tree_g.answ}', tuttavia esso non è uno degli alberi dei cammini minimi con radice nel nodo {s}, pertanto la soluzione non è ottima.")
            sef.optimality_OK(opt_tree_g, f"'{opt_tree_g.alias}'={opt_tree_g.answ} è effettivamente un risultato ottimo.", f"")

        # verifico che num_opt_paths sia effettivamente il numero di cammini minimi differenti
        if 'num_opt_paths' in self.goals:
            num_opt_paths_g = self.goals['num_opt_paths']
            true_answ = self.graph.get_num_shortest_paths()
            if num_opt_paths_g.answ != true_answ:
                return sef.optimality_NO(num_opt_paths_g, f"Come '{num_opt_paths_g.alias}' ha inserito '{num_opt_paths_g.answ}', tuttavia esso non è l'esatto numero di cammini minimi dal nodo {s} al nodo {t}, pertanto il valore non è ottimo.")
            sef.optimality_OK(num_opt_paths_g, f"'{num_opt_paths_g.alias}'={num_opt_paths_g.answ} è effettivamente il risultato ottimo.", f"")

        # verifico che num_opt_trees sia effettivamente il numero di alberi dei cammini minimi differenti
        if 'num_opt_trees' in self.goals:
            num_opt_trees_g = self.goals['num_opt_trees']
            true_answ = self.graph.get_num_shortest_path_trees()
            if num_opt_trees_g.answ != true_answ:
                return sef.optimality_NO(num_opt_trees_g, f"Come '{num_opt_trees_g.alias}' ha inserito '{num_opt_trees_g.answ}', tuttavia esso non è l'esatto numero di alberi dei cammini minimi con radice nel nodo {s}, pertanto il valore non è ottimo.")
            sef.optimality_OK(num_opt_trees_g, f"'{num_opt_trees_g.alias}'={num_opt_trees_g.answ} è effettivamente il risultato ottimo.", f"")

        # verifico che list_opt_paths contenga effettivamente tutti cammini minimi
        if 'list_opt_paths' in self.goals:
            list_opt_paths_g = self.goals['list_opt_paths']
            if len(list_opt_paths_g.answ) != self.graph.get_num_shortest_paths() and self.graph.get_num_shortest_paths() <= self.I.CAP_FOR_NUM_SOLS:
                return sef.optimality_NO(list_opt_paths_g, f"In '{list_opt_paths_g.alias}' hai inserito un numero di soluzioni pari a {len(list_opt_paths_g.answ)}, ma esse non sono tutte e sole le soluzioni ottime.")
            for path in list_opt_paths_g.answ:
                if path not in list_true_paths:
                    return sef.optimality_NO(list_opt_paths_g, f"Come '{list_opt_paths_g.alias}' ha inserito '{list_opt_paths_g.answ}', tuttavia uno dei percorsi immessi non è un cammino minimo dal nodo {s} al nodo {t}, pertanto la soluzione non è ottima.")
            sef.optimality_OK(list_opt_paths_g, f"'{list_opt_paths_g.alias}'={list_opt_paths_g.answ} è effettivamente un insieme di risultati ottimi.", f"")

        # verifico che list_opt_trees contenga effettivamente tutti cammini minimi
        if 'list_opt_trees' in self.goals:
            list_opt_trees_g = self.goals['list_opt_trees']
            if len(list_opt_trees_g.answ) != self.graph.get_num_shortest_path_trees() and self.graph.get_num_shortest_path_trees() <= self.I.CAP_FOR_NUM_SOLS:
                return sef.optimality_NO(list_opt_trees_g, f"In '{list_opt_trees_g.alias}' hai inserito un numero di soluzioni pari a {len(list_opt_trees_g.answ)},  ma esse non sono tutte e sole le soluzioni ottime.")
            for tree in list_opt_trees_g.answ:
                if tree not in list_true_paths_trees:
                    return sef.optimality_NO(list_opt_trees_g, f"Come '{list_opt_trees_g.alias}' ha inserito '{list_opt_trees_g.answ}', tuttavia uno degli alberi immessi non è un albero dei cammini minimi con radice nel nodo {s}, pertanto la soluzione non è ottima.")
            sef.optimality_OK(list_opt_trees_g, f"'{list_opt_trees_g.alias}'={list_opt_trees_g.answ} è effettivamente un insieme di risultati ottimi.", f"")

        # verifico che edge_profile sia effettivamente il risultato corretto per il query edge
        if 'edge_profile' in self.goals:
            edge_profile_g = self.goals['edge_profile']
            true_answ = self.graph.compute_edge_profile(query_edge)
            if edge_profile_g.answ != true_answ:
                return sef.optimality_NO(edge_profile_g, f"Come '{edge_profile_g.alias}' ha inserito '{edge_profile_g.answ}', tuttavia esso non è l'edge profile per il query edge {query_edge}, pertanto la soluzione non è ottima.")
            sef.optimality_OK(edge_profile_g, f"'{edge_profile_g.alias}'={edge_profile_g.answ} è effettivamente la soluzione ottima.", f"")

        # verifico che nodes_relying_on_query_edge sia effettivamente l'insieme di nodi che dipendono dal query edge
        if 'nodes_relying_on_query_edge' in self.goals:
            nodes_relying_on_query_edge_g = self.goals['nodes_relying_on_query_edge']
            true_answ = self.graph.get_nodes_relying_on_query_edge(query_edge)
            if len(true_answ) != len(nodes_relying_on_query_edge_g.answ):
                return sef.optimality_NO(nodes_relying_on_query_edge_g, f"Come '{nodes_relying_on_query_edge_g.alias}' ha inserito '{nodes_relying_on_query_edge_g.answ}', tuttavia esso non contiene tutti i nodi che dipendono dal query edge, pertanto la soluzione non è ottima.")
            for node in nodes_relying_on_query_edge_g.answ:
                if node not in true_answ:
                    return sef.optimality_NO(nodes_relying_on_query_edge_g, f"Come '{nodes_relying_on_query_edge_g.alias}' ha inserito '{nodes_relying_on_query_edge_g.answ}', tuttavia esso non contiene tutti e solo i nodi che dipendono dal query edge, pertanto la soluzione non è ottima.")
            sef.optimality_OK(nodes_relying_on_query_edge_g, f"'{nodes_relying_on_query_edge_g.alias}'={nodes_relying_on_query_edge_g.answ} è effettivamente la soluzione ottima.", f"")

        return True