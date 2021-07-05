#!/usr/bin/env python3
import sys, random
sys.setrecursionlimit(1000000)


def get_input_from(config, n):
    """Assume N!=-1 if start=all_X and final=all_X"""
    if config == "all_A":
        return 'A' * n
    if config == "all_B":
        return 'B' * n
    if config == "all_C":
        return 'C' * n
    return config


class HanoiTowerProblem():
    def __init__(self, version):
        # All
        self.version = version  # classic|toddler|clockwise
        self.moves = list()

        # toddler version
        self.names = ["[Daddy  ] ", "[Toddler] "]
        self.player = 0
    

    # PUBLIC INTERFACE
    def get_min_moves(self, initial, final):
        assert len(initial) == len(final)
        return self.__get_min_moves_from_to(initial, final)


    def get_moves_list(self, start, final):
        assert len(start) == len(final)
        self.moves.clear()
        self.__move_disks_from_to(start, final)
        self.player = 0
        return self.moves
    
    
    def is_valid(self, state, disk, c, t):
        """Assume valid state"""
        if (c != 'A' and c!= 'B' and c != 'C') or \
           (t != 'A' and t!= 'B' and t != 'C'):
           return False # invalid peg
        if state[disk-1] != c:
            return False # wrong current
        for i in range(disk-1, 0, -1):
            if state[i-1] == state[disk-1]:
                return False #disk is blocked
        return True
    

    def check_sol(self, sol, initial, final):
        state = initial
        states = {state : 1}
        for e in sol:
            disk, tmp = e.split(": ")
            disk = int(disk)
            c, t = tmp.split("->")
            if not self.is_valid(state, disk, c, t):
                return 'move_not_valid', e
            state = state[:disk-1] + t + state[disk:]
            states[state] = states.get(state, 0) + 1
        if state != final:
            return 'final_wrong', state
        # check loops
        for k, v in states.items():
            if v > 1:
                return 'admissible', k
        return 'admissible', None


    def get_not_opt_sol(self, initial, final, size):
        tmp = self.version
        self.version = 'classic'
        self.moves.clear()
        self.__move_disks_from_to(initial, final)
        self.version = tmp
        sol = self.moves.copy()
        diff = size - len(sol)
        if diff <= 0:
            return sol

        i = 0
        while i < len(sol) and diff > 0:
            disk, tmp = sol[i].split(": ")
            disk = int(disk)
            if disk == 1 and random.randint(1,10) > 2:
                c, t = tmp.split("->")
                s = self.__getPegFrom(c, t)
                sol[i] = f"{disk}: {c}->{s}"
                sol.insert(i+1, f"{disk}: {s}->{t}")
                diff = diff - 1
                # deliberately not incrementing by 2 to add randomness
            i = i + 1
        
        for _ in range(diff):
            move_index = random.randint(0, len(sol)-1)
            disk, tmp = sol[move_index].split(": ")
            c, t = tmp.split("->")
            sol.insert(move_index, f"{disk}: {c}->{c}")
        
        if self.version == "toddler":
            p = 0
            for i in range(len(sol)):
                sol[i] = self.names[p] + sol[i]
                p = (p + 1) % 2
        return sol


    # PRIVATE
    def __getPegFrom(self, x, y):
        if x == 'A':
            if y == 'B':
                return 'C'
            return 'B'
        elif x == 'B':
            if y == 'A':
                return 'C'
            return 'A'
        if y == 'B':
            return 'A'
        return 'B'


    def __move_disk(self, disk, current, target):
        """Move the disk from current to target"""
        if self.version == 'classic':
            self.moves.append(f"{disk}: {current}->{target}")

        elif self.version == 'toddler':
            self.moves.append(f"[{self.names[self.player]}]{disk}: {current}->{target}")
            self.player = (self.player + 1) % 2
    

    def __move_disks_from_to(self, initial, final):
        """I assume: len(initial) == len(final). Move all disks from initial configuration to final configuration"""
        disk = len(initial)
        if disk <= 0:
            return 
        if initial[-1] == final[-1]:
            self.__move_disks_from_to(initial[:-1], final[:-1])
        else:
            intermediate = self.__getPegFrom(initial[-1], final[-1]) * (disk - 1)
            self.__move_disks_from_to(initial[:-1], intermediate)
            self.__move_disk(disk, initial[-1], final[-1])
            self.__move_disks_from_to(intermediate, final[:-1])


    def __get_min_moves_tower_to(self, peg, final):
        """Return the minimum moves for move the tower in peg to final configuration"""
        counter = 0
        current = peg
        for i in range(len(final), 0, -1):
            if (current != final[i - 1]):
                sub_target = self.__getPegFrom(current, final[i-1])
                counter += 2 ** (i - 1)
                current = sub_target
        return counter
    

    def __get_min_moves_from_to(self, initial, final):
        """I assume: len(initial) == len(final). Return the minimum of moves to move all disks from initial configuration to final configuration"""
        disk = len(initial)
        if disk <= 0:
            return 0
        if initial[-1] == final[-1]:
            return self.__get_min_moves_from_to(initial[:-1], final[:-1])
        else:
            intermediate = self.__getPegFrom(initial[-1], final[-1])
            return self.__get_min_moves_tower_to(intermediate, initial[:-1]) + 1 + \
                    self.__get_min_moves_tower_to(intermediate, final[:-1])



if __name__ == "__main__":
    h_classic = HanoiTowerProblem(version='classic')
    assert h_classic.get_min_moves('A', 'A') == 0
    assert h_classic.get_min_moves('A', 'C') == 1
    assert h_classic.get_min_moves('AA', 'CC') == 3
    assert h_classic.get_min_moves('AAA', 'CCC') == 7
    assert h_classic.get_min_moves('AAAA', 'CCCC') == 15

    assert h_classic.is_valid('AA', 2, 'A', 'B') == False
    assert h_classic.is_valid('AA', 1, 'A', 'B') == True
    assert h_classic.is_valid('AA', 1, 'A', 'D') == False
    assert h_classic.is_valid('AA', 1, 'C', 'B') == False


    h_toddler = HanoiTowerProblem(version='toddler')
    assert h_toddler.get_min_moves('A', 'A') == 0
    assert h_toddler.get_min_moves('A', 'C') == 1
    assert h_toddler.get_min_moves('AA', 'CC') == 3
    assert h_toddler.get_min_moves('AAA', 'CCC') == 7
    assert h_toddler.get_min_moves('AAAA', 'CCCC') == 15

    assert h_toddler.get_min_moves('AA', 'BB') == 3
    assert h_toddler.get_min_moves('AAA', 'BBB') == 7
    assert h_toddler.get_min_moves('AA', 'CC') == 3
    assert h_toddler.get_min_moves('AA', 'AC') == 3
    assert h_toddler.get_min_moves('AAA', 'ABC') == 5
    assert h_toddler.get_min_moves('AAAA', 'CBCC') == 14



    initial = 'AA'
    final = 'CC'
    opt_sol = h_classic.get_moves_list(initial, final)
    assert h_classic.check_sol(opt_sol, initial, final) == ('admissible', None)

    not_opt_sol = h_classic.get_not_opt_sol(initial, final, 5)
    assert h_classic.check_sol(not_opt_sol, initial, final) == ('admissible', 'AA')