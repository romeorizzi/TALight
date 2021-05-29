#!/usr/bin/env python3
  
from collections import defaultdict 
import random

def zcon(W, wt, val, n):
    K = [[0 for w in range(W + 1)]
            for i in range(n + 1)]
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1]+ K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]
    res = K[n][W]
    print(res)
    w = W
    arr=[]
    s=""
    for i in range(0,n,1):
        arr.append(0)

    for i in range(n,0,-1):
        if res <= 0:
            break
        if res == K[i - 1][w]:
            continue
        else:
            pos = wt.index(wt[i-1])
            arr[pos]=1
            res = res - val[i - 1]
            w = w - wt[i - 1]
    s = " ".join([str(_) for _ in arr])
    return s


def zopt(W, wt, val, n):
    if n == 0 or W == 0:
        return 0
    if (wt[n-1] > W):
        return zopt(W, wt, val, n-1)
    else:
        return max(val[n-1] + zopt(W-wt[n-1], wt, val, n-1),zopt(W, wt, val, n-1))
 

def zdec(W, wt, val, n, target):
    opt = zopt(W, wt, val, n)
    if opt >= target:
        return True
    else:
        return False
    


# generazione istanze

def GenZdec(size, seed):
    if seed == "random_seed":
        a = random.randrange(1000,8000)
        random.seed(a)
    if seed != "random_seed":
        a = seed
        random.seed(int(seed))

    if size == "small":
        n = random.randrange(5,10)
        W = random.randrange(100,150)
        target = random.randrange(700,800)
        wt = ""
        val = ""
        for i in range(n):
            if i == n-1:
                weight = random.randrange(1,60)
                value = random.randrange(100,450)
                wt = wt+f"{weight}"
                val = val+f"{value}"
            else:
                weight = random.randrange(1,60)
                value = random.randrange(100,450)
                wt = wt+f"{weight},"
                val = val+f"{value},"               
        return a, W, wt, val, n, target 
    if size == "large":
        n = random.randrange(50,100)
        W = random.randrange(1000,1500)
        target = random.randrange(7000,8000)
        wt = ""
        val = ""
        for i in range(n):
            if i == n-1:
                weight = random.randrange(100,600)
                value = random.randrange(1000,4500)
                wt = wt+f"{weight}"
                val = val+f"{value}"
            else:
                weight = random.randrange(100,600)
                value = random.randrange(1000,4500)
                wt = wt+f"{weight},"
                val = val+f"{value},"               
        return a, W, wt, val, n, target


def GenZopt(size, seed):
    if seed == "random_seed":
        a = random.randrange(1000,8000)
        random.seed(a)
    if seed != "random_seed":
        a = seed
        random.seed(int(seed))

    if size == "small":
        n = random.randrange(5,10)
        W = random.randrange(100,150)
        wt = ""
        val = ""
        for i in range(n):
            if i == n-1:
                weight = random.randrange(1,60)
                value = random.randrange(100,450)
                wt = wt+f"{weight}"
                val = val+f"{value}"
            else:
                weight = random.randrange(1,60)
                value = random.randrange(100,450)
                wt = wt+f"{weight},"
                val = val+f"{value},"               
        return a, W, wt, val, n, target 
    if size == "large":
        n = random.randrange(50,100)
        W = random.randrange(1000,1500)
        wt = ""
        val = ""
        for i in range(n):
            if i == n-1:
                weight = random.randrange(100,600)
                value = random.randrange(1000,4500)
                wt = wt+f"{weight}"
                val = val+f"{value}"
            else:
                weight = random.randrange(100,600)
                value = random.randrange(1000,4500)
                wt = wt+f"{weight},"
                val = val+f"{value},"               
        return a, W, wt, val, n


def GenZcon(size, seed):
    if seed == "random_seed":
        a = random.randrange(1000,8000)
        random.seed(a)
    if seed != "random_seed":
        a = seed
        random.seed(int(seed))

    if size == "small":
        n = random.randrange(5,10)
        W = random.randrange(100,150)
        wt = ""
        val = ""
        for i in range(n):
            if i == n-1:
                weight = random.randrange(1,60)
                value = random.randrange(100,450)
                wt = wt+f"{weight}"
                val = val+f"{value}"
            else:
                weight = random.randrange(1,60)
                value = random.randrange(100,450)
                wt = wt+f"{weight},"
                val = val+f"{value},"               
        return a, W, wt, val, n, target 
    if size == "large":
        n = random.randrange(50,100)
        W = random.randrange(1000,1500)
        wt = ""
        val = ""
        for i in range(n):
            if i == n-1:
                weight = random.randrange(100,600)
                value = random.randrange(1000,4500)
                wt = wt+f"{weight}"
                val = val+f"{value}"
            else:
                weight = random.randrange(100,600)
                value = random.randrange(1000,4500)
                wt = wt+f"{weight},"
                val = val+f"{value},"               
        return a, W, wt, val, n

