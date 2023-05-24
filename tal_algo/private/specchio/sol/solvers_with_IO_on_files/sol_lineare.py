#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""
 *  File: sol_lineare.py
 *  Soluzione in python per specchio
 *  Romeo Rizzi, 2022-05-25
"""

fin = open("input.txt","r")
input_tree = list(map(int,fin.readline().split()))
mirrored_tree_reversed = []

def reverso_write_mirrored_tree():
  n_figli = input_tree.pop(0)
  for _ in range(n_figli):
    reverso_write_mirrored_tree()
  mirrored_tree_reversed.append(n_figli)

reverso_write_mirrored_tree()

with open("output.txt","w") as fout:
    print(" ".join(map(str,reversed(mirrored_tree_reversed))), file=fout)
