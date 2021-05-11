#!/usr/bin/python
from sys import stderr, exit, argv

def get_position_from_subseq(subseq, all_subseq):
    index_subseq = []

    for i in all_subseq:
        if i:
            c,v = zip(*i)
            if subseq == list(c):
                index_subseq.append(list(v))

    return index_subseq

def sub_lists (l):
    empty = []  
    lists = [empty]
    for i in range(len(l)):
        orig = lists[:]
        new = (l[i],i)
        for j in range(len(lists)):
            lists[j] = lists[j] + [new]

        lists = orig + lists
    return lists

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

    
    l = sub_lists(T)
    index = get_position_from_subseq(S, l)  
    count = len(index) 
    print(count)

exit(0)