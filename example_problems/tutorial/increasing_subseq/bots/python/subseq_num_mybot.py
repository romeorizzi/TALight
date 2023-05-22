#!/usr/bin/python
from sys import stderr, exit, argv

def count_occurences(T, S):
    m = len(T) #T
    n = len(S) #S

    lookup = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(n + 1):
        lookup[0][i] = 0

    for i in range(m + 1):
        lookup[i][0] = 1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if T[i - 1] == S[j - 1]:
                lookup[i][j] = lookup[i - 1][j - 1] + lookup[i - 1][j]
            else:
                lookup[i][j] = lookup[i - 1][j]

    return lookup[m][n]


while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    T = spoon.split()
    T = list(map(int, T))

    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    S = spoon.split()
    S = list(map(int, S))

    
    count = count_occurences(T, S)
   
    print(count)

exit(0)