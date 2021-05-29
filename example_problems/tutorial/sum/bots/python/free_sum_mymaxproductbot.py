#!/usr/bin/env python3

while True:
    spoon = input()
    if spoon[0] != '#':
        n = int(spoon)
        print(f"{n//2} {(n+1)//2}")
