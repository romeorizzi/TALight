#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""
 *  File: sol_lineare.py
 *  Soluzione in python per specchio
 *  Romeo Rizzi, 2022-05-25
"""
from sys import stderr, setrecursionlimit
setrecursionlimit(100000)

T = int(input())
for _ in range(T):
  input_tree = list(map(int, input().split()))
  #print(f"got {input_tree=}", file=stderr)
  pos_Read = 0
  mirrored_tree_reversed = []

  def reverso_write_mirrored_tree():
    global pos_Read
    n_figli = input_tree[pos_Read]
    pos_Read += 1
    for _ in range(n_figli):
      reverso_write_mirrored_tree()
    mirrored_tree_reversed.append(n_figli)

  reverso_write_mirrored_tree()
  print(" ".join(map(str,reversed(mirrored_tree_reversed))))
  #print("printed: " + " ".join(map(str,reversed(mirrored_tree_reversed))), file = stderr)
