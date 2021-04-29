#!/usr/bin/python
from sys import stderr, exit, argv


def min_decreasing_col(arr):
    n = len(arr)
    mdc = [1]*n
 
    for i in range (1 , n):
        for j in range(0 , i):
            if arr[i] > arr[j] and mdc[i]< mdc[j] + 1 :
                mdc[i] = mdc[j]+1
 
    return mdc


while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    T = spoon.split()
    T = list(map(int, T))


    mdc = min_decreasing_col(T)
    n_col = len(set(mdc))
   
    print(n_col)

exit(0)
