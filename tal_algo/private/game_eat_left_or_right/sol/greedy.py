#!/usr/bin/env python3
from sys import stderr

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        #print(f"testcase {t}", file=stderr)
        n = int(input())
        V = list(map(int, input().split()))
        me_to_move = True # preferisco giocare per primo
        print(1, flush=True)
        i, j = 0, n
        while i < j:
            if me_to_move:
                if V[i] > V[j - 1]:
                    print("L", flush=True)
                    i += 1
                else:
                    print("R", flush=True)
                    j -= 1
            else:
                if input().strip() == "L":
                    i += 1
                else:
                    j -= 1
            me_to_move = not me_to_move
