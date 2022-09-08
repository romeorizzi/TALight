import ast
import re
import networkx as nx
from sys import stderr
from typing import Dict
from RO_verify_submission_gen_prob_lib import verify_submission_gen

# specifiche dell'istanza del problema
instance_objects_spec = [
    ('n', int),                 # numero di nodi
    ('m', int),                 # numero di archi
    ('edges', str),             # lista degli archi
    ('forbidden_edges', str),   # lista indici degli archi da escludere
    ('forced_edges', str),      # lista indici degli archi obbligati
    ('query_edge', int)         # indice arco da esaminare
]

# specifiche delle risposte dell'utente
answer_objects_spec = {
    'opt_sol': str,         # soluzione ottimale (lista indici archi)
    'opt_val': int,         # Valore ottimale (peso di questa opt_sol)
    'num_opt_sols': int,    # numero di soluzioni ottimali totali
    'list_opt_sols': str,   # lista soluzioni ottimali
    'edge_profile': str,
    'cyc_cert': str,
    'edgecut_cert': str,
    'cutshore_cert': str
}

# lista delle soluzioni implementate
answer_objects_implemented = [
    'opt_sol',
    'opt_val',
    'num_opt_sols',
    'list_opt_sols',
    'edge_profile',
    'cyc_cert',
    'edgecut_cert',
    'cutshore_cert'
]


def check_isolated_nodes(n: int, edges: list) -> bool:
    """
    Verifica se esistono nodi isolati (nodi non connessi da archi).
    """
    nodes_found = set()
    for u, v, w in edges:
        nodes_found.add(u)
        nodes_found.add(v)
    return len(nodes_found) != n


def check_isolated_nodes_by_forbidden(n: int, edges: list, forbidden_edges: list) -> bool:
    """
    Verifica se esistono nodi isolati, anche a causa di archi esclusi.
    """
    nodes_found = set()
    for i, (u, v, w) in enumerate(edges):
        if i not in forbidden_edges:
            nodes_found.add(u)
            nodes_found.add(v)
    return len(nodes_found) != n


def check_tree(tree: list, edges: list, n: int) -> bool:
    """
    Verifica se la lista di archi corrisponde a un albero.
    """
    graph = nx.MultiGraph()
    graph.add_nodes_from(list(range(n)))
    for i in tree:
        u, v = list(edges[i][0])    # edges[i] == ({u, v}, w)
        graph.add_edge(u, v)
    return nx.is_tree(graph)


def check_spanning(tree: list, edges: list, n: int) -> bool:
    """
    Verifica se la lista di archi copre tutto il grafo.
    """
    nodes_found = set()
    for i in tree:
        nodes_found = nodes_found.union(edges[i][0])    # edges[i] == ({u, v}, w)
    return len(nodes_found) == n


def check_weight_in_range(input_weight: float, edges: list, nodes: int) -> int:
    """
    Verifica il peso totale dell'albero rientra nel range possibile.
    """
    weights = sorted([w for _, w in edges])     # ordina gli archi per peso crescente
    min_weight = sum(weights[:nodes - 1])       # somma i pesi dei primi |V| - 1 archi
    max_weight = sum(weights[-(nodes-1):])      # somma i pesi degli ultimi |V| - 1 archi
    return -1 if input_weight < min_weight else 1 if input_weight > max_weight else 0


def check_instance_consistency(instance: dict):
    """
    Verifica se l'istanza del problema immessa dal problem-maker è corretta.
    """
    print(f"instance={instance}", file=stderr)
    n = instance['n']
    m = instance['m']
    edges = instance['edges']
    forbidden_edges = instance['forbidden_edges']
    forced_edges = instance['forced_edges']
    query_edge = instance['query_edge']

    edges = ast.literal_eval(re.sub(r"[{}]", "", edges))
    forbidden_edges = ast.literal_eval(forbidden_edges)
    forced_edges = ast.literal_eval(forced_edges)

    if n <= 0:
        print(f"Errore: il numero di nodi è minore o uguale a 0")
        exit(0)
    if m <= 0:
        print(f"Errore: il numero di archi è minore o uguale a   0")
        exit(0)
    if m != len(edges):
        print(f"Errore: il numero di archi non corrisponde con il numero di archi della lista data")
        exit(0)
    if not all(w >= 0 for _, _, w in edges):
        print(f"Errore: alcuni pesi sono minori di 0")
    if not all(0 <= u < n and 0 <= v < n for u, v, _ in edges):
        print(f"Errore: alcuni nodi dati negli archi non esistono")
        exit(0)
    if not all(u != v for u, v, _ in edges):
        print(f"Errore: il grafo non può contenere auto-loop")
        exit(0)
    if not all(0 <= e < m for e in forbidden_edges):
        print(f"Errore: alcuni archi dichiarati in forbidden_edges non esistono")
        exit(0)
    if not all(0 <= e < m for e in forced_edges):
        print(f"Errore: alcuni archi dichiarati in forced_edges non esistono")
        exit(0)
    if not 0 <= query_edge < m:
        print(f"Errore: il query_edge non esiste")
        exit(0)
    if len(set(forbidden_edges).intersection(set(forced_edges))) != 0:
        print(f"Errore: alcuni forced_edges sono anche forbidden_edges")
        exit(0)
    if query_edge in forbidden_edges:
        print(f"Errore: il query_edge è nei forbidden_edges, la soluzione può solo che essere in_no")
        exit(0)
    if query_edge in forced_edges:
        print(f"Errore: il query_edge è nei forbidden_edges, la soluzione può solo che essere in_all")
        exit(0)
    if check_isolated_nodes(n, edges):
        print(f"Errore: sono presenti dei nodi isolati, non connessi da archi")
        exit(0)
    if check_isolated_nodes_by_forbidden(n, edges, forbidden_edges):
        print(f"Errore: sono presenti dei nodi isolati, dovuti ad archi eliminati da forbidden_edges")
        exit(0)


