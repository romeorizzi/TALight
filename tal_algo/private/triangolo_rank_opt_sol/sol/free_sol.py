#!/usr/bin/env python3
from sys import stderr

from triangolo_lib import max_val, num_opt_sols, rank_safe, display_triangle

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        opt_path_given = input().strip()
        Tr = []
        for i in range(n):
            Tr.append(list(map(int, input().strip().split())))
        #display_triangle(Tr, stderr)
        #print(max_val(Tr), file=stderr)
        #print(f"{opt_path_given=}", file=stderr)
        print(max_val(Tr))
        print(num_opt_sols(Tr))
        print(rank_safe(Tr, opt_path_given))
