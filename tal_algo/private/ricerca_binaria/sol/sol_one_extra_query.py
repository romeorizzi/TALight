#!/usr/bin/env python3

from sys import stdout, stderr

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n, k, b = map(int, input().strip().split())
        print(f"Testcase {t}: {n=}, {k=}, {b=}", file=stderr)
        if b == 0:
            lier = { i: 'no' for i in range(k) }
        else:
            assert b == 1
            lier = { i: 'unknown' for i in range(k) }
        left = 1; right = n; q = 0
        x_questioned = False
        while left < right:
            q = q + 1
            if lier[q%k] == 'unknown':
                print(f"?{right}", flush=True)
                ans = input().strip()
                if ans == '=':
                    left = right
                    x_questioned = True
                elif ans == '>':
                    lier[q%k] == 'yes'
                    right = right - 1
                else:
                    assert ans == '<'
                    lier[q%k] == 'no'
                    right = right - 1
            else:
                assert lier[q%k] in {'yes','no'}
                mid = (left + right)//2
                print(f"?{mid}", flush=True)
                ans = input().strip()
                assert ans in {'<','>','='}
                if ans == '=':
                    x_questioned = True
                    left = right
                elif ( ans == '>' ) == ( lier[q%k] == 'no' ):
                    left = mid + 1
                else:
                    right = mid - 1
        assert left == right
        if not x_questioned:
            print(f"?{left}", flush=True)
            assert input().strip() == '='            
        print(f"!{left}", flush=True)
