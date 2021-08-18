#!/usr/bin/env python3
import sys
sys.setrecursionlimit(1000000)

if len(sys.argv) == 2 and sys.argv[1] == 'yes':
    be_efficient = True
else:
    be_efficient = False


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

    def getMinMoves(self, initial, final, efficient=True):
        assert len(initial) == len(final)
        if efficient:
            # return self.__getMinMoves_classic(initial, final)
            return (2 ** len(initial)) -1
        else:
            self.n_moves = 0
            self.move(initial, final)
            return self.n_moves

    def __getMinMovesTowerInto(self, peg, config):
        """Return the minimum moves for move the tower in peg to the specified configuration"""
        counter = 0
        current = peg
        for i in range(len(config), 0, -1):
            if (current != config[i - 1]):
                sub_target = self.__getPegFrom(current, config[i-1])
                counter += 2 ** (i - 1)
                current = sub_target
        return counter
    
    def __getMinMoves_classic(self, initial, final):
        """I assume: len(initial) == len(final). Return the minimum of moves to move all disks from initial configuration to final configuration"""
        disk = len(initial)
        if disk <= 0:
            return 0
        if initial[-1] == final[-1]:
            return self.__getMinMoves_classic(initial[:-1], final[:-1])
        else:
            aux_peg = self.__getPegFrom(initial[-1], final[-1])
            return self.__getMinMovesTowerInto(aux_peg, initial[:-1]) + 1 + \
                    self.__getMinMovesTowerInto(aux_peg, final[:-1])

h = MyHanoi()

while True:
    start = input()
    if start[0] == '#':
        continue
    if start == 'Finish Tests':
        break
    final = input()
    print(h.getMinMoves(start, final, be_efficient))
