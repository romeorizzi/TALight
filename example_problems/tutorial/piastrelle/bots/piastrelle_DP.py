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

def rank(wff,sorting_criterion):
    count=len(wff)//2
    if count==0 or count==1:
        return 1
    pos=1
    a=0
    while pos<len(wff):
        if wff[pos]==']':
            pos+=2
            count-=1
        else:
            a+=num_sol(count-1)
            pos+=4
            count-=2
    if sorting_criterion=='loves_short_tiles':
        return a+1
    elif sorting_criterion=='loves_long_tiles':
        return num_sol(len(wff)//2)-a

def unrank(n_tiles,pos,sorting_criterion):
    assert pos>0 and pos<=num_sol(n_tiles), 'the position must be between 1 and '+str(num_sol(n_tiles))
    if n_tiles==0:
        return '-'
    if n_tiles==1:
        return '[]'
    if sorting_criterion=='loves_long_tiles':
        pos=num_sol(n_tiles)-pos+1
    count=n_tiles
    solu=''
    while count>1:
        if pos<=num_sol(count-1):
            solu+='[]'
            count-=1
        else:
            solu+='[--]'
            pos-=num_sol(count-1)
            count-=2
    if count%2==1:
        solu+='[]'
    return solu
    
def lista(n_tiles, sort_crit):
    solu=[]
    for i in range (1,num_sol(int(n_tiles))+1):
        solu.append(unrank(int(n_tiles),i,sort_crit))
    return solu

def next_wff(wff, sorting_criterion):
    n_tiles = len(wff)//2
    r = rank(wff,sorting_criterion)
    return unrank(n_tiles,r+1,sorting_criterion)
        
def num_sol_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            print(num_sol(int(tmp)))

def unrank_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            #print('tmp ',tmp.split())
            n, r, crit = map(str, tmp.split())
            print(unrank(int(n), int(r),crit))

def rank_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            wft, r = map(str, tmp.split())
            print(rank(wft,r))

def next_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            wft, r = map(str, tmp.split())
            print(next_wff(wft,r))

def list_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            n_tiles, sort_crit = map(str, tmp.split())
            print(' , '.join(lista(n_tiles, sort_crit)))

usage=f"""I am a general (non efficient) purpouse bot with the following functionalities:
  1. num_sol
  2. rank
  3. unrank
  4. next
  5. list
You should call me as follows:
$ {argv[0]} <evalution service>
"""

if len(argv) != 2:
    print(f"WARNING from bot {argv[0]}: called with the wrong number of parameters.")
    print(usage)
    exit(1)
if argv[1] == 'num_sol':
    num_sol_bot()
if argv[1] == 'rank':
    rank_bot()
if argv[1] == 'unrank':
    unrank_bot()
if argv[1] == 'next':
    next_bot()
if argv[1] == 'list':
    list_bot()