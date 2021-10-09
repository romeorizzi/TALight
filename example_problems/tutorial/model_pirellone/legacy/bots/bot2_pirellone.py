#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 21:18:54 2021

@author: aurora
"""
from sys import argv
    
def switch_row(i,pirellone):
    for j in range(len(pirellone[0])):
        pirellone[i][j] = int(not pirellone[i][j])

def switch_col(j,pirellone):
    for i in range(len(pirellone)):
        pirellone[i][j] = int(not pirellone[i][j])
        
        
def solution(pirellone):
    m=len(pirellone)
    n=len(pirellone[0]) 
    sr=[]
    sc=[]
    for j in range(n):
        if pirellone[0][j]:
            sc.append(j)
            switch_col(j,pirellone)
    for i in range(1,m):
        if pirellone[i][0]:
            sr.append(i)
            switch_row(i,pirellone)
    if len(sr)+len(sc)>= (m+n)//2:
        switches_row=[]
        switches_col=[]
        for j in range(n):
            if j not in sc:
                switches_col.append(j)
        for i in range(m):
            if i not in sr:
                switches_row.append(i)
    else:
        switches_row=sr
        switches_col=sc
    lista=[]
    for i in switches_row:
        lista.append(f"r{i+1}")
    for j in switches_col:
        lista.append(f"c{j+1}")
    return lista

def num_sol_bot():
    sr=[]
    pirellone=[]
    while True:
        tmp = input()
        if tmp[0] != '#':
            tmp=tmp.split()
            m=int(tmp[0])
            n=int(tmp[1])
            for i in range(m):
                for j in range(n):
                    print(f'? {i+1} {j+1}')
                    tmp = input()
                    tmp=int(tmp)
                    sr.append(tmp)
                pirellone.append(sr[:])
                sr.clear()
            print(f'#')    
            print(" ".join(solution(pirellone)))
            
            pirellone.clear()
        
            
            
if argv[1] == 'prova':
    num_sol_bot()