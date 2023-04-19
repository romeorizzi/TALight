#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""  sometimes it answers correct but, on other testcases, picked up at random, it just echoes the tree received in input """
from sys import stderr
import random

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
  dado = random.randint(0,3)
  if dado == 0:
    print(" ".join(map(str,input_tree)))
  else:
    print(" ".join(map(str,reversed(mirrored_tree_reversed))))
