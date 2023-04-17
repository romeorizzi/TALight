#!/usr/bin/env python3
from sys import stderr

def display_triangle(Tr, out=stderr):
    for i in range(n):
        print(" ".join(map(str, Tr[i])), file=out)


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        #print(f"testcase {t}", file=stderr)
        n = int(input())
        Tr = []
        for i in range(n):
            Tr.append(list(map(int, input().strip().split())))
        #display_triangle(Tr, stderr)
        for r in reversed(range(n-1)):
             for c in range(r+1):
                  Tr[r][c] += max(Tr[r+1][c], Tr[r+1][c+1])
        print(Tr[0][0])
        opt_sol = ""; r = 0; c = 0
        while r+1 < n:
            if Tr[r+1][c] >= Tr[r+1][c+1]:
                opt_sol += "L"; r += 1
            else:
                opt_sol += "R"; r += 1; c += 1
        print(opt_sol)
