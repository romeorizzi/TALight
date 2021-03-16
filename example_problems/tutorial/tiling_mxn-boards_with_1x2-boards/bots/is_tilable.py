#!/usr/bin/python3

M=20
N=20

def is_tilable(m, n):
   return 1 - (m%2)*(n%2)

for i in range(1,M+1):
   for j in range(1,N+1):
      print(is_tilable(i, j),end="")
   print()

