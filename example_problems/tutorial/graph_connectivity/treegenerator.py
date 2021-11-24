import sys
from random import seed, randint

def printTreeEdges(prufer,m):
	vertices = m + 2
	vertex_set = [0] * vertices

	for i in range(vertices):
		vertex_set[i] = 0

	for i in range(vertices - 2):
		vertex_set[prufer[i] - 1] += 1

	for i in range(vertices - 2):
		for j in range(vertices):
			if (vertex_set[j] == 0):
				vertex_set[j] = -1
				print(str((j+1)) + " " + str(prufer[i]))

				vertex_set[prufer[i] - 1] = vertex_set[prufer[i] - 1] - 1
				break

	j = 0
	for i in range(vertices):
		if (vertex_set[i] == 0 and j == 0):
			print((str((i+1)) + " "), end='')
			j += 1
		elif (vertex_set[i] == 0 and j == 1):
			print(str((i+1)) + "\n")


def generateRandomTree(n):
	length = n - 2
	arr = [0] * length

	for i in range(length):
		arr[i] = randint(0, length + 1) + 1

	printTreeEdges(arr, length)


n = 5
generateRandomTree(n)