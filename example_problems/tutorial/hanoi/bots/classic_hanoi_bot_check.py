#!/usr/bin/env python3
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



# START
wait_start()
move_tower(2, 'A', 'C', 'B')
print("end")
wait_end()