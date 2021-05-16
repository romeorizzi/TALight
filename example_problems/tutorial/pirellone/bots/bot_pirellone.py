#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 21:18:54 2021

@author: aurora
"""
from sys import argv
def solution(sr,sc,a):
    lista=[]
    src = [1-x for x in sr]
    scc = [1-x for x in sc]
    if a:
        
    
    
    
    
    
    
    
    
    if sc[0] and sr[0]:
        if a==1 and sc[1] and sr[1]:
            sc=[ 1-val for val in sc]
        if a==0 and sc[1]:
            sc=[ 1-val for val in sc]
        if a==0 and sr[1]:
            sr=[ 1-val for val in sr]

            
    
    print(f"#{sr},{sc}")    
    for i in range(len(sr)):
        if sr[i]:
            lista.append(f"r{i+1}")
    for j in range(len(sc)):
        if sc[j]:
            lista.append(f"c{j+1}")
    return lista

def num_sol_bot():
    sr=[]
    sc=[]
    while True:
        tmp = input()
        if tmp[0] != '#':
            tmp=tmp.split()
            m=int(tmp[0])
            n=int(tmp[1])
            print('? 2 2')
            a=int(input())
            for j in range(n):
                print(f'? 1 {j+1}')
                tmp = input()
                tmp=int(tmp)
                sc.append(tmp)
            for i in range(m):
                print(f'? {i+1} 1')
                tmp = input()
                tmp=int(tmp)
                sr.append(tmp)
            print(f"#{sr},{sc},{a}")
            print(" ".join(solution(sr,sc,a)))
            sr.clear()
            sc.clear()
        
            
            
if argv[1] == 'prova':
    num_sol_bot()