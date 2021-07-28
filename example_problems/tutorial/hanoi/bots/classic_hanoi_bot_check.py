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
        print(f"{disk}:{current}{target}")


def move_tower(n, current, target, support):
    if (n <= 0 or current == target):
        return
    move_tower(n - 1, current, support, target)
    move_disk(n, current, target)
    move_tower(n - 1, support, target, current)



wait_start()
##############################
# TEST1:
# CASE: AA -> CC
# move_tower(2, 'A', 'C', 'B')

# CASE: AA -> CC simple-walk not-optimal
print('1:AC')
print('1:CB')
print('2:AC')
print('1:BA')
print('1:AC')


# TEST2:
# CASE: ABC -> CBA
# print('1:AB')
# print('3:CA')
# print('1:BC')
# print('1:CB')
# print('1:BC')
##############################
print("end")
wait_end() 

