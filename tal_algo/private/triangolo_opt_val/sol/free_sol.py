#!/usr/bin/env python3
from sys import stderr

from triangolo_lib import max_val, display_triangle

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr,stderr)
        #print(max_val(Tr),file=stderr)
        print(max_val(Tr))
