#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 21:18:54 2021

@author: aurora
"""
from sys import argv
def solution_speed(sr,sc,a):
    lista=[]
    b=sr[0]
    if sc[0] and sr[0]:
        if a==1 and sc[1] and sr[1]:
            sc=[ 1-val for val in sc]
        if a==0 and sc[1]:
            sc=[ 1-val for val in sc]
        if a==0 and sr[1]:
            sr=[ 1-val for val in sr]
        if b==0 and sr[0]:
            sr=[ 1-val for val in sr]
        if b==0 and sc[0]:
            sc=[ 1-val for val in sc]
    if sc[0] and sr[0]:
        if b:
            sr=[ 1-val for val in sr]
 
    for i in range(len(sr)):
        if sr[i]:
            lista.append(f"r{i+1}")
    for j in range(len(sc)):
        if sc[j]:
            lista.append(f"c{j+1}")
    return lista

def num_sol_bot_speed():
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
            print(" ".join(solution_speed(sr,sc,a)))
            sr.clear()
            sc.clear()
            

    
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
        
            
        
            
            
if argv[1] == 'speed':
    num_sol_bot_speed()
else:
     num_sol_bot()
    