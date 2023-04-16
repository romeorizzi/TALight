#!/usr/bin/env python3
from sys import stderr
from random import randrange

from triangolo_lib import max_val, unrank_safe, display_triangle

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n,rnk = map(int,input().strip().split())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int,input().strip().split())))
        #display_triangle(Tr,stderr)
        #print(max_val(Tr), file=stderr)
        #print(num_opt_sols(Tr), file=stderr)
        print(max_val(Tr))
        opt_path = unrank_safe(Tr,rnk)
        dice = randrange(0,6)
        if dice == 0:
            print(opt_path[:-1] + 'L')
        elif dice == 1:
            print(opt_path[:-1] + 'R')
        else:
            print(opt_path)
