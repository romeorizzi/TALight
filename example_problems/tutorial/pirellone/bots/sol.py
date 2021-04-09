#!/usr/bin/env python3
from sys import argv, stdout, stderr
import copy
def switch_row(i,pirellone):
    for j in range(len(pirellone[0])):
        pirellone[i][j] = int(not pirellone[i][j])
    return

def switch_col(j,pirellone):
    for i in range(len(pirellone)):
        pirellone[i][j] = int(not pirellone[i][j])
    return


def is_solvable(pirellone, n, m):
    for i in range(n):
        inv = pirellone[0][0] != pirellone[i][0]
        for j in range(m):
            v = not pirellone[i][j] if inv else pirellone[i][j]
            if v != pirellone[0][j]:
                return False
    return True 

def soluzione_min(pirellone,m,n):
    pirellone1=copy.deepcopy(pirellone)
    if is_solvable(pirellone, m, n):
        R1=[0]*len(pirellone)
        C1=[0]*len(pirellone[0])
        R2=[0]*len(pirellone)
        C2=[0]*len(pirellone[0])
    for j in range(0,n):
        if pirellone1[0][j]:
            C1[j] = 1
            switch_col(j,pirellone1)
    for i in range(0,m):
         if pirellone1[i][0]:
            R1[i] = 1
            switch_row(i,pirellone1)
    pirellone2=copy.deepcopy(pirellone)
    
    for i in range(0,m):
        if pirellone2[i][0]:
            R2[i] = 1
            switch_row(i,pirellone2)
    for j in range(0,n):
        if pirellone2[0][j]:
            C2[j] = 1
            switch_col(j,pirellone2)
    lista=[]
    if (sum(R1)+sum(C1))<=(sum(R2)+sum(C2)):
        for i in range(m):
            if R1[i]:
                lista.append(f"r{i+1}")
        for j in range(n):
            if C1[j]:
                lista.append(f"c{j+1}")
    else:
        for i in range(m):
            if R2[i]:
                lista.append(f"r{i+1}")
        for j in range(n):
            if C2[j]:
                lista.append(f"c{j+1}")
    return lista

def my_soluzione(pirellone,n,m):
    lista=[]
    if is_solvable(pirellone, n, m):
        R=[0]*len(pirellone)
        C=[0]*len(pirellone[0])
        for i in range(0,n):    
            for j in range(0,m):
                if pirellone[i][j]:
                    C[j] = 1
                    switch_col(j,pirellone)
        for i in range(0,n):
             if pirellone[i][0]:
                R[i] = 1
                switch_row(i,pirellone)
    
        for i in range(n):
            if R[i]:
                lista.append(f"r{i+1}")
        for j in range(m):
            if C[j]:
                lista.append(f"c{j+1}")
    return lista


def num_sol_bot():
    pirellone=[]
    riga=[]
    while True:
        tmp = input()
        if tmp[0] != '#':
            for i in range(len(tmp)-1):
                if tmp[i]=='0' or tmp[i]=='1':
                    riga.append(int(tmp[i]))
                if tmp[i]==']':
                    pirellone.append(copy.deepcopy(riga))
                    riga.clear()
            print(soluzione_min(pirellone,len(pirellone),len(pirellone[0])))
            pirellone.clear()

if argv[1] == 'prova':
    num_sol_bot()

