#!/usr/bin/env python3

# does 4*log2(n) queries

from sys import stderr

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())

        def f(start, end):
            if start + 1 == end:
                print("?", start, 1, flush=True)
                r = int(input())
                if r == 0:
                    return float("inf"), float("-inf"), 1
                else:
                    return start, start + 1, 1
            mid = (start + end) // 2
            print("?", start, end - start, flush=True)
            r = int(input())
            if r == 0:
                return float("inf"), float("-inf"), 1
            if r == end - start:
                return start, end, 1
            left = f(start, mid)
            right = f(mid, end)
            return (
                min(left[0], right[0]),
                max(left[1], right[1]),
                left[2] + right[2] + 1
            )

        a, b, q = f(0, n)
        print("!", a, b - a, flush=True)
        print(f"Case #{t+1:03} q:", q, file=stderr)
