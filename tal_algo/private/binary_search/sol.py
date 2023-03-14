#!/usr/bin/env python3

from sys import stderr

def my_input():
    got = ''
    while len(got)==0 or got[0]=='#':
        got = input()
    return got
    

if __name__ == "__main__":
    T = int(my_input())
    for t in range(T):
        N = int(my_input())
        q = 0
        lo, hi = 1, N+1
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            q += 1
            print("?", mid, flush=True)
            ans = my_input()
            assert ans in {'<','>','='}
            if ans == '>':
                lo = mid+1
            elif ans == '<':
                hi = mid
            else:
                hi = mid
        print("!", lo, flush=True)
        print(f"Case #{t+1:03} q:", q, file=stderr)
