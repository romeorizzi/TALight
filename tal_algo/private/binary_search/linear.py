#!/usr/bin/env python3

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n = int(input())
        s = []
        stopped = False
        for i in range(n):
            print("?", i, 1, flush=True)
            r = input().strip()
            if r == "-1":
                stopped = True
                break
            s.append(r)
        s = "".join(s)
        if stopped:
            continue
        print("!", s.find("1"), s.count("1"), flush=True)
