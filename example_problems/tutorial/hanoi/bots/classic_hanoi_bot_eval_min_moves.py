#!/usr/bin/env python3
from os import wait
import sys
sys.setrecursionlimit(1000000)


class MyHanoi():
    def __init__(self):
        self.n_moves = 0
    
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

    def getMin(self, initial, final):
        self.n_moves = 0
        self.move(initial, final)
        return self.n_moves

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
            self.n_moves += 1
            self.move(intermediate, final[:-1])

    def getMinTowerOf(self, n):
        return 2**n -1

h = MyHanoi()

while True:
    start = input()
    if start[0] == '#':
        continue
    if start == 'end':
        break
    final = input()
    # print(h.getMin(start, final)) # not efficient
    print(h.getMinTowerOf(len(start))) # efficient


