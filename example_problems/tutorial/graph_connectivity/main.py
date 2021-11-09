from scc_lib import *

'''
3. check_certificate_of_nonconnectivity
his service checks whether a bipartition of the nodes is a valid certificate of the non-connectivity of a given graph
'''
n = 5
m = 5
seed = "lazy"

g,graph_print,edges,seed = GenerateGraph(seed, n, m, False)

print(graph_print)

# Inizio INPUT DEL BOT
input_spTree, not_visited_elements = g.spanning_tree() # Simulo la risposta del bot
spTree_elements = []

print("---")
for elem in input_spTree:
    print(elem[0])
    spTree_elements.append(elem[0])
print("-non visit:-")
for elem in not_visited_elements:
    print(elem)
print("---")
# Fine INPUT DEL BOT

# Cerco uno spanning tree e genero i 2 insiemi
spTree, not_spTree_list = g.spanning_tree() 
spTree_list = []

for elem in spTree:
    spTree_list.append(elem[0])

# Controllo uguaglianza delle liste (bipartizioni)

equals = sorted(spTree_elements) == sorted(spTree_list) and sorted(not_visited_elements) == sorted(not_spTree_list)

print(equals)
#span = Graph(int(n))
#is_correct = True
#
#for i in range(0, len(input_spTree)):
#    tail, head = input_spTree[i]
#    #print(head, tail)
#    # Verifico l'esistenza degli archi (e dei nodi)
#    if(g.checkEdge(head, tail)):
#        span.addEdge(int(head),int(tail))
#    else:
#        is_correct = False
#        break
## Controllo se è connesso
#is_correct = is_correct and span.isConnected()
#
#print(is_correct)

'''
4. eval_bot_deciding_connectivity
dato grafo, diamo certificato di connettività o no
'''

'''
print("# Dammi il grafo")

grafo = grafo_connesso

n,m = grafo[0].split()
n = int(n)
m = int(m)

g = Graph(int(n))

print("# Dammi il certificato")
'''