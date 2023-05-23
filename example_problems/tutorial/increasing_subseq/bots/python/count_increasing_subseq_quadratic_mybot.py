#!/usr/bin/python
from sys import stderr, exit, argv

max_val = 100

def count_increasing_sub(T, n):
    countSub = [1 for i in range(n)]
    for i in range(1, n):
        for j in range(i):
            if T[i] > T[j]:
                countSub[i]+=countSub[j]

    result = 0
    for i in range(n):
        result+=countSub[i]

    return result


while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    T = spoon.split()
    T = list(map(int, T))

    n = len(T)
    count = count_increasing_sub(T, n)
   
    print(count)

exit(0)
