#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:55:02 2021

@author: Aurora Rossi
"""
import random
def rand_bit():
    k=random.randrange(3,15)
    n=[]
    for i in range(k):
        h=random.randrange(0,2)
        n.append(h)
    j=0
    while n[j]==0:
        n.pop(j)
    if len(n)==0:
        n=1010100
    return n
        


def dec_to_bin(n):
    'da decimale a binario'
    b=0
    i=0
    while n>0:
        if n%2==0:
            b+=0*(10**i)
        else:
            b+=1*(10**i)
        i+=1   
        n=int(n/2)
    return b


def count1(n):
    'conta quanti 1 ci sono restituisce se sono pari'
    j=0
    s=0
    for i in range(0,len(n)):
        if (n[i])==1:
            j=j+1
    if j%2==0:
        s=0
    else:
        s=1
    return s

def mossa1(n):
    if n[len(n)-1]==1:
        n[len(n)-1]=0
    else:
       n[len(n)-1]=1
    return n

def mossa2(n):
    i=len(n)-1
    while n[i]!=1:
        i-=1
    if n[i]==1:
        if n[i-1]==1:
                n[i-1]=0
        else:
                n[i-1]=1
                
    return n

def controllo(n):
    a=True 
    for i in range(0,len(n)):
        if n[i]==1:
            a=False
    return a

def num_mosse(n):
    u=0
    d=0
    while controllo(n)==False:
        if count1(n)==0:
            mossa2(n)
            u+=1
        else:
            mossa1(n)
            d+=1
    return (u+d)


def mossa(n):
    if len(n)==1 and n[0]==0:
        return 0
    if count1(n)==0:
        return 2
    else:
        return 1
