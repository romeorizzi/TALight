#!/usr/bin/env python3
from os import name
from re import L, sub
import sys, random
sys.setrecursionlimit(1000000)


def get_input_from(config, n, seed = 0, n_query=1):
    """Assume N!=-1 if start=all_X and final=all_X"""
    if config == 'all_A':
        return 'A' * n
    if config == 'all_B':
        return 'B' * n
    if config == 'all_C':
        return 'C' * n
    if config == 'general':
        random.seed(seed)
        for _ in range(n_query):
            config = ''
            for _ in range(n):
                config += random.choice(('A', 'B', 'C'))
    return config


def get_description_of(code):
    if code == 0:
        return "Correct"
    if code == 1:
        return "Invalid disk: not exist"
    if code == 2:
        return "Wrong current or state: they don't coincide"
    if code == 3:
        return "Invalid peg: not exist"
    if code == 4:
        return "Invalid move: current and target can't be equal"
    if code == 5:
        return "Invalid disk: Toddler can't move last disk"
    if code == 6:
        return "Invalid move: counterclockwise move"
    if code == 7:
        return "Invalid move: big disk on small disk"
    if code == 8:
        return "Invalid disk: is blocked"
    return "This code not exist"


class HanoiTowerProblem():
    def __init__(self, version):
        # All
        assert version == 'classic' or version == 'toddler' or version == 'clockwise'
        self.version = version  # classic|toddler|clockwise
        self.moves = list()
        self.n_moves_of = list()

        # toddler version
        self.names = ["Daddy  ", "Toddler"]
        assert len(self.names[0]) == len(self.names[1])
        self.len_names = len(self.names[0])
        self.player = 0

        # clockwise version
        self.mem = dict()
    

    # PUBLIC INTERFACE
    def getMovesList(self, initial, final):
        assert len(initial) == len(final)
        self.moves.clear()
        self.n_moves_of = [0] * (len(initial) + 1)

        if self.version == 'classic':
            self.__move_classic(initial, final)
        
        elif self.version == 'toddler':
            self.player = 0
            self.__move_classic(initial, final) #equal to toddler version
        
        elif self.version == 'clockwise':
            self.__move_clockwise(initial, final)
        
        return self.moves


    def getMinMoves(self, initial, final, optimized=True):
        assert len(initial) == len(final)
        if optimized:
            if self.version == 'classic':
                return self.__getMinMoves_classic(initial, final)
            
            if self.version == 'toddler':
                return self.__getMinMoves_classic(initial, final)
            
            if self.version == 'clockwise':
                # self.mem.clear()
                return self.__getMinMoves_clockwise(initial, final)
        else:
            self.getMovesList(initial, final)
            return sum(self.n_moves_of)


    def getMinMovesOf(self, initial, final, disk):
        assert len(initial) == len(final)
        assert disk > 0 and disk <= len(initial)
        self.getMovesList(initial, final)
        return self.n_moves_of[disk]
    
    
    def parseMove(self, move):
        if self.version == 'toddler':
            player, tmp = move.split("|")
            if player == self.names[0]:
                p = 0
            elif player == self.names[1]:
                p = 1
            else:
                p = -1
            disk, tmp = tmp.split(":")
            disk = int(disk)
            c = tmp[0]
            t = tmp[1]
            return disk, c, t, p
        else:
            disk, tmp = move.split(":")
            disk = int(disk)
            c = tmp[0]
            t = tmp[1]
            return disk, c, t


    def checkMove(self, state, disk, c, t, player = None, last_disk = None):
        """Assume valid state and valid last_disk"""
        if disk > len(state) or disk < 1:
            return 1 #Invalid disk: not exist
        if state[disk-1] != c:
            return 2 #Wrong current or state: they don't coincide
        if (c != 'A' and c!= 'B' and c != 'C') or \
           (t != 'A' and t!= 'B' and t != 'C'):
           return 3 #Invalid Peg: not exist
        if c == t:
            return 4 #Invalid move: current and target can't be equal
        if self.version == 'toddler':
            assert player != None
            assert last_disk != None
            assert last_disk > 0 and last_disk <= len(state)
            if player == 1 and disk == last_disk:
                return 5 #Invalid disk: Toddler can't move last disk
        if self.version == 'clockwise':
            if t == self.__getPegFrom(self.__getNextPeg(c), c):
                return 6 #Invalid move: counterclockwise move
        for i in range(disk-1, 0, -1):
            if state[i-1] == t:
                return 7 #Invalid move: big disk on small disk
        for i in range(disk-1, 0, -1):
            if state[i-1] == state[disk-1]:
                return 8 #Invalid disk: is blocked
        return 0 #Correct
    

    def isValid(self, state, disk, c, t, player = None, last_disk = None):
        return self.checkMove(state, disk, c, t, player, last_disk) == 0


    def checkSol(self, sol, initial, final):
        state = initial
        states = {state : 1}
        last_disk = 1 #Daddy move always first, so first last_disk is ignored
        for e in sol:
            if self.version == 'toddler':
                disk, c, t, p = self.parseMove(e)
                if not self.isValid(state, disk, c, t, p, last_disk):
                    return 'move_not_valid', e
            else:
                disk, c, t = self.parseMove(e)
                if not self.isValid(state, disk, c, t):
                    return 'move_not_valid', e
            state = state[:disk-1] + t + state[disk:]
            states[state] = states.get(state, 0) + 1
            last_disk = disk
        if state != final:
            return 'final_wrong', state
        # check loops
        for k, v in states.items():
            if v > 1:
                return 'admissible', k
        return 'admissible', None


    def getNotOptimalSol(self, initial, final, desired_size):
        self.getMovesList(initial, final)
        sol = self.moves
        diff = desired_size - len(sol)
        if diff <= 0 or len(sol) == 0:
            return sol
        
        i = 0
        if self.version == 'toddler':
            n_moves_t = len(sol) // 2           # toddler
            n_moves_d = len(sol) - n_moves_t    # daddy
            # n_moves_t + 3(n_upgrades) + 1(n_moves_d - n_upgrades) <= desired_size
            # -> n_upgrades <= diff / 2
            n_upgrades = diff // 2 if (diff // 2) < n_moves_d else n_moves_d
            i_targets = random.sample(range(0, len(sol), 2), n_upgrades)

            state = initial #Note: without [None] + the i = disk-1
            while i < len(sol):
                disk, c, t, p = self.parseMove(sol[i])
                state = state[:disk-1] + t + state[disk:]
                if i in i_targets:
                    s = self.__getPegFrom(c, t)
                    x = state[disk] #this is the state of disk+1
                    y = self.__getPegFrom(x, s)
                    sol[i] = f"{self.names[0]}|{disk}:{c}{s}"
                    sol.insert(i+1, f"{self.names[0]}|{disk+1}:{x}{y}")
                    sol.insert(i+2, f"{self.names[0]}|{disk+1}:{y}{x}")
                    sol.insert(i+3, f"{self.names[0]}|{disk}:{s}{t}")
                    i += 3
                else:
                    i += 1

            p = 0
            for i in range(len(sol)):
                sol[i] = self.names[p] + sol[i][self.len_names:]
                p = (p + 1) % 2
            return sol

        else:
            while diff > 0:
                disk, c, t = self.parseMove(sol[i])
                if disk == 1 and random.randint(1,10) > 2:
                    if self.version == 'classic':
                        s = self.__getPegFrom(c, t)
                        sol[i] = f"{disk}:{c}{s}"
                        sol.insert(i+1, f"{disk}:{s}{t}")
                        diff = diff - 1
                        if diff <= 0:
                            break
                        # deliberately not incrementing by 1+1 to add randomness
                    elif self.version == 'clockwise':
                        s = self.__getNextPeg(t)
                        sol.insert(i+1, f"{disk}:{t}{s}")
                        sol.insert(i+2, f"{disk}:{s}{c}")
                        sol.insert(i+3, f"{disk}:{c}{t}")
                        diff = diff - 3
                        # deliberately not incrementing by 1+3 to add randomness
                        if diff < 3:
                            break
                i = i + 1
                if i >= len(sol):
                    i = 0
            return sol


    def getAvailableMovesIn(self, state, player = None, last_disk = None):
        '''I Assume valid state and valid last_dik'''
        state = [None] + list(state)
        move_list = list()
        blocked = {'A': False, 'B': False, 'C': False}
        
        for disk in range(1, len(state)):
            # Check if the i-disk is blocked
            if not blocked[state[disk]]:
                # Check if the other pegs have disk smaller
                for t in self.__getPegsFrom(state[disk]):
                    if not blocked[t]:
                        if self.version == 'classic':
                            move_list.append(f"{disk}:{state[disk]}{t}")
                        elif self.version == 'toddler':
                            assert player != None
                            assert last_disk != None
                            assert last_disk > 0 and last_disk <= len(state)
                            if player == 0 or disk != last_disk:
                                move_list.append(f"{self.names[player]}|{disk}:{state[disk]}{t}")
                        elif self.version == 'clockwise':
                            if t == self.__getNextPeg(state[disk]):
                                move_list.append(f"{disk}:{state[disk]}{t}")
            # Blocking
            blocked[state[disk]] = True
            
            # Check if all other moves are blocked
            if all(v == True for v in blocked.values()):
                break
        
        # print(move_list)
        return move_list


    # PRIVATE ALL
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


    def __getNextPeg(self, peg):
        if peg == 'A':
            return 'B'
        if peg == 'B':
            return 'C'
        if peg == 'C':
            return 'A'


    def __getPegsFrom(self, peg):
        return self.__getNextPeg(peg), self.__getNextPeg(self.__getNextPeg(peg))


    def __moveDisk(self, disk, current, target):
        """Move the disk from current to target"""
        if self.version == 'classic':
            self.moves.append(f"{disk}:{current}{target}")

        elif self.version == 'toddler':
            self.moves.append(f"{self.names[self.player]}|{disk}:{current}{target}")
            self.player = (self.player + 1) % 2

        elif self.version == 'clockwise':
            self.moves.append(f"{disk}:{current}{target}")
        
        self.n_moves_of[disk] += 1
    

    # PRIVATE CLASSIC
    def __move_classic(self, initial, final):
        """I assume: len(initial) == len(final). Move all disks from initial configuration to final configuration"""
        disk = len(initial)
        if disk <= 0:
            return 
        if initial[-1] == final[-1]:
            self.__move_classic(initial[:-1], final[:-1])
        else:
            intermediate = self.__getPegFrom(initial[-1], final[-1]) * (disk - 1)
            self.__move_classic(initial[:-1], intermediate)
            self.__moveDisk(disk, initial[-1], final[-1])
            self.__move_classic(intermediate, final[:-1])


    def __getMinMovesTowerInto(self, peg, config):
        """Return the minimum moves for move the tower in peg to the specified configuration"""
        counter = 0
        current = peg
        for i in range(len(config), 0, -1):
            if (current != config[i - 1]):
                sub_target = self.__getPegFrom(current, config[i-1])
                # Explain:
                # move_tower(i - 1, current, sub_target, final[i-1])
                # -> min_moves = 2 ** (i-1) - 1
                # move_disk(i, current, final[i-1])
                # -> min_moves = 1
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


    # PRIVATE CLOCKWISE
    def __move_clockwise(self, initial, final):
        """I assume: len(initial) == len(final). Move all disks from initial configuration to final configuration"""
        disk = len(initial)
        if disk <= 0:
            return 
        if initial[-1] == final[-1]:
            self.__move_clockwise(initial[:-1], final[:-1])
        else:
            next_peg = self.__getNextPeg(initial[-1])
            if final[-1] == next_peg:
                intermediate = self.__getPegFrom(initial[-1], final[-1]) * (disk - 1)
                self.__move_clockwise(initial[:-1], intermediate)
                self.__moveDisk(disk, initial[-1], final[-1])
                self.__move_clockwise(intermediate, final[:-1])
            else:
                intermediate1 = final[-1] * (disk - 1)
                intermediate2 = initial[-1] * (disk - 1)
                self.__move_clockwise(initial[:-1], intermediate1)
                self.__moveDisk(disk, initial[-1], next_peg)
                self.__move_clockwise(intermediate1, intermediate2)
                self.__moveDisk(disk, next_peg, final[-1])
                self.__move_clockwise(intermediate2, final[:-1])


    def __getMinMoves_clockwise(self, initial, final):
        """I assume: len(initial) == len(final). Move all disks from initial configuration to final configuration"""
        disk = len(initial)
        if disk <= 0:
            return 0
        if (initial, final) in self.mem:
            return self.mem[(initial, final)]
        else:
            sum = 0
            if initial[-1] == final[-1]:
                sum += self.__getMinMoves_clockwise(initial[:-1], final[:-1])
            else:
                next_peg = self.__getNextPeg(initial[-1])
                if final[-1] == next_peg:
                    intermediate = self.__getPegFrom(initial[-1], final[-1]) * (disk - 1)
                    sum += self.__getMinMoves_clockwise(initial[:-1], intermediate)
                    sum += 1
                    sum += self.__getMinMoves_clockwise(intermediate, final[:-1])
                else:
                    intermediate1 = final[-1] * (disk - 1)
                    intermediate2 = initial[-1] * (disk - 1)
                    sum += self.__getMinMoves_clockwise(initial[:-1], intermediate1)
                    sum += 1
                    sum += self.__getMinMoves_clockwise(intermediate1, intermediate2)
                    sum += 1
                    sum += self.__getMinMoves_clockwise(intermediate2, final[:-1])
            self.mem[(initial, final)] = sum
            return sum


