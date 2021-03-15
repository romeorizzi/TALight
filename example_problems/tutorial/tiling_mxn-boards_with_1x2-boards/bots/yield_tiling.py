#!/usr/bin/python3

m,n = map(int,input().split())
grid=[ ["X" for j in range(n) ] for i in range(m) ]

if n%2 == 0:
  for i in range(m): #for every raw (deal each raw separately)
    for j in range(0,n,2):
        grid[i][j] = "W"
        grid[i][j+1] = "E"
elif m%2 == 0:
  for j in range(n): #for every column (split the problem into separate columns)
    for i in range(0,m,2): 
        grid[i][j] = "N"
        grid[i+1][j] = "S"      

print(m,n)
if m*n % 2 == 0:
   for i in range(m):
      for j in range(n):
         print(grid[i][j],end="")
      print()
