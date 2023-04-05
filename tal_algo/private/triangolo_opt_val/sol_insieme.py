#!/usr/bin/env python3
from sys import stderr

def display_triangle(Tr):
    n = len(Tr)
    for i in range(n):
        print(" ".join(map(str,Tr[i])))


def max_val(Tr):
    """L'idea è di considerare una famiglia di sottoproblemi S, uno per ogni elemento del triangolo in input fornito come una coppia (riga,colonna).
       Per ogni r in [0,n) e c in [0,r] vorremmo che:
          S[r][c] = il massimo valore di un cammino a scendere dall'elemento (r,c)."""
    #display_triangle(Tr)
    n = len(Tr)
    S = []
    print(f"{n=}",file=stderr)
    for r in range(n):
        S.append([None] * (r+1))
    for c in range(n):
        S[n-1][c] = Tr[n-1][c]
    for r in reversed(range(0,n-1)):
        for c in range(r+1):
            print(f"{r=}, {c=}",file=stderr)
            S[r][c] = Tr[r][c] + max(S[r+1][c],S[r+1][c+1])
    return S[0][0]

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr)
        print(max_val(Tr))
