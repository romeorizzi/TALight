#!/usr/bin/env python3
import random
import copy

def random_pirellone(m, n, seed="any", solvable=False, s=False):
    if seed=="any":
        random.seed()
        seed = random.randrange(0,1000000)
    else:
        seed = int(seed)
    random.seed(seed)
    switches_row = [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    pirellone = [ [ (switches_col[j] + switches_row[i]) % 2 for j in range(n) ] for i in range(m)]
    if not solvable:
        ar=[]
        ac=[]
        k=random.randrange(1, m+n)
        print(k)
        for _ in range(k):
            row = random.randrange(0, m)
            col = random.randrange(0, n)
            if row not in ar and col not in ac:
                pirellone[row][col] = 1-pirellone[row][col] 
    if s:
        return pirellone, seed, switches_row, switches_col
    else:
        return pirellone, seed

def switch_row(i,pirellone):
    for j in range(len(pirellone[0])):
        pirellone[i][j] = int(not pirellone[i][j])

def switch_col(j,pirellone):
    for i in range(len(pirellone)):
        pirellone[i][j] = int(not pirellone[i][j])

def is_solvable(pirellone):
    for i in range(len(pirellone)):
        inv = pirellone[0][0] != pirellone[i][0]
        for j in range(len(pirellone[0])):
            v = not pirellone[i][j] if inv else pirellone[i][j]
            if v != pirellone[0][j]:
                return False
    return True 

def print_pirellone(pirellone):
    for l in pirellone:
        print(*l) 
        
def check_off_lights(pirellone,solu):
    pirellone1=copy.deepcopy(pirellone)
    empty=[[0 for j in range(0,len(pirellone[0]))] for i in range(0,len(pirellone))]
    for i in range(0,len(solu)):
        
        if solu[i][0]=='r':
            if len(solu[i])>2:
                switch_row(int(solu[i][1])*10+int(solu[i][2])-1,pirellone)
            else:
                switch_row(int(solu[i][1])-1,pirellone)
        elif solu[i][0]=='c':
            if len(solu[i])>2:
                switch_col(int(solu[i][1])*10+int(solu[i][2])-1,pirellone)
            else:
                switch_col(int(solu[i][1])-1,pirellone)
    if is_solvable(pirellone):             
        if empty==pirellone:
                return True,'s'
        else: 
                return False,'s'
    else:
        lights=0
        for i in range(len(pirellone)):
            lights+=sum(pirellone[i]) 
        if lights==(min_lights_on(pirellone1)):
            return True,'n'
        else:
            return False,'n'

def solution_min(switches_row,switches_col):
    m=len(switches_row)
    n=len(switches_col)
    num_one=sum(switches_col)+sum(switches_row)
    if num_one>m+n-num_one:
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    lista=[]
    for i in range(m):
        if switches_row[i]:
            lista.append(f"r{i+1}")
    for j in range(n):
        if switches_col[j]:
            lista.append(f"c{j+1}")
    return lista
        
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
        
#forse non corretta la seguente funzione            
def solution_irredundant(pirellone,switches_row,switches_col,smallest=True):
    m=len(switches_row)
    n=len(switches_col)
    assert is_solvable(pirellone)
    switches_row = pirellone[0]
    if pirellone[0][0] == 0:
        switches_col = pirellone[0]
    else:    
        switches_row = [ 1-pirellone[i][0] for i in range(m) ]
    if smallest != (sum(switches_col)+sum(switches_row) <= (m+n)//2):
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    
    [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    pirellone = [ [ (switches_col[j] + switches_row[i]) % 2 for j in range(n) ] for i in range(m)]

    lista=[]
    for i in range(m):
        if switches_row[i]:
            lista.append(f"r{i+1}")
    for j in range(n):
        if switches_col[j]:
            lista.append(f"c{j+1}")
    return lista

def solution_pad(sol,m,n,lb,seed="any"):
    if type(seed)==str:
        assert seed=="any"
        random.seed()
        seed = random.randrange(0,1000000)
    random.seed(seed)  
    longsol=sol
    while len(longsol)<lb:
        num=f"r{random.randint(1,m)}" 
        longsol.append(num)
        longsol.append(num)
        num=f"c{random.randint(1,n)}"
        longsol.append(num)
        longsol.append(num)      
    random.shuffle(longsol)
    return longsol



def min_lights_on(pirellone):
    s=0
    h=1
    k=1
    while h!=0 or k!=0:
        h=0
        k=0
        for i in range(len(pirellone)):
            if sum(pirellone[i])>(len(pirellone)-sum(pirellone[i])):
                switch_row(i,pirellone)
                h+=1      
        for j in range(len(pirellone[0])):
            for i in range(len(pirellone)):
                s+=pirellone[i][j]
            if s>(len(pirellone[0])-s):
                switch_col(j,pirellone)
                k+=1
            s=0   
    light=0
    for i in range(len(pirellone)):
        light+=sum(pirellone[i]) 
    return light
    
     

