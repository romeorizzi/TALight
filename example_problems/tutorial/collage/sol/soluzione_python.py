#!/usr/bin/env python3
import sys
from sys import setrecursionlimit, argv, exit, stderr
import os
setrecursionlimit(10**8)

#traduzione soluzione luca, ma senza doppioni
NMAX=1000

m = [[0 for __ in range(NMAX)] for _ in range(NMAX)]
col = [0 for _ in range(NMAX)]

if __name__ == "__main__":
  fIn = open("input.txt").readlines()
  fOut = open("output.txt", "w")
  n = [int(x) for x in fIn[0].split()]
  n = n[0]
  #print(n)
  old = 256
  j = 0
  second = [int(x) for x in fIn[1].split()]
  for i in range(n):
    k = second[i]
    #print(k)
    if ( k != old ):
      col[j] = k
      m[0][j] = 1
      j = j + 1
      old = k
  n = j
  for i in range(1, n):
    for j in range(n - i):
      minimo=int(sys.maxsize)
      for k in range(1, i + 1):
        if col[j]==col[j+i]:
          temp = 1
        else:
          temp = 0
        a = m[k-1][j] + m[i-k][j+k] - temp
        minimo = min(a , minimo)
        m[i][j] = minimo
  fOut.write(str(m[n-1][0]))
