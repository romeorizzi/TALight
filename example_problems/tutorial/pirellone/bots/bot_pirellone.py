#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 21:18:54 2021

@author: aurora
"""
from sys import argv
def solution(sr,sc):
    lista=[]
    for i in sr:
        lista.append(f"r{i+1}")
    for j in sc:
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
            for j in range(n):
                print(f'? 1 {j+1} ')
                tmp = input()
                tmp=int(tmp)
                sc.append(tmp)
            for i in range(m):
                print(f'? {i+1} 1')
                tmp = input()
                tmp=int(tmp)
                sr.append(tmp)
            print(" ".join(solution(sr,sc)))
        
            
            
if argv[1] == 'prova':
    num_sol_bot()