#!/usr/bin/env python3
from sys import stdout, stderr

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        m, n = map(int, input().strip().split())
        print(f"Testcase {t}: {m=}, {n=}", file=stderr)
        
        winning_move = [ [None] * (n + 1) for _ in range(m + 1) ]
        winning_move.append([None] + ([(1, 1)] * n) )
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                for ii in range(1, i):
                    if winning_move[ii][j] is None:
                        winning_move[i][j] = (ii, j)
                        continue
                for jj in range(1, j):
                    if winning_move[i][jj] is None:
                        winning_move[i][j] = (i, jj)
                        continue
 
        if winning_move[m][n] is None:
            me_to_move = 2 # preferisco giocare per secondo
        else:
            me_to_move = 1 # preferisco giocare per primo
        print(me_to_move, flush=True)
        while m + n > 2:
            if me_to_move == 2:
                m, n = map(int, input().strip().split())
            else:
                m, n = winning_move[m][n]
                print(f"{m} {n}", flush=True)
            me_to_move = 3 - me_to_move
