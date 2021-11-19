#!/usr/bin/env python3
  
from collections import defaultdict 
import random 
from sys import stderr, exit


class Graph(): 
  
	def __init__(self, vertices): 
		self.V = vertices 
		self.graph = defaultdict(list) 

	def addEdge(self, v, u): 
		self.graph[v].append(u) 
		#self.graph[u].append(v) 

	def tostring(self):
		import json
		return json.dumps(self.graph)


	def checkEdge(self, v, u):
		if u == 0 and v == 0:
			return True

		if u in self.graph[v]:
			return True
		return False

	def listNotConnectedEdges(self):
		list_nc = []

		for v in range(self.V):
			for u in range(self.V):
				if not self.checkEdge(v, u):
					list_nc.append((v, u))

		return list_nc

	'''
		DFS dato nodo v di partenza
	'''
	def DFSUtil(self, v, visited): 
		visited[v] = True
		for node in self.graph[v]: 
			if visited[node] == False: 
				self.DFSUtil(node, visited) 
	'''
		Ritorna se il grafo è connesso o no, utilizzando la DFS
	'''
	def isConnected(self, return_not_connected=False):
		v = 0
		visited = [False] * (self.V)

		self.DFSUtil(v, visited)
		for i in range(self.V): 
			#print(visited[i])
			if visited[i] == False:
				return False, []
		
		if(return_not_connected):
			# listo i non connessi
			not_conn = []
			for i in range(len(visited)):
				if(not visited[i]):
					not_conn.append(i)

			for elem in not_conn:
				print(elem)

			return True, not_conn
		return True, []

	'''
		DFS che tiene traccia dei nodi visitati
	'''
	def DFS_spanning(self, v, dad, visited): 
		visited[v] = dad

		for node in self.graph[v]: 
			if visited[node] == -1: 
				self.DFS_spanning(node, v, visited) 

	'''
		Ritorna:
		- lo spanning tree sotto forma di routing table
		- lista dei nodi non toccati dallo spanning tree
	'''
	def spanning_tree(self):  
		v = 0
		visited = [-1] * (self.V)

		spanning_tree = []
		not_visited = []

		self.DFS_spanning(v, v, visited)
		for i in range(self.V): 
			if visited[i] == -1:
				not_visited.append(i)
			else:
				spanning_tree.append((i, visited[i]))
		
		return spanning_tree, not_visited

'''
Genera un grafo dato seed, n, m 
indicando tramite parametro 'is_connected' se deve essere connesso o no
'''

'''def GenerateGraphOLD(seed, n, m, is_connected):
	if seed == "lazy":
		shake = random.randrange(10000,80000)
		random.seed(shake)
	else:
		shake = seed
		random.seed(int(seed))

	while True:
		g = Graph(n)
		graph_print = f"{n} {m}\n"
		edges = ""

		for i in range(m):
			head = random.randrange(0,n)
			tail = random.randrange(0,n)
			g.addEdge(head,tail)
			
			if(i < m-1):
				graph_print = graph_print+f"{head} {tail}\n"
			else:
				graph_print = graph_print+f"{head} {tail}"
			edges = edges+f"{head} {tail}-"
		# Esco solo se il grafo generato è connesso
		if(g.isConnected()[0] == is_connected): 
			break

	return g, graph_print, edges, shake
'''

'''
Generazione grafo da albero via Prufer
'''
def generateTreeEdges(prufer,m, g):
	vertices = m + 2
	vertex_set = [0] * vertices
	graph_print = ""

	for i in range(vertices):
		vertex_set[i] = 0

	for i in range(vertices - 2):
		vertex_set[prufer[i] - 1] += 1

	for i in range(vertices - 2):
		for j in range(vertices):
			if (vertex_set[j] == 0):
				vertex_set[j] = -1

				g.addEdge(j+1, prufer[i])

				graph_print = graph_print+f"{j+1} {prufer[i]}\n"
				vertex_set[prufer[i] - 1] = vertex_set[prufer[i] - 1] - 1
				break

	j = 0
	head = -1
	for i in range(vertices):
		if (vertex_set[i] == 0 and j == 0):
			head = i+1
			j += 1
		elif (vertex_set[i] == 0 and j == 1):
			g.addEdge(head, i+1)
			graph_print = graph_print+f"{head} {i+1}\n"
			break
	
	return g, graph_print


def GenerateConnectedGraph(seed, n, m):
	g = Graph(n)

	# Genero un albero con le dimensioni date
	length = n - 2
	arr = [0] * length

	for i in range(length):
		arr[i] = random.randint(0, length + 1) + 1

	g, graph_print = generateTreeEdges(arr, length, g)

	# Aggiungo casualmente archi fino ad arrivare a m

	# TODO usa g.listNotConnectedEdges() e a caso metti m -1 elem

	return g, graph_print

def GenerateGraph(seed, n, m, is_connected):
	if seed == "lazy":
		shake = random.randrange(10000,80000)
	else:
		shake = seed

	random.seed(int(shake))
	if(is_connected): # Genero grafo connesso
		g, graph_print = GenerateConnectedGraph(n, m) # TODO: controlla se random chiamato esternamente funziona
	else: # Genero grafo NON connesso
		# TODO
		pass
	return g, graph_print

'''
n=6
m=10
grafo,gp = GenerateConnectedGraph("lazy", n, m)
print(gp)

list_nc = grafo.listNotConnectedEdges()

for elem in list_nc:
	print(elem)
'''