if __name__ == "__main__":
    enable_test_classic = 1
    enable_test_toddler = 1
    enable_test_clockwise = 1
    enable_advanced_tests = 1
    print_feedback = 1

    seed = 13000
    num_tests = 50
    num_tests_not_optimal = 10
    n_max = 10
    size_shorter = 10
    


    # CLASSIC
    if enable_test_classic:
        print("START  TEST CLASSIC")
        h_classic = HanoiTowerProblem(version='classic')

        # Check parseMove
        assert h_classic.parseMove('130:AB') == (130, 'A', 'B')

        # Check isValid
        assert h_classic.isValid('AA', 2, 'A', 'B') == False
        assert h_classic.isValid('AA', 1, 'A', 'B') == True

        # Check checkMove
        assert h_classic.checkMove('AA', 1, 'A', 'B') == 0
        assert h_classic.checkMove('AA', -1, 'A', 'B') == 1
        assert h_classic.checkMove('AA', 130, 'A', 'B') == 1
        assert h_classic.checkMove('AA', 1, 'B', 'A') == 2
        assert h_classic.checkMove('AA', 1, 'A', 'D') == 3
        assert h_classic.checkMove('DA', 1, 'D', 'A') == 3
        assert h_classic.checkMove('AA', 1, 'A', 'A') == 4
        assert h_classic.checkMove('BA', 2, 'A', 'B') == 7
        assert h_classic.checkMove('AA', 2, 'A', 'B') == 8

        # Check getMinMoves
        assert h_classic.getMinMoves('A', 'A') == 0
        assert h_classic.getMinMoves('A', 'C') == 1
        assert h_classic.getMinMoves('AA', 'CC') == 3
        assert h_classic.getMinMoves('AAA', 'CCC') == 7
        assert h_classic.getMinMoves('AAAA', 'CCCC') == 15
        assert h_classic.getMinMoves('AA', 'BB') == 3
        assert h_classic.getMinMoves('AAA', 'BBB') == 7
        assert h_classic.getMinMoves('AA', 'AC') == 3
        assert h_classic.getMinMoves('AAA', 'ABC') == 5
        assert h_classic.getMinMoves('AAAA', 'CBCC') == 14

        # Check getAvailableMovesIn
        assert h_classic.getAvailableMovesIn('A') == \
            ['1:AB', '1:AC']
        assert h_classic.getAvailableMovesIn('AA') == \
            ['1:AB', '1:AC']
        assert h_classic.getAvailableMovesIn('AB') == \
            ['1:AB', '1:AC', '2:BC']
        assert h_classic.getAvailableMovesIn('AAA') == \
            ['1:AB', '1:AC']
        assert h_classic.getAvailableMovesIn('ABB') == \
            ['1:AB', '1:AC', '2:BC']
        assert h_classic.getAvailableMovesIn('ABC') == \
            ['1:AB', '1:AC', '2:BC']
        

        if enable_advanced_tests:
            # Random tests
            for t in range(1, num_tests + 1):
                for n in range(1, n_max + 1):
                    # get random configs
                    initial = get_input_from('general', n, seed, 1)
                    final = get_input_from('general', n,  seed, 2)

                    # Check getMovesList
                    try:
                        opt_sol = h_classic.getMovesList(initial, final)
                        assert h_classic.checkSol(opt_sol, initial, final) == ('admissible', None)
                    except AssertionError:
                        print("AssertionError in classic -> getMovesList()")
                        print(f"initial: {initial}")
                        print(f"final:   {final}")
                        print(f"sol: {opt_sol}")
                        for e in opt_sol:
                            print(e)
                        exit(0)

                    # Check getNotOptimalSol
                    for _ in range(num_tests_not_optimal):
                        try:
                            not_opt_sol = h_classic.getNotOptimalSol(initial, final, size_shorter)
                            adm, info = h_classic.checkSol(not_opt_sol, initial, final) 
                            assert adm == 'admissible'
                        except AssertionError:
                            print("AssertionError in classic -> getNotOptimalSol()")
                            print(f"initial: {initial}")
                            print(f"final:   {final}")
                            print(f"sol: {not_opt_sol}")
                            for e in not_opt_sol:
                                print(e)
                            exit(0)

                    # Check correctness min_moves optimized
                    fast = h_classic.getMinMoves(initial, final, True)
                    slow = h_classic.getMinMoves(initial, final, False)
                    assert fast == slow
                if print_feedback:
                    print(f"-> finish test {t}/{num_tests}")
        
        print("FINISH TEST CLASSIC")



    # TODDLER
    if enable_test_toddler:
        print("START  TEST TODDLER")
        h_toddler = HanoiTowerProblem(version='toddler')

        # Check parseMove
        assert h_toddler.parseMove('Daddy  |130:AB') == (130, 'A', 'B', 0)
        assert h_toddler.parseMove('Daddy  |130:AB') != (130, 'A', 'B', 1)
        assert h_toddler.parseMove('Toddler|130:AB') != (130, 'A', 'B', 0)
        assert h_toddler.parseMove('Toddler|130:AB') == (130, 'A', 'B', 1)

        # Check isValid
        assert h_toddler.isValid('AA', 2, 'A', 'B', 0, 1) == False
        assert h_toddler.isValid('AA', 1, 'A', 'B', 0, 1) == True
        assert h_toddler.isValid('AA', 1, 'A', 'B', 0, 1) == True
        assert h_toddler.isValid('AA', 1, 'A', 'B', 1, 1) == False

        # Check checkMove
        assert h_toddler.checkMove('AA', 1, 'A', 'B', 0, 1) == 0
        assert h_toddler.checkMove('AA', -1, 'A', 'B', 0, 1) == 1
        assert h_toddler.checkMove('AA', 130, 'A', 'B', 0, 1) == 1
        assert h_toddler.checkMove('AA', 1, 'B', 'A', 0, 1) == 2
        assert h_toddler.checkMove('AA', 1, 'A', 'D', 0, 1) == 3
        assert h_toddler.checkMove('DA', 1, 'D', 'A', 0, 1) == 3
        assert h_toddler.checkMove('AA', 1, 'A', 'A', 0, 1) == 4
        assert h_toddler.checkMove('AA', 1, 'A', 'B', 0, 1) == 0
        assert h_toddler.checkMove('AA', 1, 'A', 'B', 1, 1) == 5
        assert h_toddler.checkMove('BA', 2, 'A', 'B', 1, 1) == 7
        assert h_toddler.checkMove('AA', 2, 'A', 'B', 0, 1) == 8

        # Check getMovesList
        assert h_toddler.getMovesList('AA', 'AC') == \
            ['Daddy  |1:AB', 'Toddler|2:AC', 'Daddy  |1:BA']
        assert h_toddler.getMovesList('AA', 'BB') == \
            ['Daddy  |1:AC', 'Toddler|2:AB', 'Daddy  |1:CB']
        assert h_toddler.getMovesList('AAA', 'ABC') == \
            ['Daddy  |1:AC', 'Toddler|2:AB', 'Daddy  |1:CB', 'Toddler|3:AC', 'Daddy  |1:BA']

        # Check getAvailableMovesIn
        assert h_toddler.getAvailableMovesIn('A', 0, 1) == \
            ['Daddy  |1:AB', 'Daddy  |1:AC']
        assert h_toddler.getAvailableMovesIn('A', 1, 1) == \
            []
        assert h_toddler.getAvailableMovesIn('A', 1, 2) == \
            ['Toddler|1:AB', 'Toddler|1:AC']
        assert h_toddler.getAvailableMovesIn('AA', 0, 1) == \
            ['Daddy  |1:AB', 'Daddy  |1:AC']
        assert h_toddler.getAvailableMovesIn('AA', 1, 1) == \
            []
        assert h_toddler.getAvailableMovesIn('AA', 1, 2) == \
            ['Toddler|1:AB', 'Toddler|1:AC']
        assert h_toddler.getAvailableMovesIn('AB', 0, 1) == \
            ['Daddy  |1:AB', 'Daddy  |1:AC', 'Daddy  |2:BC']
        assert h_toddler.getAvailableMovesIn('AB', 1, 1) == \
            ['Toddler|2:BC']
        assert h_toddler.getAvailableMovesIn('AB', 1, 2) == \
            ['Toddler|1:AB', 'Toddler|1:AC']
        assert h_toddler.getAvailableMovesIn('AAA', 0, 1) == \
            ['Daddy  |1:AB', 'Daddy  |1:AC']
        assert h_toddler.getAvailableMovesIn('AAA', 1, 1) == \
            []
        assert h_toddler.getAvailableMovesIn('AAA', 1, 2) == \
            ['Toddler|1:AB', 'Toddler|1:AC']
        assert h_toddler.getAvailableMovesIn('AAA', 1, 3) == \
            ['Toddler|1:AB', 'Toddler|1:AC']
        assert h_toddler.getAvailableMovesIn('ABB', 0, 1) == \
            ['Daddy  |1:AB', 'Daddy  |1:AC', 'Daddy  |2:BC']
        assert h_toddler.getAvailableMovesIn('ABB', 1, 1) == \
            ['Toddler|2:BC']
        assert h_toddler.getAvailableMovesIn('ABB', 1, 2) == \
            ['Toddler|1:AB', 'Toddler|1:AC']
        assert h_toddler.getAvailableMovesIn('ABB', 1, 3) == \
            ['Toddler|1:AB', 'Toddler|1:AC', 'Toddler|2:BC']
        assert h_toddler.getAvailableMovesIn('ABC', 0, 1) == \
            ['Daddy  |1:AB', 'Daddy  |1:AC', 'Daddy  |2:BC']
        assert h_toddler.getAvailableMovesIn('ABC', 1, 1) == \
            ['Toddler|2:BC']
        assert h_toddler.getAvailableMovesIn('ABC', 1, 2) == \
            ['Toddler|1:AB', 'Toddler|1:AC']
        assert h_toddler.getAvailableMovesIn('ABC', 1, 3) == \
            ['Toddler|1:AB', 'Toddler|1:AC', 'Toddler|2:BC']


        if enable_advanced_tests:
            # Random tests
            for t in range(1, num_tests + 1):
                for n in range(1, n_max + 1):
                    # get random configs
                    initial = get_input_from('general', n, seed, 1)
                    final = get_input_from('general', n,  seed, 2)

                    # Check getMovesList
                    try:
                        opt_sol = h_toddler.getMovesList(initial, final)
                        adm, info = h_toddler.checkSol(opt_sol, initial, final) 
                        assert h_toddler.checkSol(opt_sol, initial, final) == ('admissible', None)
                    except AssertionError:
                        print("AssertionError in toddler -> getMovesList()")
                        print(f"initial: {initial}")
                        print(f"final:   {final}")
                        print(f"sol: {opt_sol}")
                        for e in opt_sol:
                            print(e)
                        exit(0)

                    # Check getNotOptimalSol
                    for _ in range(num_tests_not_optimal):
                        try:
                            not_opt_sol = h_toddler.getNotOptimalSol(initial, final, size_shorter)
                            adm, info = h_toddler.checkSol(not_opt_sol, initial, final) 
                            assert adm == 'admissible'
                        except AssertionError:
                            print("AssertionError in toddler -> getNotOptimalSol()")
                            print(f"initial: {initial}")
                            print(f"final:   {final}")
                            print(f"sol: {not_opt_sol}")
                            for e in not_opt_sol:
                                print(e)
                            exit(0)

                    # Check correctness min_moves optimized
                    fast = h_toddler.getMinMoves(initial, final, True)
                    slow = h_toddler.getMinMoves(initial, final, False)
                    assert fast == slow
                if print_feedback:
                    print(f"-> finish test {t}/{num_tests}")
        
        print("FINISH TEST TODDLER")



    # CLOCKWISE
    if enable_test_clockwise:
        print("START  TEST CLOCKWISE")
        h_clockwise = HanoiTowerProblem(version='clockwise')

        # Check isValid
        assert h_clockwise.isValid('AA', 2, 'A', 'B') == False
        assert h_clockwise.isValid('AA', 1, 'A', 'B') == True
        assert h_clockwise.isValid('AA', 1, 'A', 'C') == False
        assert h_clockwise.isValid('CA', 1, 'C', 'A') == True
        assert h_clockwise.isValid('CA', 1, 'C', 'B') == False

        # Check checkMove
        assert h_clockwise.checkMove('AA', 1, 'A', 'B') == 0
        assert h_clockwise.checkMove('AA', -1, 'A', 'B') == 1
        assert h_clockwise.checkMove('AA', 130, 'A', 'B') == 1
        assert h_clockwise.checkMove('AA', 1, 'B', 'A') == 2
        assert h_clockwise.checkMove('AA', 1, 'A', 'D') == 3
        assert h_clockwise.checkMove('DA', 1, 'D', 'A') == 3
        assert h_clockwise.checkMove('AA', 1, 'A', 'A') == 4
        assert h_clockwise.checkMove('AA', 1, 'A', 'C') == 6
        assert h_clockwise.checkMove('CA', 1, 'C', 'A') == 0
        assert h_clockwise.checkMove('CA', 1, 'C', 'B') == 6
        assert h_clockwise.checkMove('BA', 2, 'A', 'B') == 7
        assert h_clockwise.checkMove('AA', 2, 'A', 'B') == 8

        # Check getMiMoves
        assert h_clockwise.getMinMoves('AA', 'BB') == 5
        assert h_clockwise.getMinMoves('AAA', 'BBB') == 15
        assert h_clockwise.getMinMoves('AA', 'CC') == 7
        assert h_clockwise.getMinMoves('AA', 'AC') == 5
        assert h_clockwise.getMinMoves('AAA', 'ABC') == 18
        assert h_clockwise.getMinMoves('AAAA', 'CBCC') == 55

        # Check getAvailableMovesIn
        assert h_clockwise.getAvailableMovesIn('A') != \
            ['1:AB', '1:AC']
        assert h_clockwise.getAvailableMovesIn('A') == \
            ['1:AB']
        assert h_clockwise.getAvailableMovesIn('AA') != \
            ['1:AB', '1:AC']
        assert h_clockwise.getAvailableMovesIn('AA') == \
            ['1:AB']
        assert h_clockwise.getAvailableMovesIn('AB') != \
            ['1:AB', '1:AC', '2:BC']
        assert h_clockwise.getAvailableMovesIn('AB') == \
            ['1:AB', '2:BC']
        assert h_clockwise.getAvailableMovesIn('AAA') != \
            ['1:AB', '1:AC']
        assert h_clockwise.getAvailableMovesIn('AAA') == \
            ['1:AB']
        assert h_clockwise.getAvailableMovesIn('ABB') != \
            ['1:AB', '1:AC', '2:BC']
        assert h_clockwise.getAvailableMovesIn('ABB') == \
            ['1:AB', '2:BC']
        assert h_clockwise.getAvailableMovesIn('ABC') != \
            ['1:AB', '1:AC', '2:BC']
        assert h_clockwise.getAvailableMovesIn('ABC') == \
            ['1:AB', '2:BC']


        if enable_advanced_tests:
            # Random tests
            for t in range(1, num_tests + 1):
                for n in range(1, n_max + 1):
                    # get random configs
                    initial = get_input_from('general', n, seed, 1)
                    final = get_input_from('general', n,  seed, 2)

                    # Check getMovesList
                    try:
                        opt_sol = h_clockwise.getMovesList(initial, final)
                        assert h_clockwise.checkSol(opt_sol, initial, final) == ('admissible', None)
                    except AssertionError:
                        print("AssertionError in clockwise -> getMovesList()")
                        print(f"initial: {initial}")
                        print(f"final:   {final}")
                        print(f"sol: {opt_sol}")
                        for e in opt_sol:
                            print(e)
                        exit(0)

                    # Check getNotOptimalSol
                    for _ in range(num_tests_not_optimal):
                        try:
                            not_opt_sol = h_clockwise.getNotOptimalSol(initial, final, size_shorter)
                            adm, info = h_clockwise.checkSol(not_opt_sol, initial, final) 
                            assert adm == 'admissible'
                        except AssertionError:
                            print("AssertionError in clockwise -> getNotOptimalSol()")
                            print(f"initial: {initial}")
                            print(f"final:   {final}")
                            print(f"sol: {not_opt_sol}")
                            for e in not_opt_sol:
                                print(e)
                            exit(0)

                    # Check correctness min_moves optimized
                    fast = h_clockwise.getMinMoves(initial, final, True)
                    slow = h_clockwise.getMinMoves(initial, final, False)
                    assert fast == slow
                if print_feedback:
                    print(f"-> finish test {t}/{num_tests}")
        
        print("FINISH TEST CLOCKWISE")