class Graph:
    """
    Classe per grafi pesati indiretti, con possibili archi paralleli.
    """

    def __init__(self, vertices: int):
        self.V = vertices   # numero di vertici
        self.edges = []     # lista degli archi, [(u, v, weight, label), ...]
        self.adjacency = [[[] for _ in range(vertices)] for _ in range(vertices)]   # matrice di adiacenza

    def add_edge(self, u: int, v: int, weight: float, label: int):
        """
        Aggiungi un arco al grafo.
        """
        self.edges.append((u, v, weight, label))
        self.adjacency[u][v].append({'weight': weight, 'label': label})
        self.adjacency[v][u].append({'weight': weight, 'label': label})

    def add_all_edges(self, edges: list):
        """
        Aggiungi una lista di archi pesati, nel formato [({u,v}, w), ...], al grafo attuale.
        """
        for label, edge in enumerate(edges):
            u, v = list(edge[0])
            weight = float(edge[1])
            self.add_edge(u, v, weight, label)

    def __search_root(self, parent: list, i: int) -> int:
        """
        Cerca il nodo radice del sotto albero a cui appartiene il nodo i
        """
        return i if parent[i] == i else self.__search_root(parent, parent[i])

    def __apply_union(self, parent: list, rank: list, u: int, v: int):
        """
        Unisci i sotto-alberi a cui appartengono u e v
        """
        u_root = self.__search_root(parent, u)
        v_root = self.__search_root(parent, v)
        if rank[u_root] < rank[v_root]:
            parent[u_root] = v_root
        elif rank[u_root] > rank[v_root]:
            parent[v_root] = u_root
        else:
            parent[v_root] = u_root
            rank[u_root] += 1

    def kruskal_constrained(self, forced: list, excluded: list) -> (list, int):
        """
        Trova un MST per il grafo attuale, considerando archi forzati e archi esclusi. Nota: funziona solo se il grafo
        è connesso.
        """
        mst = []
        i, e, tot_weight = 0, 0, 0
        self.edges = sorted(self.edges, key=lambda item: item[2])   # ordina gli archi in ordine crescente di peso
        parent = list(range(self.V))    # list del nodo genitore, per ogni nodo
        rank = [0] * self.V             # dimensione del sotto-albero di appartenenza per ogni nodo

        # aggiungo gli archi forzati alla soluzione (obbligati)
        for u, v, weight, label in self.edges:
            if label in forced:
                e += 1
                mst.append(label)
                tot_weight += weight
                u_root = self.__search_root(parent, u)              # ricerca della radice di u
                v_root = self.__search_root(parent, v)              # ricerca della radice di v
                self.__apply_union(parent, rank, u_root, v_root)    # unisci i due sotto-alberi

        # itera finché non completi l'albero (n°archi = |V| - 1)
        while e < self.V - 1:
            u, v, weight, label = self.edges[i]
            i += 1
            u_root = self.__search_root(parent, u)
            v_root = self.__search_root(parent, v)
            # se: le radici sono diverse, l'arco non è in quelli esclusi e non è già stato aggiunto (forzato)
            if u_root != v_root and label not in excluded and label not in forced:
                e += 1
                mst.append(label)   # aggiungi arco a mst
                tot_weight += weight
                self.__apply_union(parent, rank, u_root, v_root)    # unisci i due sotto-alberi

        return mst, tot_weight  # ritorno lista indice archi es.([0, 2]), peso totale

    def __find_substitute(self, cut: int, tree: set, excluded: set):
        """
        Trova un sostituto ideale per l'arco cut
        """
        # ricerca arco tagliato nella lista degli archi del grafo
        cut_u, cut_v, cut_w, cut_l = list(filter(lambda x: x[3] == cut, self.edges))[0]
        subtree = {cut_u}  # sotto-abero di partenza (l'altro sotto-albero corrisponde a V\subtree)
        tmp_list = [cut_u]  # lista dei nodi dei quali bisogna esplorare gli archi
        # costruzione dei due sotto-alberi generati dal taglio
        while tmp_list:
            u = tmp_list.pop()
            for v in range(self.V):
                # se il nodo v non fa parte di questo sotto-albero ed esistono archi che collegano u e v
                if v not in subtree and (edges := self.adjacency[u][v]):
                    # se il primo arco che collega u e v non fa parte dell'albero e non è l'arco tagliato
                    for edge in edges:
                        if edge['label'] in tree and edge['label'] != cut_l:
                            tmp_list.append(v)  # aggiungi v ai nodi di cui esplorare gli archi
                            subtree.add(v)  # aggiungi v al sotto-albero
                            break

        # ricerca di un sostituito per l'arco tagliato, ovvero un arco che riconnette i due sotto-alberi,
        # con peso uguale a quello tagliato (non può essere minore)
        for u in subtree:
            for v in range(self.V):
                if v not in subtree and (edges_uv := self.adjacency[u][v]):
                    for edge in edges_uv:
                        if edge['label'] != cut_l and edge['label'] not in excluded and edge['weight'] == cut_w:
                            return edge['label']

        # non esiste un sostituto per l'arco tagliato
        return None

    def __all_mst(self, tree: set, forced: set, excluded: set) -> list:
        """
        Trova tutti gli MST del grafo attuale, a partire da una soluzione ottima.
        """
        search_set = tree.difference(forced)    # si esclude dalla ricerca gli archi forzati
        forced_copy = forced.copy()
        msts = []
        for edge in search_set:
            sub = self.__find_substitute(edge, tree, excluded)  # ricerca del sostituto per edge
            if sub is not None:
                new_tree = tree.copy()          # nuovo mst trovato in cui...
                new_tree.remove(edge)           # ...sostituisco l'arco tagliato (edge)...
                new_tree.add(sub)               # ...con l'arco sostitutivo (sub)
                msts.append(list(new_tree))     # aggiungi il nuovo mst alla lista degli mst trovati
                # ricerca ricorsiva di nuovi mst a partire da quello nuovo trovato, inserendo tra gli esclusi edge
                msts += self.__all_mst(new_tree, forced_copy, excluded.union({edge}))
            forced_copy.add(edge)
        return msts

    def all_mst(self, forced: list, excluded: list) -> list:
        """
        Trova tutti gli MST del grafo attuale
        """
        # trova un mst di partenza
        first, _ = self.kruskal_constrained(forced, excluded)
        # trova tutti gli altri mst a partire dalla soluzione appena trovata
        return [first] + self.__all_mst(set(first), set(forced), set(excluded))

    def find_cutshore_and_edgecut(self, cut: int, tree: list, excluded: set) -> (list, list):
        """
        Costruisci i certificati di taglio a partire da un MST.
        """
        # ricerca arco tagliato nella lista degli archi del grafo
        cut_u, cut_v, cut_w, cut_l = list(filter(lambda x: x[3] == cut, self.edges))[0]
        subtree = {cut_u}  # sotto-abero di partenza (l'altro sotto-albero corrisponde a V\subtree)
        tmp_list = [cut_u]  # lista dei nodi dei quali bisogna esplorare gli archi

        # costruzione di uno dei due sotto-alberi generati dal taglio
        while tmp_list:
            u = tmp_list.pop()
            for v in range(self.V):
                # se il nodo v non fa parte di questo sotto-albero ed esistono archi che collegano u e v
                if v not in subtree and (edges := self.adjacency[u][v]):
                    # se il primo arco che collega u e v non fa parte dell'albero e non è l'arco tagliato
                    for edge in edges:
                        if edge['label'] in tree and edge['label'] != cut_l:
                            tmp_list.append(v)  # aggiungi v ai nodi di cui esplorare gli archi
                            subtree.add(v)  # aggiungi v al sotto-albero
                            break

        shore = subtree.copy()
        # verifica che sia effettivamente la shore più piccola, altrimenti inverti
        if len(shore) > (self.V // 2):
            shore = set(range(self.V)).difference(shore)

        edgecut = []
        # ricerca dei sostituiti per l'arco tagliato, ovvero un arco che riconnette i due sotto-alberi
        for u in subtree:
            for v in range(self.V):
                if v not in subtree and (edges_uv := self.adjacency[u][v]):
                    for edge in edges_uv:
                        if edge['label'] not in excluded:
                            edgecut.append(edge['label'])

        return list(shore), edgecut

    def __find_cyc_cert(self, visited_nodes: list, visited_edges: list, excluded: list, u: int, target: int):
        """
        Trova un certificato di ciclo attraverso DFS.
        """
        if u == target:
            return visited_edges
        elif u not in visited_nodes:
            visited_nodes.append(u)
            for v in range(self.V):
                if edges := self.adjacency[u][v]:
                    for edge in edges:
                        if edge['label'] not in excluded and edge['label'] not in visited_edges:
                            if (path := self.__find_cyc_cert(visited_nodes, visited_edges + [edge['label']], excluded, v, target)) is not None:
                                return path
        else:
            return None

    def find_cyc_cert(self, cut: int, excluded: list) -> list:
        """
        Trova un certificato di ciclo.
        """
        # ricerca arco tagliato nella lista degli archi del grafo
        cut_u, cut_v, cut_w, cut_l = list(filter(lambda x: x[3] == cut, self.edges))[0]
        return self.__find_cyc_cert(list(), list(), excluded + [cut_l], cut_v, cut_u) + [cut_l]

    def check_edgecut_cert(self, edgecut: list, excluded: list) -> bool:
        """
        Verifica che i due shore siano perfettamente separate dall'edgecut
        """
        cut_u, cut_v, cut_w, cut_l = list(filter(lambda x: x[3] == edgecut[0], self.edges))[0]
        subtree1 = {cut_u}  # primo sotto-abero di partenza
        tmp_list = [cut_u]  # lista dei nodi dei quali bisogna esplorare gli archi

        # costruzione di uno dei due sotto-alberi generati dal taglio
        while tmp_list:
            u = tmp_list.pop()
            for v in range(self.V):
                # se il nodo v non fa parte di questo sotto-albero ed esistono archi che collegano u e v
                if v not in subtree1 and (edges := self.adjacency[u][v]):
                    # non percorrere archi che fanno parte dell'edgecut o che sono esclusi
                    if edges[0]['label'] not in edgecut and edges[0]['label'] not in excluded:
                        tmp_list.append(v)  # aggiungi v ai nodi di cui esplorare gli archi
                        subtree1.add(v)     # aggiungi v al sotto-albero

        subtree2 = {cut_v}  # secondo sotto-abero di partenza
        tmp_list = [cut_v]  # lista dei nodi dei quali bisogna esplorare gli archi

        # costruzione dell'altro dei due sotto-alberi generati dal taglio
        while tmp_list:
            u = tmp_list.pop()
            for v in range(self.V):
                # se il nodo v non fa parte di questo sotto-albero ed esistono archi che collegano u e v
                if v not in subtree2 and (edges := self.adjacency[u][v]):
                    # non percorrere archi che fanno parte dell'edgecut o che sono esclusi
                    if edges[0]['label'] not in edgecut and edges[0]['label'] not in excluded:
                        tmp_list.append(v)  # aggiungi v ai nodi di cui esplorare gli archi
                        subtree2.add(v)     # aggiungi v al sotto-albero

        # se esistono elementi in comune tra i subtree allora la divisione dell'edgecut non è netta
        return len(subtree1.intersection(subtree2)) == 0

    def check_cyc_cert(self, cyc_cert: list, excluded: list) -> bool:
        """
        Verifica la lista di archi inseriti sia effettivamente un ciclo.
        """
        # verifica che ogni arco abbia un solo nodo in comune con l'arco successivo
        for i in range(len(cyc_cert) - 1):
            if cyc_cert[i] in excluded:
                return False
            u, v, _, _ = self.edges[cyc_cert[i]]
            edge1 = {u, v}
            if cyc_cert[i + 1] in excluded:
                return False
            u, v, _, _ = self.edges[cyc_cert[i + 1]]
            edge2 = {u, v}
            if len(edge1.intersection(edge2)) != 1:
                return False

        # verifica che il primo e l'ultimo arco abbiano un solo nodo in comune
        u, v, _, _ = self.edges[cyc_cert[0]]
        edge1 = {u, v}
        u, v, _, _ = self.edges[cyc_cert[-1]]
        edge2 = {u, v}
        if len(edge1.intersection(edge2)) != 1:
            return False

        return True


def solver(input_to_oracle: dict) -> dict:
    instance = input_to_oracle['input_data_assigned']
    n = instance['n']
    m = instance['m']
    edges = instance['edges']
    forbidden_edges = instance['forbidden_edges']
    forced_edges = instance['forced_edges']
    query_edge = instance['query_edge']

    edges = ast.literal_eval(edges)
    forbidden_edges = ast.literal_eval(forbidden_edges)
    forced_edges = ast.literal_eval(forced_edges)
    graph = Graph(n)
    graph.add_all_edges(edges)

    opt_sol, opt_val = graph.kruskal_constrained(forced_edges, forbidden_edges)
    list_opt_sols = graph.all_mst(forced_edges, forbidden_edges)
    num_opt_sols = len(list_opt_sols)
    count = [query_edge in sol for sol in list_opt_sols].count(True)
    cutshore_cert = []
    edgecut_cert = []
    cyc_cert = []
    if count == len(list_opt_sols):
        edge_profile = 'in_all'
        cutshore_cert, edgecut_cert = \
            graph.find_cutshore_and_edgecut(query_edge, list(filter(lambda x: query_edge in x, list_opt_sols))[0], set(forbidden_edges))
    elif count > 0:
        edge_profile = 'in_some_but_not_in_all'
        cutshore_cert, edgecut_cert = \
            graph.find_cutshore_and_edgecut(query_edge, list(filter(lambda x: query_edge in x, list_opt_sols))[0], set(forbidden_edges))
    else:
        edge_profile = 'in_no'
        cyc_cert = graph.find_cyc_cert(query_edge, forbidden_edges)

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

    def set_up_and_cash_handy_data(self):
        self.graph = Graph(self.I.n)
        self.graph.add_all_edges(ast.literal_eval(self.I.edges))

    def verify_format(self, sef):
        """
        Verifica che il formato delle risposte sottomesse dal problem solver sia corretto.
        """
        if not super().verify_format(sef):
            return False

        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            if type(g.answ) != str:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una stringa.")
            try:
                answ = ast.literal_eval(g.answ)
                if type(answ) != list:
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di archi. Una lista di archi è costituita da una "
                                            f"lista di indici riferiti all'elenco degli archi nell'istanza del "
                                            f"problema.")
                if any([type(edge) != int for edge in answ]):
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di archi. Una lista di archi è costituita da una "
                                            f"lista di indici (interi) riferiti all'elenco degli archi nell'istanza "
                                            f"del problema.")
            except SyntaxError:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una lista di archi. Impossibile effettuare il parsing dell'input: "
                                        f"errore nella sintassi.")
            sef.format_OK(g, f"Come '{g.alias}' hai immesso una lista di archi come richiesto.",
                          f"Ovviamente durante lo svolgimento dell'esame non posso dirti se la stringa inserita sia poi"
                          f"la risposta giusta, ma il formato è comunque corretto.")

        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            if type(g.answ) != int:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere un valore intero.")
            sef.format_OK(g, f"Come `{g.alias}` hai immesso un valore intero come richiesto.",
                          f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi "
                          f"il valore giusto, ma il formato è comunque corretto")

        if 'num_opt_sols' in self.goals:
            g = self.goals['num_opt_sols']
            if type(g.answ) != int:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere un valore intero.")
            sef.format_OK(g, f"Come '{g.alias}' hai immesso un valore intero come richiesto.",
                          f"Ovviamente durante lo svolgimento dell'esame non posso dirti se il valore immesso sia poi "
                          f"il valore giusto, ma il formato è comunque corretto")

        if 'list_opt_sols' in self.goals:
            g = self.goals['list_opt_sols']
            if type(g.answ) != str:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una stringa.")
            try:
                answ = ast.literal_eval(g.answ)
                if type(answ) != list:
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di liste di archi. Una lista di archi è costituita "
                                            f"da una lista di indici riferiti all'elenco degli archi nell'istanza del "
                                            f"problema.")
                if any([type(tree) != list for tree in answ]):
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di liste di archi. Una lista di archi è costituita "
                                            f"da una lista di indici riferiti all'elenco degli archi nell'istanza del "
                                            f"problema.")
                for tree in answ:
                    if any([type(edge) != int for edge in tree]):
                        return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                                f"immettere una lista di liste di archi. Una lista di archi è "
                                                f"costituita da una lista di indici (interi) riferiti all'elenco "
                                                f"degli archi nell'istanza del problema.")
            except SyntaxError:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una lista di liste di archi. Impossibile effettuare il parsing "
                                        f"dell'input: errore nella sintassi.")
            sef.format_OK(g, f"Come `{g.alias}` hai immesso una lista di liste di archi, come richiesto.",
                          f"Ovviamente durante lo svolgimento dell'esame non posso dirti se la stringa inserita sia "
                          f"poi la risposta corretta, ma il formato è corretto")

        if 'edge_profile' in self.goals:
            g = self.goals['edge_profile']
            if type(g.answ) != str:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una stringa.")
            if g.answ not in ['in_all', 'in_no', 'in_some_but_not_in_all']:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', tuttavia le uniche risposte "
                                        f"accettate: 'in_all', 'in_no', 'in_some_but_not_in_all'.")
            sef.format_OK(g, f"Come '{g.alias}' hai immesso una stringa come richiesto.",
                          f"Ovviamente durante lo svolgimento dell'esame non posso dirti se la stringa inserita sia "
                          f"poi la risposta giusta, ma il formato è comunque corretto.")

        if 'edgecut_cert' in self.goals:
            g = self.goals['edgecut_cert']
            if type(g.answ) != str:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una stringa.")
            try:
                answ = ast.literal_eval(g.answ)
                if type(answ) != list:
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di archi. Una lista di archi è costituita da una "
                                            f"lista di indici riferiti all'elenco degli archi nell'istanza del "
                                            f"problema.")
                if any([type(edge) != int for edge in answ]):
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di archi. Una lista di archi è costituita da una "
                                            f"lista di indici (interi) riferiti all'elenco degli archi nell'istanza "
                                            f"del problema.")
            except SyntaxError:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una lista di archi. Impossibile effettuare il parsing "
                                        f"dell'input: errore nella sintassi.")
            sef.format_OK(g, f"come `{g.alias}` hai immesso una lista di archi come richiesto.",
                          f"Ovviamente durante lo svolgimento dell'esame non posso dirti se la stringa inserita sia "
                          f"poi la risposta corretta, ma il formato è comunque corretto.")

        if 'cutshore_cert' in self.goals:
            g = self.goals['cutshore_cert']
            if type(g.answ) != str:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una stringa.")
            try:
                answ = ast.literal_eval(g.answ)
                if type(answ) != list:
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di nodi. Una lista di archi è costituita da una "
                                            f"lista di identificatori, nel range di identificatori dei nodi possibili "
                                            f"stabilito dall'istanza del problema.")
                if any([type(node) != int for node in answ]):
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di nodi. Una lista di archi è costituita da una "
                                            f"lista di identificatori (interi), nel range di identificatori dei nodi "
                                            f"possibili stabilito dall'istanza del problema.")
            except SyntaxError:
                return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                        f"immettere una lista di nodi. Impossibile effettuare il parsing dell'input: "
                                        f"errore nella sintassi.")
            sef.format_OK(g, f"Come '{g.alias}' hai immesso una lista di nodi come richiesto.",
                          f"Ovviamente durante lo svolgimento dell'esame non posso dirti se la stringa inserita sia "
                          f"poi la risposta giusta, ma il formato è comunque corretto")

            if 'cyc_cert' in self.goals:
                g = self.goals['cyc_cert']
                if type(g.answ) != str:
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una stringa.")
                try:
                    answ = ast.literal_eval(g.answ)
                    if type(answ) != list:
                        return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                                f"immettere una lista di archi. Una lista di archi è costituita da una "
                                                f"lista di indici riferiti all'elenco degli archi nell'istanza del "
                                                f"problema.")
                    if any([type(edge) != int for edge in answ]):
                        return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                                f"immettere una lista di archi. Una lista di archi è costituita da una "
                                                f"lista di indici (interi) riferiti alla lista degli archi "
                                                f"nell'istanza del problema.")
                except SyntaxError:
                    return sef.format_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}' dove era invece richiesto di "
                                            f"immettere una lista di archi. Impossibile effettuare il parsing "
                                            f"dell'input: errore nella sintassi.")
                sef.format_OK(g, f"come `{g.alias}` hai immesso una lista di archi come richiesto.",
                              f"Ovviamente durante lo svolgimento dell'esame non posso dirti se la stringa inserita "
                              f"sia poi la risposta giusta, ma il formato è comunque corretto.")

        return True

    def verify_feasibility(self, sef):
        """
        Verifica che le risposte che il problem solver ha inserito siano sensate rispetto all'istanza del problema.
        """
        if not super().verify_feasibility(sef):
            return False

        n = self.I.n
        m = self.I.m
        edges = ast.literal_eval(self.I.edges)
        forbidden_edges = ast.literal_eval(self.I.forbidden_edges)
        forced_edges = ast.literal_eval(self.I.forced_edges)
        query_edge = self.I.query_edge

        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            answ = ast.literal_eval(g.answ)
            if not all(0 <= e < m for e in answ):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti indici di archi che non esistono.")
            if len(answ) != len(set(answ)):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti degli indici ripetuti di archi.")
            if not check_tree(answ, edges, n):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma esso non rappresenta un "
                                             f"albero, pertanto la soluzione non è valida.")
            if not check_spanning(answ, edges, n):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma non copre tutti i nodi, "
                                             f"pertanto la soluzione non è valida.")
            if len(set(answ).intersection(set(forbidden_edges))) != 0:
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti dei forbidden_edges, pertanto la soluzione non è valida.")
            if len(set(answ).intersection(set(forced_edges))) != len(forced_edges):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno non sono "
                                             f"presenti tutti i forced_edges, pertanto la soluzione non è valida.")
            sef.feasibility_OK(g, f"Come '{g.alias}' hai immesso un sottoinsieme degli oggetti dell'istanza originale.",
                               f"Ora resta da stabilire l'ottimalità di '{g.alias}'.")

        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            if (res := check_weight_in_range(g.answ, edges, n)) != 0:
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma esso sfora la somma "
                                             f"{'minima' if res < 0 else 'massima'} possibile dei pesi nel grafo.")
            sef.feasibility_OK(g, f"Come '{g.alias}' hai immesso un valore di peso valido.",
                               f"Ora resta da stabilire l'ottimalità di '{g.alias}'.")

        if 'list_opt_sols' in self.goals:
            g = self.goals['list_opt_sols']
            answ = ast.literal_eval(g.answ)
            for tree in answ:
                if any(e < 0 or e >= m for e in tree):
                    return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma alcune delle soluzioni "
                                                 f"presentano degli indici di archi che non esistono, pertanto la "
                                                 f"lista delle soluzioni non è valida.")
                if len(tree) != len(set(tree)):
                    return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma alcune delle soluzioni "
                                                 f"presentano degli archi ripetuti, pertanto la lista delle soluzioni "
                                                 f"non è valida.")
                if not check_tree(tree, edges, n):
                    return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma alcune delle soluzioni "
                                                 f"non rappresentano un albero, pertanto la lista delle soluzioni non"
                                                 f" è valida.")
                if not check_spanning(tree, edges, n):
                    return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma alcune delle soluzioni "
                                                 f"non coprono tutti nodi, pertanto la lista delle soluzioni non è "
                                                 f"valida.")
                if len(set(tree).intersection(set(forbidden_edges))) != 0:
                    return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma alcune delle soluzioni "
                                                 f"contengono dei forbidden_edges, pertanto la lista delle soluzioni "
                                                 f"non è valida.")
                if len(set(tree).intersection(set(forced_edges))) != len(forced_edges):
                    return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma alcune delle soluzioni "
                                                 f"non contengono tutti i forced_edges, pertanto la lista delle "
                                                 f"soluzioni non è valida.")
            sef.feasibility_OK(g, f"Come '{g.alias}' hai immesso una lista di oggetti valida.",
                               f"Ora resta da stabilire l'ottimalità delle soluzioni in '{g.alias}'.")

        if 'num_opt_sols' in self.goals:
            g = self.goals['num_opt_sols']
            if g.answ <= 0:
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma il numero di soluzioni "
                                             f"ottime deve essere maggiore di 0, pertanto il valore inserito non è "
                                             f"valido.")
            if g.answ > n ** (n - 2):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma in qualsiasi grafo non "
                                             f"possono esistere più di n^(n-2) spanning trees, dove n è il numero di "
                                             f"archi, pertanto il valore inserito non è valido.")
            sef.feasibility_OK(g, f"Come '{g.alias}' hai immesso un numero di soluzioni valido.",
                               f"Ora resta da stabilire la correttezza di '{g.alias}'.")

        if 'edgecut_cert' in self.goals:
            g = self.goals['edgecut_cert']
            answ = ast.literal_eval(g.answ)
            if any(e < 0 or e >= m for e in answ):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti indici di archi che non esistono, pertanto il certificato "
                                             f"inserito non è valido.")
            if len(answ) != len(set(answ)):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti indici ripetuti di archi, pertanto il certificato inserito "
                                             f"non è valido.")
            if len(set(answ).intersection(set(forbidden_edges))) != 0:
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti dei forbidden_edges, pertanto il certificato inserito non è "
                                             f"valido.")
            if query_edge not in answ:
                return sef.feasiblity_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma esso non contiente il "
                                            f"query_edge, pertanto il certificato inserito non è valido.")
            if not self.graph.check_edgecut_cert(answ, forbidden_edges):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma non risulta essere un "
                                             f"cutset corretto per il grafo, pertanto il certificato inserito non è "
                                             f"valido.")
            sef.feasibility_OK(g, f"Come '{g.alias}' hai immesso un certificato valido.",
                               f"Ora resta da stabilire la correttezza di '{g.alias}'.")

        if 'cutshore_cert' in self.goals:
            g = self.goals['cutshore_cert']
            answ = ast.literal_eval(g.answ)
            if any(v < 0 or v >= n for v in answ):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti identificatori di nodi che non esistono, pertanto il "
                                             f"certificato inserito non è valido.")
            if len(answ) != len(set(answ)):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti identificatori di nodi ripetuti, pertanto il certificato "
                                             f"inserito non è valido.")
            if len(answ) > n // 2:
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', esse non può essere la shore "
                                             f"più piccola.")
            sef.feasibility_OK(g, f"Come '{g.alias}' hai immesso un certificato valido.",
                               f"Ora resta da stabilire la correttezza di '{g.alias}'.")

        if 'cyc_cert' in self.goals:
            g = self.goals['opt_sol']
            answ = ast.literal_eval(g.answ)
            if any(e < 0 or e >= m for e in answ):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti indici di archi che non esistono, pertanto il certificato "
                                             f"inserito non è valido.")
            if len(answ) != len(set(answ)):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti indici ripetuti di archi, pertanto il certificato immesso non "
                                             f"è valido.")
            if len(set(answ).intersection(set(forbidden_edges))) != 0:
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma al suo interno sono "
                                             f"presenti dei forbidden_edges, pertanto il certificato inserito non è "
                                             f"valido.")
            if not self.graph.check_cyc_cert(answ, forbidden_edges):
                return sef.feasibility_NO(g, f"Come '{g.alias}' hai immesso '{g.answ}', ma non risulta essere un "
                                             f"ciclo valido, pertanto il certificato inserito non è valido.")
            sef.feasibility_OK(g, f"Come '{g.alias}' hai immesso un certificato valido,",
                               f"Ora resta da stabilire la correttezza di '{g.alias}'.")

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
            if sum([edges[i][1] for i in opt_sol_answ]) != opt_val_g.answ:
                return sef.consistency_NO(['opt_val', 'opt_sol'],
                                          f"Il peso totale di '{opt_sol_g.alias}' è {opt_sol_g.answ}, ma esso non "
                                          f"corrisponde al valore '{opt_val_g.alias}', {opt_val_g.answ}.")
            sef.consistency_OK(['opt_sol', 'opt_val'],
                               f"Il peso totale di '{opt_sol_g.alias}' e il valore '{opt_val_g.alias}' corrispondono.",
                               f"Ora resta da verificare l'ottimalità di entrambi.")

        # tutte gli mst della lista list_opt_sols devono avere lo stesso peso
        if 'list_opt_sols' in self.goals:
            g = self.goals['list_opt_sols']
            answ = ast.literal_eval(g.answ)
            sols_weights = [sum([edges[i][1] for i in tree]) for tree in answ]
            if len(set(sols_weights)) != 1:
                return sef.consistency_NO(['list_opt_sols'],
                                          f"Non tutte le soluzioni in '{g.alias}' hanno lo stesso peso, pertanto la "
                                          f"lista delle soluzioni non è valida.")
            sef.consistency_OK(['list_opt_sols'],
                               f"Tutte le soluzioni in '{self.goals}' hanno lo stesso peso.",
                               f"Ora resta da verificare l'ottimalità.")

        # il numero di soluzioni ottime num_opt_sols deve corrispondere al numero di soluzioni in list_opt_sols
        if 'list_opt_sols' in self.goals and 'num_opt_sols' in self.goals:
            list_opt_sols_g = self.goals['list_opt_sols']
            num_opt_sols_g = self.goals['num_opt_sols']
            list_opt_sols_answ = ast.literal_eval(list_opt_sols_g.answ)
            if num_opt_sols_g.answ != len(list_opt_sols_answ):
                return sef.consistency_NO(['list_opt_sols', 'num_opt_sols'],
                                          f"Come '{list_opt_sols_g.alias}' hai inserito '{list_opt_sols_g.answ}', ma "
                                          f"essa presenta un numero di soluzioni diverso dal valore "
                                          f"'{num_opt_sols_g.alias}' immesso, {num_opt_sols_g.answ}.")
            sef.consistency_OK(['list_opt_sols', 'opt_val'],
                               f"Il numero di soluzioni di '{list_opt_sols_g.alias}' corrisponde con il valore "
                               f"'{num_opt_sols_g.alias}' inserito.",
                               f"Ora resta da verificare l'ottimalità.")

        # il peso di ogni soluzione in list_opt_sols deve corrispondere al valore opt_val
        if 'list_opt_sols' in self.goals and 'opt_val' in self.goals:
            list_opt_sols_g = self.goals['list_opt_sols']
            opt_val_g = self.goals['opt_val']
            list_opt_sols_answ = ast.literal_eval(list_opt_sols_g.answ)
            sols_weights = [sum([edges[i][1] for i in tree]) for tree in list_opt_sols_answ]
            if any(weight != opt_val_g.answ for weight in sols_weights):
                return sef.consistency_NO(['list_opt_sols', 'opt_val'],
                                          f"Il peso totale di alcune delle soluzioni in '{list_opt_sols_g.alias}' e "
                                          f"il valore di '{opt_val_g.alias}', {opt_val_g.answ}, non corrispondono.")
            sef.consistency_OK(['list_opt_sols', 'opt_val'],
                               f"Il peso totale di ogni soluzione in '{list_opt_sols_g.alias}' corrisponde con il "
                               f"valore '{opt_val_g.alias}' inserito.",
                               f"Ora resta da verificare l'ottimalità.")

        # se si dichiara un edge_profile devono essere presenti i relativi certificati
        if 'edge_profile' in self.goals:
            g = self.goals['edge_profile']
            if g.answ in ['in_all', 'in_some_but_not_in_all'] and \
                    'edgecut_cert' not in self.goals and 'cutshore_cert' not in self.goals:
                return sef.consistency_NO(['edge_profile', 'edgecut_cert', 'cutshore_cert'],
                                          f"Come {g.alias} hai inserito {g.answ}, ma non hai inserito né un "
                                          f"cutshore_cert né un edgecut_cert, pertanto {g.alias} non può essere "
                                          f"certificata.")
            sef.consistency_OK(['edge_profile', 'edgecut_cert', 'cutshore_cert'],
                               f"Hai inserito i certificati adatti al {g.alias} dichiarato.",
                               f"Ora resta da verificare la correttezza.")
            if g.answ == 'in_no' and 'cyc_cert' not in self.goals:
                return sef.consistency_NO(['edge_profile', 'edgecut_cert', 'cutshore_cert'],
                                          f"Come {g.alias} hai inserito {g.answ}, ma non hai inserito un cyc_cert, "
                                          f"pertanto {g.alias} non può essere certificato.")
            sef.consistency_OK(['edge_profile', 'cyc_cert'],
                               f"Hai inserito i certificati adatti al {g.alias} dichiarato.",
                               f"Ora resta da verificare la correttezza.")

        # edgecut_cert e cutshore_cert devono corrispondere allo stesso cut del grafo
        if 'edgecut_cert' in self.goals and 'cutshore_cert' in self.goals:
            edgecut_cert_g = self.goals['edgecut_cert']
            cutshore_cert_g = self.goals['cutshore_cert']
            edgecut_cert = ast.literal_eval(edgecut_cert_g.answ)
            cutshore_cert = ast.literal_eval(cutshore_cert_g.answ)
            if any(((u in cutshore_cert) == (v in cutshore_cert)) for u, v in [list(edges[i][0]) for i in edgecut_cert]):
                # dopo aver estratto gli archi dell'edgecut dalla lista degli edges, verifica che ognuno di questi archi non colleghino due nodi nella stessa shore
                return sef.consistency_NO(['edgecut_cert', 'cutshore_cert'],
                                          f"{cutshore_cert_g.answ} e {edgecut_cert_g.answ} non corrispondono allo "
                                          f"stesso cut del grafo.")
            sef.consistency_OK(['edgecut_cert', 'cutshore_cert'],
                               f"{cutshore_cert_g.answ} e {edgecut_cert_g.answ} corrispondono allo stesso cut.",
                               f"Ora resta da verificare la correttezza.")

        return True

    def verify_optimality(self, sef):
        """
        Verifica che le risposte inserite dell'utente siano quelle corrette
        """
        if not super().verify_optimality(sef):
            return False

        n = self.I.n
        m = self.I.m
        edges = ast.literal_eval(self.I.edges)
        forbidden_edges = ast.literal_eval(self.I.forbidden_edges)
        forced_edges = ast.literal_eval(self.I.forced_edges)
        query_edge = self.I.query_edge

        # verifica che opt_val sia effettivamente ottimo
        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            true_answ = sef.oracle_dict['opt_val']
            if g.answ != true_answ:
                return sef.optimality_NO(g, f"Come '{g.alias}' ha inserito '{g.answ}', tuttavia esso non è il valore "
                                            f"minimo possibile, {true_answ}, pertanto il valore non è corretto.")
            sef.optimality_OK(g, f"{g.alias} = {true_answ} è effettivamente il valore ottimo.", "")

        # verifica che la soluzione opt_sol sia una delle possibili soluzioni ottime
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            answ = ast.literal_eval(g.answ)
            list_opt_sols = sum([set(tree) for tree in sef.oracle_dict['opt_sol']])
            if set(answ) not in list_opt_sols:
                return sef.optimality_NO(g, f"Come '{g.alias}' hai inserito '{g.answ}', ma essa non è tra le "
                                            f"soluzioni ottime, pertanto la soluzione inserita non è corretta")
            sef.optimality_OK(g, f"{g.alias} = {g.answ} é effettivamente una possibile soluzione ottima.", "")

        # verifica che il numero di soluzioni ottime sia corretto
        if 'num_opt_sols' in self.goals:
            g = self.goals['num_opt_sols']
            true_answ = sef.oracle_dict['num_opt_sols']
            if g.answ != true_answ:
                return sef.optimality_NO(g, f"Come '{g.alias}' hai inserito '{g.answ}', ma questo non corrisponde al "
                                            f"numero di soluzioni ottime corretto.")
            sef.optimality_OK(g, f"{g.alias} = {g.answ} è effettivamente il numero corretto di soluzioni ottime.", "")

        # verifica che la lista delle soluzioni corrisponda a quella reale
        if 'list_opt_sols' in self.goals:
            g = self.goals['list_opt_sols']
            answ = [set(tree) for tree in ast.literal_eval(g.answ)]
            true_answ = [set(tree) for tree in sef.oracle_dict['list_opt_sols']]
            if answ != true_answ:
                return sef.optimality_NO(g, f"Come '{g.alias}' hai inserito '{g.answ}', ma essa non corrisponde a "
                                            f"quella reale, pertanto la lista inserita non è corretta.")
            sef.optimality_OK(g, f"{g.alias} = {g.answ} è effettivamente la lista completa di soluzioni ottime", "")

        # verifica che edge profile sia corretto con relativi certificati
        if 'edge_profile' in self.goals:
            g = self.goals['edge_profile']
            true_answ = sef.oracle_dict['edge_profile']
            if g.answ != true_answ:
                return sef.optimality_NO(g, f"Come '{g.alias}' hai inserito '{g.answ}', ma la risposta non risulta "
                                            f"essere quella corretta.")
            sef.optimality_OK(g, f"{g.alias} = {g.answ} è effettivamente la risposta corretta per l'arco richiesto", "")
            if g.answ == 'in_all':
                if 'edgecut_cert' in self.goals:
                    edgecut_cert_g = self.goals['edgecut_cert']
                    edgecut_cert_answ: list = ast.literal_eval(edgecut_cert_g.answ)
                    if any([w <= edges[query_edge][2] for _, _, w, _ in list(filter(lambda x: x[3] in edgecut_cert_answ, edges))]):
                        # ogni peso dell'edgecut sia <= query_edge
                        return sef.optimality_NO(g, f"Secondo il certificato {edgecut_cert_g.alias}, il {g.alias} non "
                                                    f"è l'arco strettamente minore.")
                    sef.optimality_OK(g, f"Il certificato {edgecut_cert_g.alias} effettivamente dimostra che {g.alias} "
                                         f"deve appartenere a tutte le soluzioni ottime.", "")
                if 'cutshore_cert' in self.goals:
                    cutshore_cert_g = self.goals['cutshore_cert']
                    cutshore_cert_answ: list = ast.literal_eval(cutshore_cert_g.answ)
                    if any([w <= edges[query_edge][2] for u, v, w, l in edges if ((u in cutshore_cert_answ) ^ (v in cutshore_cert_answ)) and l != query_edge]):
                        # arco con peso minore
                        return sef.optimality_NO(g, f"Secondo il certificato {cutshore_cert_g.alias}, il {g.alias} non "
                                                    f"è l'arco strettamente minore.")
                    sef.optimality_OK(g, f"Il certificato {cutshore_cert_g.alias} effettivamente dimostra che {g.alias}"
                                         f" deve appartenere a tutte le soluzioni ottime.", "")
            if g.answ == 'in_some_but_not_in_all':
                if 'edgecut_cert' in self.goals:
                    edgecut_cert_g = self.goals['edgecut_cert']
                    edgecut_cert_answ: list = ast.literal_eval(edgecut_cert_g.answ)
                    edgecut_cert_answ.remove(query_edge)
                    if any([w < edges[query_edge][2] for _, _, w, _ in list(filter(lambda x: x[3] in edgecut_cert_answ, edges))]):
                        # query_edge non strettamente minore
                        return sef.optimality_NO(g, f"Secondo il certificato {edgecut_cert_g.alias}, il {g.alias} non "
                                                    f"è uno degli archi di peso minimo.")
                    sef.optimality_OK(g, f"Il certificato {edgecut_cert_g.alias} effettivamente dimostra che {g.alias} "
                                         f"appartiene ad alcune delle soluzioni ottime.", "")
                if 'cutshore_cert' in self.goals:
                    cutshore_cert_g = self.goals['cutshore_cert']
                    cutshore_cert_answ: list = ast.literal_eval(cutshore_cert_g.answ)
                    if any([w < edges[query_edge][2] for u, v, w, l in edges if ((u in cutshore_cert_answ) ^ (v in cutshore_cert_answ)) and l != query_edge]):
                        return sef.optimality_NO(g, f"Secondo il certificato {cutshore_cert_g.alias}, il {g.alias} non "
                                                    f"è l'arco strettamente minore.")
                    sef.optimality_OK(g, f"Il certificato {cutshore_cert_g.alias} effettivamente dimostra che {g.alias}"
                                         f"appartiene ad alcune delle soluzioni ottime.", "")
            if g.answ == 'in_no':
                if 'cyc_cert' in self.goals:
                    cyc_cert_g = self.goals['cyc_cert']
                    cyc_cert_answ: list = ast.literal_eval(cyc_cert_g.answ)
                    if any([w >= edges[query_edge][2] for _, _, w, _ in list(filter(lambda x: x[3] in cyc_cert_answ, edges))]):
                        # query_edge è quello strettamente maggiore nel ciclo
                        return sef.optimality_NO(g, f"Secondo il certificato {cyc_cert_g.alias}, il {g.alias} non "
                                                    f"è l'arco strettamente maggiore.")
                    sef.optimality_OK(g, f"Il certificato {cyc_cert_g.alias} effettivamente dimostra che {g.alias} "
                                         f"non appartiene a nessuna delle soluzioni ottime.", "")

        return True
