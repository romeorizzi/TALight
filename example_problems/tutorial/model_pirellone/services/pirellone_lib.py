#!/usr/bin/env python3
import random
import re
from sys import exit



####DA SISTEMARE TUTTI I CHECK OFF LIGHTS 


def gen_pirellone(m, n, seed=0, solvable=None, with_yes_certificate=False):
    """we reserve those seed divisible by 3 to the NOT solvable instances"""
    assert m >= 0
    assert n >= 0
    # Generate suitable seed if necessary
    if seed == 0:
        random.seed()
        seed = random.randint(100002,999999)
        # adust seed if not suitable
        if solvable == (seed%3 == 0):
            if solvable:
               seed -= random.randrange(1,3)   
            else:
               seed -= seed%3     
    else:
        solvable = (seed%3 != 0)
    # Generate pirellone
    random.seed(seed)
    switches_row = [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    pirellone = [ [ (switches_col[j] + switches_row[i]) % 2 for j in range(n) ] for i in range(m)]
    if not solvable:
        if m < 2 or n < 2:
            raise RuntimeError()
        num_altered_rows = random.randrange(1, m)
        altered_rows= random.sample(range(m), num_altered_rows)
        for row in altered_rows:
            col = random.randrange(0, n)
            pirellone[row][col] = 1-pirellone[row][col] 
    if with_yes_certificate:
        return pirellone, seed, switches_row, switches_col
    else:
        return pirellone, seed


def extract_sol(line, m, n, LANG, TAc):
    matched = re.match("^((\n*(r|c)[1-9][0-9]{0,3})*\n*)$", line)
    if not bool(matched):
        TAc.print(LANG.render_feedback("wrong-sol-line",f'# Error! The line with your solution ({line}) is not accordant (it does not match the regular expression "^((\n*(r|c)[1-9][0-9]{0,3})*\n*)$"'), "red", ["bold"])
        exit(0)
    switch_rows = [0]*m
    switch_cols = [0]*n
    moves = line.split()
    for move,i in zip(moves,len(moves)):
        index = int(move[1:])
        if move[0] == "r":
            if index > m:
                TAc.print(LANG.render_feedback("row-index-exceeds-m",f'# Error! In your solution line ({line}) the {i}-th move ({move}) is not applicable. Indeed, {index}>{m}=m.'), "red", ["bold"])
                exit(0)
            switch_rows[index] = 1-switch_rows[index]
        if move[0] == "c":
            if index > n:
                TAc.print(LANG.render_feedback("column-index-exceeds-n",f'# Error! In your solution line ({line}) the {i}-th move ({move}) is not applicable. Indeed, {index}>{n}=n.'), "red", ["bold"])
                exit(0)
            switch_cols[index] = 1-switch_cols[index]
    return switch_rows, switch_cols


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


def check_off_lights(pirellone,solu, LANG, TAc):
    pirellone1=[line[:] for line in pirellone]
    m=len(pirellone)
    n=len(pirellone[0])
    empty=[[0 for j in range(0,len(pirellone[0]))] for i in range(0,len(pirellone))]
    for i in range(0,len(solu)):
        if solu[i][0]=='r':
            if int(solu[i][1:]) > m:
                TAc.print(LANG.render_feedback("row-index-exceeds-m",f'# Error! In your solution the move ({solu[i]}) is not applicable. Indeed, {int(solu[i][1:])}>{m}.'), "red", ["bold"])
                exit(0)
            switch_row(int(solu[i][1:])-1,pirellone)
        elif solu[i][0]=='c':
            if int(solu[i][1:]) > n:
                TAc.print(LANG.render_feedback("col-index-exceeds-n",f'# Error! In your solution the move ({solu[i]}) is not applicable. Indeed, {int(solu[i][1:])}>{n}.'), "red", ["bold"])
                exit(0)
            switch_col(int(solu[i][1:])-1,pirellone)
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


def solution_pad(sol,m,n,lb,seed="random_seed"):
    if type(seed)==str:
        assert seed=="random_seed"
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
    
