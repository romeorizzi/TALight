#!/usr/bin/env python3
from sys import argv, stdout, stderr
MAX_N_PAIRS = 1000

num_wffs = [1] * (MAX_N_PAIRS+1)

for n in range(2,MAX_N_PAIRS+1):
    for n_pairs_included in range(n):
        num_wffs[n] = num_wffs[n-1] + num_wffs[n-2] 

def num_sol(n):
    assert n <= MAX_N_PAIRS
    return num_wffs[n]

def unrank(n):
    if num_sol(n)==1:
        return ['[]']
    if num_sol(n)==2:
        return ['[][]', '[--]']
    solu1=[]
    solu2=[]
    for i in range(num_sol(n-1)):
        solu1.append('[]' + unrank(n-1)[i])
    for j in range(num_sol(n-2)):
        solu2.append('[--]' + unrank(n-2)[j])
    return solu1 + solu2
    
def next_wff(wff, sorting_criterion):
    if wff == "":
        return 0
    n_tiles = len(wff) // 2
    ord_list=unrank(n_tiles)
    if sorting_criterion=='loves_short_tiles':
        pos=ord_list.index(wff)
        solu=ord_list[pos+1]
    elif sorting_criterion=='loves_long_tiles':
        new=ord_list[::-1]
        pos=new.index(wff)
        solu=new[pos+1]
    return solu

def num_sol_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            print(num_sol(int(tmp)))

# def unrank_bot():
#     while True:
#         tmp = input()
#         if len(tmp) == 0 or tmp[0] != '#':
#             n, r = map(int, tmp.split())
#             print(unrank(n, r))

# def rank_bot():
#     while True:
#         tmp = input()
#         if len(tmp) == 0 or tmp[0] != '#':
#             print(rank(tmp))

def next_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            wft, r = map(str, tmp.split())
            print(next_wff(wft,r))

if argv[1] == 'num_sol':
    num_sol_bot()
# if argv[1] == 'rank':
#     rank_bot()
# if argv[1] == 'unrank':
#     unrank_bot()
if argv[1] == 'next':
    next_bot()