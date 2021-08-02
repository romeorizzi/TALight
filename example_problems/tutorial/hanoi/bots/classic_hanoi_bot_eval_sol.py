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


class MyHanoi():
    def __getPegFrom(self, peg1, peg2):
        if peg1 == 'A':
            if peg2 == 'B':
                return 'C'
            return 'B'
        elif peg1 == 'B':
            if peg2 == 'A':
                return 'C'
            return 'A'
        if peg2 == 'B':
            return 'A'
        return 'B'

    def __moveDisk(self, disk, current, target):
        print(f"{disk}:{current}{target}")
    
    def move(self, initial, final):
        """I assume: len(initial) == len(final). Move all disks from initial configuration to final configuration"""
        disk = len(initial)
        if disk <= 0:
            return 
        if initial[-1] == final[-1]:
            self.move(initial[:-1], final[:-1])
        else:
            intermediate = self.__getPegFrom(initial[-1], final[-1]) * (disk - 1)
            self.move(initial[:-1], intermediate)
            self.__moveDisk(disk, initial[-1], final[-1])
            self.move(intermediate, final[:-1])


h = MyHanoi()


##############################
while True:
    start = input()
    if start[0] == '#':
        continue
    if start == 'Finish Tests':
        break
    final = input()
    h.move(start, final)
    # print(f"1:AC")
    print('end')


