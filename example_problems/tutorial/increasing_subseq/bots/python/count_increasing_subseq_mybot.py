#!/usr/bin/python
from sys import stderr, exit, argv

max_val = 100

def count_increasing_sub(arr, n):
    count = [0 for i in range(max_val+1)]

    for i in range(n):
        for j in range(arr[i] - 1, -1, -1):
            count[arr[i]] += count[j]

        count[arr[i]] += 1

    result = 0
    for i in range(max_val +1):
        result += count[i]

    return result

while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    T = spoon.split()
    T = list(map(int, T))

    n = len(T)
    count = count_increasing_sub(arr, n)
   
    print(count)

exit(0)
