#!/usr/bin/env python3

import random as ran

def main():
    print("Indovina il mio numero")
    n = ran.randint(0, 10)
    while True:
        my = int(input())
        if (my > n):
            print("Piu piccolo")
        elif (my < n):
            print("Piu grande")
        else:
            print("Uguale")
            break

if __name__ == "__name__":
    main()
