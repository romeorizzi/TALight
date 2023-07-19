#!/usr/bin/env python3

from sys import stderr

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        q = 1
        print("?", 0, n, flush=True)
        tot = int(input())
        # print(f"{n=}, {tot=}", file=stderr)
        lo, hi = 0, n + 1 - tot
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            q += 1
            # print(f"{lo=}, {hi=}, {q=}, {mid=}", file=stderr)
            print("?", 0, mid, flush=True)
            ans = int(input())
            # print(f"{q=}: (0,{mid=}) --> {ans=}", file=stderr)
            if ans == 0:
                lo = mid
            elif ans < tot:
                lo = mid - ans   # equivalently, (mid -1) - (ans -1)
                hi = lo + 1
            else:
               assert ans == tot, f"instead, {ans=}"
               hi = mid
        print("!", lo, tot, flush=True)
        print(f"Case #{t+1:03} q:", q, file=stderr)
