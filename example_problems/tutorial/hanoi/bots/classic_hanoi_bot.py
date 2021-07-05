#!/usr/bin/env python3
from os import wait
import sys
sys.setrecursionlimit(1000000)


def wait_start():
    while True:
        spoon = input()
        if spoon[0] != '#':
            break


def wait_end():
    while True:
        spoon = input()

def move_disk(disk, current, target):
    if current != target:
        print(f"{disk}: {current}->{target}")


def move_tower(n, current, target, support):
    if (n <= 0 or current == target):
        return
    move_tower(n - 1, current, support, target)
    move_disk(n, current, target)
    move_tower(n - 1, support, target, current)



wait_start()
##############################
# CASE: AA -> CC
# move_tower(2, 'A', 'C', 'B')

# CASE: ABC -> CBA
print('1: A->B')
print('3: C->A')
print('1: B->C')
print('1: C->C')
print('1: C->C')
print('1: C->C')
print('1: C->C')
##############################
print("end")
wait_end() 

