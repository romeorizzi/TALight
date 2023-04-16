#!/usr/bin/env python3
from sys import stderr

from triangolo_lib import game_val, display_triangle

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        chooser = list(map(int,input().strip().split()))
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr, stderr)
        #print(game_val(Tr), chooser, file=stderr)
        print(game_val(Tr, chooser))
