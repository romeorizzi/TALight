#!/usr/bin/env python3
# LIBRARY: rand_trees.py   last change: 19-04-2023   author: Romeo Rizzi

from sys import stderr
import random

def random_tree(minn: int, maxn: int, degree_at_most_2: bool):
  def randomParenth(a: int, b: int, degree_at_most_2):
    nonlocal s
    if a >= b:
        return
    assert (a-b) % 2 == 1
    s[a] = '(';  s[b] = ')'
    dist_mate_of_a_from_b = 2*random.randint(0, (b-a)//2)
    if dist_mate_of_a_from_b == 0:
      randomParenth(a+1, b-1, degree_at_most_2)
    else:
      c = b - dist_mate_of_a_from_b
      s[c] = ')'
      s[c+1] = '('
      randomParenth(a+1, c-1, degree_at_most_2)
      if degree_at_most_2:
        randomParenth(c+2,b-1, degree_at_most_2)
      else:
        randomParenth(c+1, b, degree_at_most_2)

  def encodeRootedTree(root_left: int, posW: int):
    nonlocal tree
    nonlocal s
    #print(f"{root_left=}, {posW=}")
    num_children = 0; root_right = 1 + root_left
    while s[root_right] == '(':
      num_children += 1
      root_right = 1 + encodeRootedTree(root_right, posW + (root_right-root_left +1)//2)
    tree[posW] = num_children
    return root_right


  n = random.randint(minn, maxn)
  s = [None] * (2*n)
  tree = [None] * n
  randomParenth(0, 2*n-3, degree_at_most_2)
  root_right = encodeRootedTree(0, 1)
  num_children = 1
  while root_right < 2*n-3:
    num_children += 1
    root_right = encodeRootedTree(root_right +1, 1+(root_right+1)//2)
  tree[0] = num_children
  return [tree[i] for i in range(n)]

def random_tree_any_degree(minn: int, maxn: int):
  return  random_tree(minn, maxn, degree_at_most_2 = False)

def random_tree_at_most_2_children(minn: int, maxn: int):
  return  random_tree(minn, maxn, degree_at_most_2 = True)

def random_binary_tree(minn: int, maxn: int):
  tree = random_tree(minn, maxn, degree_at_most_2 = True)
  pruned_tree = [x for x in tree if x != 1]
  return [2, 0] * ((len(tree) - len(pruned_tree))//2) + pruned_tree 


def print_tree_edges(prufer, m):
	vertices = m + 2
	vertex_set = [0] * vertices

	# Initialize the array of vertices
	for i in range(vertices):
		vertex_set[i] = 0

	# Number of occurrences of vertex in code
	for i in range(vertices - 2):
		vertex_set[prufer[i] - 1] += 1

	print("\nThe edge set E(G) is:")

	j = 0

	# Find the smallest label not present in prufer[].
	for i in range(vertices - 2):
		for j in range(vertices):
			# If j+1 is not present in prufer set
			if vertex_set[j] == 0:
				# Remove from Prufer set and print pair.
				vertex_set[j] = -1
				print("({}, {})".format(j + 1, prufer[i]), end=" ")

				vertex_set[prufer[i] - 1] -= 1

				break

	j = 0

	# For the last element
	for i in range(vertices):
		if vertex_set[i] == 0 and j == 0:
			print("({}, ".format(i + 1), end="")
			j += 1
		elif vertex_set[i] == 0 and j == 1:
			print("{})".format(i + 1))

def generate_random_free_labeled_tree(n):
  # complexity O(n^2), optimal since we need \Omega(n^2) random bits
	length = n - 2
	arr = [0] * length

	# Generate random array
	for i in range(length):
		arr[i] = random.randint(1, length + 1)

	print_tree_edges(arr, length)


if __name__ == "__main__":
  N = int(input("N = "))
  print(f"{random_tree_any_degree(N)=}")
  print(f"{random_tree_at_most_2_children(N)=}")
  print(f"{random_binary_tree(N)=}")

  generate_random_free_labeled_tree(n)
