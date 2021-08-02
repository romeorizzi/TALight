#!/usr/bin/env python3
import sys, random
sys.setrecursionlimit(1000000)



PEGS_LIST = ['A', 'B', 'C']



class ConfigGenerator():
    def __init__(self, seed = 0):
        random.seed(seed)
        

    def getConfigs(self, start, final, n):
        """Assume valid config for start and final"""
        if start[:4] == 'all_':
            if final[:4] == 'all_':
                if n == -1:
                    return (None, None, 'n_not_valid')
                else:
                    return (self.getTower(start[4], n), \
                            self.getTower(final[4], n), \
                            None)
            else:
                new_n = len(final)
                return (self.getTower(start[4], new_n), \
                        final, \
                        None)
        else:
            if final[:4] == 'all_':
                new_n = len(start)
                return (start, \
                        self.getTower(final[4], new_n), \
                        None)
            else:
                if len(start) != len(final):
                    return None, None, 'different_len'
                else:
                    return start, final, None


    def getTower(self, type, n):
        """Generate a n-tower of type 'A', 'B', or 'C'"""
        assert n > 0
        assert type in PEGS_LIST
        
        return type * n


    def setSeed(self, seed):
        """Reset RndGenerator"""
        random.seed(seed)


    def getRandom(self, n):
        """Generate a config from previously initialized RndGenerator"""
        config = ''
        for _ in range(n):
            config += random.choice(PEGS_LIST)
        return config



class HanoiState():
    def __init__(self, initial):
        # Note: I use a sentinel in 0 position
        self.current = ["*"] + list(initial)
        self.turn = 0
        self.last_disk = 1 # for Toddler version
    

    def getTowerSize(self):
        return len(self.current) - 1
    

    def getString(self):
        return ''.join(self.current[1:])
    

    def update(self, disk, target):
        """Assume valid disk"""
        assert disk > 0 and disk < len(self.current)
        
        self.current[disk] = target
        self.turn += 1
        self.last_disk = disk
    

    def of(self, disk):
        return self.current[disk]
    

    def isEqualTo(self, config):
        return self.getString() == config



class HanoiTowerProblem():
    """
    Move Format: {disk}:{from_peg}{to_peg} with bracked omitted
    Example: move disk1 from pegA to pegB == 1:AB
    """
    def __init__(self, version):
        # All
        assert version == 'classic' or version == 'toddler' or version == 'clockwise'
        self.version = version          # classic|toddler|clockwise
        self.moves = list()             # for getMoveList
        self.enable_n_moves_of = False  # for enable n_moves_of
        self.n_moves_of = list()        # for getMinMovesOf

        # toddler version
        # Note: in this version move-i odd -> Daddy; move-i+1 -> Toddler

        # clockwise version
        self.mem = dict()               # for  __getMinMoves_clockwise memoizzation


    # PUBLIC INTERFACE 
    def generateMoveFrom(self, disk, current, target):
        """Generate a move string from info"""
        return f"{disk}:{current}{target}"
    

    def parseMove(self, move):
        """Extract the info from the move string"""
        disk, (c, t) = move.split(":")
        return int(disk), c, t


    def checkMove(self, state, disk, current, target):
        """
        Assume valid state
        Return: Success, ErrorCode
        """
        assert isinstance(state, HanoiState)

        if disk > state.getTowerSize() or disk < 1:
            return False, 1     # "Invalid disk: not exist"
        if current not in PEGS_LIST or \
           target not in PEGS_LIST:
           return False, 2      # "Invalid Peg: not exist"
        if current == target:
            return False, 3     # "Invalid move: current and target can't be equal"
        if state.of(disk) != current:
            return False, 4     # "Wrong current or state: they don't coincide"
        if self.version == 'toddler':
            # Assume that in all odd turns, Toddler plays
            if disk == state.last_disk and state.turn % 2 == 1:
                return False, 5 # "Invalid move: Toddler can't move last disk"
        if self.version == 'clockwise':
            if target != self.__getNextPeg(current):
                return False, 6 # "Invalid move: can't make a counterclockwise move"
        for i in range(disk-1, 0, -1):
            #Note: this can be optimized using getAvailableMovesIn()
            if state.current[i] == target:
                return False, 7 # "Invalid move: can't move big disk on small disk"
            if state.of(i) == state.of(disk):
                return False, 8 # "Invalid disk: is blocked"
        return True, 0          # "Correct"

    
    def checkMoveList(self, move_list, initial, final):
        """Check if the move list is admissible or not"""
        state = HanoiState(initial)             # state class
        states_occ = {state.getString() : 1}    # state occurences
        
        # check moves correctness
        for move in move_list:
            # check move
            d, c, t = self.parseMove(move)
            success, errorCode = self.checkMove(state, d, c, t)
            if not success:
                return 'move_wrong', (move, errorCode)
            # update state and occurences
            state.update(d, t)
            # if state.current is not in states_occ, insert it with occ=1 else occ+=1
            states_occ[state.getString()] = states_occ.get(state.getString(), 0) + 1
        
        # check final correctness
        if not state.isEqualTo(final):
            return 'final_wrong', state
        
        # check loops in move_list
        occ = {k:v for k,v in states_occ.items() if v > 1}
        if len(occ) != 0:
            return 'admissible', occ
        return 'admissible', None


    def getAvailableMovesIn(self, state):
        """ Assume valid state"""
        assert isinstance(state, HanoiState)

        move_list = list()
        blocked = {i:False for i in PEGS_LIST}
        
        for disk in range(1, state.getTowerSize()+1):
            # Check if the i-disk is blocked
            if not blocked[state.of(disk)]:
                # Get others pegs
                for peg in self.__getPegsFrom(state.of(disk)):
                    # Check if can move disk in this peg
                    if not blocked[peg]:
                        if self.version == 'toddler':
                            # Assume that in all odd turns, Toddler plays
                            if disk == state.last_disk and state.turn % 2 == 1:
                                continue
                        elif self.version == 'clockwise':
                            if peg != self.__getNextPeg(state.of(disk)):
                                continue
                        # Add valid move
                        move_list.append(f"{disk}:{state.of(disk)}{peg}")
            # Blocking
            blocked[state.of(disk)] = True
            
            # Check if all other moves are blocked
            if all(v == True for v in blocked.values()):
                break
        
        return move_list


    def getMovesList(self, initial, final):
        """
        Return the optimal moves list
        Note1: the length of initial must be equal to the length of final
        Note2: the return list is a pointer
        """
        assert len(initial) == len(final)

        # reset
        self.moves.clear()
        self.n_moves_of = [0] * (len(initial) + 1)

        if self.version == 'classic':
            self.__move_classic(initial, final)
        
        elif self.version == 'toddler':
            self.__move_toddler(initial, final)
        
        elif self.version == 'clockwise':
            self.__move_clockwise(initial, final)
        
        return self.moves


    def getMinMoves(self, initial, final, optimized=True):
        """
        Return the optimal minimum number of moves
        Note1: in Toddler version assume always that Toddler make worst move.
        Note2: the length of initial must be equal to the length of final
        """
        assert len(initial) == len(final)

        if optimized:
            if self.version == 'classic':
                return self.__getMinMoves_classic(initial, final)
            
            if self.version == 'toddler':
                return self.__getMinMoves_toddler(initial, final)
            
            if self.version == 'clockwise':
                # self.mem.clear() # If u want reset 
                return self.__getMinMoves_clockwise(initial, final)
        else:
            self.getMovesList(initial, final)
            return len(self.moves)


    def getMinMovesOf(self, initial, final, disk):
        """
        Note1: the length of initial must be equal to the length of final
        Note2: the disk must be valid
        """
        assert len(initial) == len(final)
        assert disk > 0 and disk <= len(initial)

        self.enable_n_moves_of = True
        self.getMovesList(initial, final)
        n = self.n_moves_of[disk]
        self.enable_n_moves_of = False
        return n
    

    def getNotOptimalMovesList(self, initial, final, desired_size):
        self.getMovesList(initial, final)
        sol = self.moves
        diff = desired_size - len(sol)

        # if desired_size is too small return optimal solution
        if diff <= 0 or len(sol) == 0:
            return sol
        
        if self.version == 'toddler':
            i = 2
            state = HanoiState(initial)
            while i < len(sol) and diff >= 3:
                d, c, t = self.parseMove(sol[i])
                state.update(d, t)
                # search Daddy move with disk 1
                if d == 1 and state.turn % 2 == 0:
                    # get the support peg
                    s = self.__getPegFrom(c, t)
                    blocked = {i:False for i in PEGS_LIST}
                    blocked[s] = True
                    # search first bigger disk not blocked
                    for big_d in range(2, state.getTowerSize()+1):
                        # get potentially peg bigger disk
                        x = state.of(big_d)
                        if blocked[x] == False: # optimal case
                            # get the peg different from x and s
                            y = self.__getPegFrom(x, s)
                            sol[i] = f"{d}:{c}{s}"
                            sol.insert(i+1, f"{big_d}:{x}{y}")
                            sol.insert(i+2, f"{big_d}:{y}{x}")
                            sol.insert(i+3, f"{d}:{s}{t}")
                            diff -= 3
                            i += 3
                            break
                        else:
                            blocked[x] = True
                            # Check if all other moves are blocked
                            if all(v == True for v in blocked.values()):
                                break
                else:
                    i += 1
        else:
            i = 0
            while diff > 0:
                d, c, t = self.parseMove(sol[i])
                if d == 1 and random.randint(1,10) > 2:
                    if self.version == 'classic':
                        s = self.__getPegFrom(c, t)
                        sol[i] = f"{d}:{c}{s}"
                        sol.insert(i+1, f"{d}:{s}{t}")
                        diff = diff - 1
                        if diff <= 0:
                            break
                        # deliberately not incrementing by 1+1 to add randomness
                    elif self.version == 'clockwise':
                        s = self.__getNextPeg(t)
                        sol.insert(i+1, f"{d}:{t}{s}")
                        sol.insert(i+2, f"{d}:{s}{c}")
                        sol.insert(i+3, f"{d}:{c}{t}")
                        diff = diff - 3
                        # deliberately not incrementing by 1+3 to add randomness
                        if diff < 3:
                            break
                i = i + 1
                if i >= len(sol):
                    i = 0
        return sol


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
        self.moves.append(f"{disk}:{current}{target}")
        
        if self.enable_n_moves_of:
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


    # PRIVATE TODDLER
    def __move_toddler(self, initial, final):
        # get optimal moves list
        self.__move_classic(initial, final)
        # get first optimal moves
        if len(self.moves) > 1:
            d, c, t = self.parseMove(self.moves[0])
            # If Daddy move first with disk=1, he have the control of the game.
            # So the solution is equal to optimal solution for classic version.
            # Otherwise I assume that child do the worst move (on second move),
            # and Daddy make the rollback
            if d != 1:
                # Toddler now can make the worst move, and he make it...
                d, c, t = self.parseMove(self.moves[1])
                s = self.__getPegFrom(c, t)
                # change t in move {d}:{c}{t}
                self.moves[1] = self.moves[1][:-1] + s
                # ... so, daddy add a moves for adjust the wrong move of toddler.
                self.moves.insert(2, f"{1}:{s}{t}")
                self.n_moves_of[1] += 1



    def __getMinMoves_toddler(self, initial, final):
        self.getMovesList(initial, final)
        return len(self.moves)


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



# HANOI TOWER PROBLEM GENERAL
def general_test(h, enable_advanced_tests, print_feedback, seed, n_max, num_tests, num_tests_not_optimal, size_offset=-1):
    assert isinstance(h, HanoiTowerProblem)

    # TEST generateMoveFrom() and parseMove()
    assert h.generateMoveFrom(130, 'C', 'A') == '130:CA'
    assert h.generateMoveFrom(10, 'A', 'C') == '10:AC'
    assert h.generateMoveFrom(1291, 'B', 'A') == '1291:BA'

    assert h.parseMove('130:CA') == (130, 'C', 'A')
    assert h.parseMove('10:AC') == (10, 'A', 'C')
    assert h.parseMove('1291:BA') == (1291, 'B', 'A')

    for s in ['1:AB', '2:BC', '130:CA']:
        d, c, t = h.parseMove(s)
        assert s == h.generateMoveFrom(d, c, t)

    
    # TEST checkMove()
    assert h.checkMove(HanoiState('AA'), 1,   'A', 'B') == \
            (True, 0) # Correct
    assert h.checkMove(HanoiState('AA'), -1,  'A', 'B') == \
            (False, 1) # "Invalid disk: not exist"
    assert h.checkMove(HanoiState('AA'), 130, 'A', 'B') == \
            (False, 1) # "Invalid disk: not exist"
    assert h.checkMove(HanoiState('AA'), 1,   'A', 'D') == \
            (False, 2) # "Invalid Peg: not exist"
    assert h.checkMove(HanoiState('DA'), 1,   'D', 'A') == \
            (False, 2) # "Invalid Peg: not exist"
    assert h.checkMove(HanoiState('DA'), 1,   'D', 'E') == \
            (False, 2) # "Invalid Peg: not exist"
    assert h.checkMove(HanoiState('AA'), 1,   'A', 'A') == \
            (False, 3) # "Invalid move: current and target can't be equal"
    assert h.checkMove(HanoiState('AA'), 1,   'B', 'A') == \
            (False, 4) # "Wrong current or state: they don't coincide"
    assert h.checkMove(HanoiState('BA'), 2,   'A', 'B') == \
            (False, 7) # "Invalid move: can't move big disk on small disk"
    assert h.checkMove(HanoiState('AA'), 2,   'A', 'B') == \
            (False, 8) # "Invalid disk: is blocked"


    if enable_advanced_tests:
        gen = ConfigGenerator()

        # Random tests
        for t in range(1, num_tests + 1):
            for n in range(1, n_max + 1):
                # get random configs
                gen.setSeed(seed)
                initial = gen.getRandom(n)
                final = gen.getRandom(n)

                # TEST getMovesList()
                try:
                    opt_sol = h.getMovesList(initial, final).copy()
                    assert h.checkMoveList(opt_sol, initial, final) == ('admissible', None)
                except AssertionError:
                    print("AssertionError in -> getMovesList()")
                    print(f"initial: {initial}")
                    print(f"final:   {final}")
                    print(f"sol: {opt_sol}")
                    exit(0)

                # TEST getNotOptimalMovesList()
                size_longer = len(opt_sol) + (random.randint(0, 20) if size_offset == -1 else size_offset)
                for _ in range(num_tests_not_optimal):
                    not_opt_sol = h.getNotOptimalMovesList(initial, final, size_longer)
                    adm, info = h.checkMoveList(not_opt_sol, initial, final)
                    try:
                        assert adm == 'admissible'
                    except AssertionError:
                        print("AssertionError in -> getNotOptimalSol() [admissible check]")
                        print(f"size_offset: {size_offset}")
                        print(f"initial: {initial}")
                        print(f"final:   {final}")
                        print(f"opt_sol:     {opt_sol}")
                        print(f"not_opt_sol: {not_opt_sol}")
                        print("info: ", info)
                        exit(0)
                    try:
                        assert (info != None or len(not_opt_sol) == 0)
                    except AssertionError:
                        # print("AssertionError in -> getNotOptimalSol() [info check]")
                        # print(f"size_offset: {size_offset}")
                        # print(f"initial: {initial}")
                        # print(f"final:   {final}")
                        # print(f"opt_sol:     {opt_sol}")
                        # print(f"not_opt_sol: {not_opt_sol}")
                        # print("info: ", info)
                        if not continue_if_info_is_none:
                            exit(0)

                # TEST correctness min_moves() optimized
                fast = h.getMinMoves(initial, final, True)
                slow = h.getMinMoves(initial, final, False)
                assert fast == slow
            if print_feedback:
                print(f"-> finish test {t}/{num_tests}")



# TESTS
if __name__ == "__main__":
    enable_test_ConfigGenerator = 1
    enable_test_HanoiState = 1
    
    enable_test_classic = 1
    enable_test_toddler = 1
    enable_test_clockwise = 1


    # HanoiTowerProblem tests addictional option
    enable_advanced_tests = 1
    print_feedback = 1
    seed = 13000
    n_max = 10
    num_tests = 50
    num_tests_not_optimal = 10
    size_offset = 10
    continue_if_info_is_none = True


    # CONFIG GENERATOR
    if enable_test_ConfigGenerator:
        print("START  CONFIG GENERATOR TEST")

        gen = ConfigGenerator()

        assert gen.getTower('A', 1) == 'A'
        assert gen.getTower('B', 6) == 'BBBBBB'
        assert gen.getTower('C', 10) == 'CCCCCCCCCC'

        assert gen.getRandom(3) == 'BBA'
        assert gen.getRandom(3) == 'BCB'
        assert gen.getRandom(3) != 'BCB'

        gen.setSeed(0)
        assert gen.getRandom(3) == 'BBA'
        assert gen.getRandom(3) == 'BCB'
        assert gen.getRandom(3) != 'BCB'

        gen.setSeed(13000)
        assert gen.getRandom(3) != 'BBA'
        assert gen.getRandom(3) == 'BCB'
        assert gen.getRandom(3) != 'BCB'

        assert gen.getConfigs('all_A', 'all_B', -1) == (None, None, 'n_not_valid')
        assert gen.getConfigs('all_A', 'all_C', 2) == ('AA', 'CC', None)
        assert gen.getConfigs('all_A', 'BBB', 10) == ('AAA', 'BBB', None)
        assert gen.getConfigs('AAAA', 'all_B', 10) == ('AAAA', 'BBBB', None)
        assert gen.getConfigs('AA', 'CC', 10) == ('AA', 'CC', None)
        assert gen.getConfigs('AAA', 'BBBB', -1) == (None, None, 'different_len')
    
        print("FINISH CONFIG GENERATOR TEST")



    # HANOI STATE
    if enable_test_HanoiState:
        print("START  HANOI STATE TEST")

        state = HanoiState('ABCC')
        state.update(1, 'C')
        assert state.current == ['*'] + list('CBCC')

        state.update(1, 'A')
        assert state.current == ['*'] + list('ABCC')
        assert state.last_disk == 1

        state.update(2, 'C')
        assert state.current == ['*'] + list('ACCC')
        assert state.last_disk == 2

        assert state.isEqualTo('ACCC')

        assert state.getTowerSize() == 4

        assert state.getString() == 'ACCC'

        assert state.of(1) == 'A'
        assert state.of(2) == 'C'
        assert state.of(3) == 'C'
        assert state.of(4) == 'C'

        print("FINISH HANOI STATE TEST")



    # CLASSIC
    if enable_test_classic:
        print("START  TEST CLASSIC")
        h_classic = HanoiTowerProblem(version='classic')


        # TEST checkMoveList()
        # print(h_classic.getMovesList('AA', 'CC'))
        moves = ['1:AB', '2:AC', '1:BC'] #optimal
        assert h_classic.checkMoveList(moves, 'AA', 'CC') == ('admissible', None)

        moves = ['1:AC', '1:CB', '2:AC', '1:BC'] # admissible without loops
        assert h_classic.checkMoveList(moves, 'AA', 'CC') == ('admissible', None)

        moves = ['1:AC', '1:CA', '1:AB', '2:AC', '1:BC'] # admissible with loops
        assert h_classic.checkMoveList(moves, 'AA', 'CC') == ('admissible', {'AA': 2})


        # TEST getMinMoves(), getMinMovesOf() and getMovesList()
        # print(h_classic.getMovesList('A','A'))
        assert h_classic.getMinMoves('A', 'A') == 0
        assert h_classic.getMinMovesOf('A', 'A', 1) == 0
        assert h_classic.getMovesList('A', 'A') == \
            []
        
        # print(h_classic.getMovesList('A','C'))
        assert h_classic.getMinMoves('A', 'C') == 1
        assert h_classic.getMinMovesOf('A', 'C', 1) == 1
        assert h_classic.getMovesList('A', 'C') == \
            ['1:AC']
        
        # print(h_classic.getMovesList('AA','CC'))
        assert h_classic.getMinMoves('AA', 'CC') == 3
        assert h_classic.getMinMovesOf('AA', 'CC', 1) == 2
        assert h_classic.getMinMovesOf('AA', 'CC', 2) == 1
        assert h_classic.getMovesList('AA', 'CC') == \
            ['1:AB', '2:AC', '1:BC']
        
        # print(h_classic.getMovesList('AAA','CCC'))
        assert h_classic.getMinMoves('AAA', 'CCC') == 7
        assert h_classic.getMinMovesOf('AAA', 'CCC', 1) == 4
        assert h_classic.getMinMovesOf('AAA', 'CCC', 2) == 2
        assert h_classic.getMinMovesOf('AAA', 'CCC', 3) == 1
        assert h_classic.getMovesList('AAA', 'CCC') == \
            ['1:AC', '2:AB', '1:CB', '3:AC', '1:BA', '2:BC', '1:AC']
        
        # print(h_classic.getMovesList('AAAA','CCCC'))
        assert h_classic.getMinMoves('AAAA', 'CCCC') == 15
        assert h_classic.getMinMovesOf('AAAA', 'CCCC', 1) == 8
        assert h_classic.getMinMovesOf('AAAA', 'CCCC', 2) == 4
        assert h_classic.getMinMovesOf('AAAA', 'CCCC', 3) == 2
        assert h_classic.getMinMovesOf('AAAA', 'CCCC', 4) == 1
        assert h_classic.getMovesList('AAAA', 'CCCC') == \
            ['1:AB', '2:AC', '1:BC', '3:AB', '1:CA', '2:CB', '1:AB', '4:AC', '1:BC', '2:BA', '1:CA', '3:BC', '1:AB', '2:AC', '1:BC']
        
        # print(h_classic.getMovesList('AA','BB'))
        assert h_classic.getMinMoves('AA', 'BB') == 3
        assert h_classic.getMinMovesOf('AA', 'BB', 1) == 2
        assert h_classic.getMinMovesOf('AA', 'BB', 2) == 1
        assert h_classic.getMovesList('AA', 'BB') == \
            ['1:AC', '2:AB', '1:CB']
        
        # print(h_classic.getMovesList('AAA','BBB'))
        assert h_classic.getMinMoves('AAA', 'BBB') == 7
        assert h_classic.getMinMovesOf('AAA', 'BBB', 1) == 4
        assert h_classic.getMinMovesOf('AAA', 'BBB', 2) == 2
        assert h_classic.getMinMovesOf('AAA', 'BBB', 3) == 1
        assert h_classic.getMovesList('AAA', 'BBB') == \
            ['1:AB', '2:AC', '1:BC', '3:AB', '1:CA', '2:CB', '1:AB']
        
        # print(h_classic.getMovesList('AA','AC'))
        assert h_classic.getMinMoves('AA', 'AC') == 3
        assert h_classic.getMinMovesOf('AA', 'AC', 1) == 2
        assert h_classic.getMinMovesOf('AA', 'AC', 2) == 1
        assert h_classic.getMovesList('AA', 'AC') == \
            ['1:AB', '2:AC', '1:BA']
        
        # print(h_classic.getMovesList('AAA','ABC'))
        assert h_classic.getMinMoves('AAA', 'ABC') == 5
        assert h_classic.getMinMovesOf('AAA', 'ABC', 1) == 3
        assert h_classic.getMinMovesOf('AAA', 'ABC', 2) == 1
        assert h_classic.getMinMovesOf('AAA', 'ABC', 3) == 1
        assert h_classic.getMovesList('AAA', 'ABC') == \
            ['1:AC', '2:AB', '1:CB', '3:AC', '1:BA']
        
        # print(h_classic.getMovesList('AAAA','CBCC'))
        assert h_classic.getMinMoves('AAAA', 'CBCC') == 14
        assert h_classic.getMinMovesOf('AAAA', 'CBCC', 1) == 7
        assert h_classic.getMinMovesOf('AAAA', 'CBCC', 2) == 4
        assert h_classic.getMinMovesOf('AAAA', 'CBCC', 3) == 2
        assert h_classic.getMinMovesOf('AAAA', 'CBCC', 4) == 1
        assert h_classic.getMovesList('AAAA', 'CBCC') == \
            ['1:AB', '2:AC', '1:BC', '3:AB', '1:CA', '2:CB', '1:AB', '4:AC', '1:BC', '2:BA', '1:CA', '3:BC', '1:AC', '2:AB']
        
        # print(h_classic.getMovesList('AC','AA'))
        assert h_classic.getMinMoves('AC', 'AA') == 3
        assert h_classic.getMinMovesOf('AC', 'AA', 1) == 2
        assert h_classic.getMinMovesOf('AC', 'AA', 2) == 1
        assert h_classic.getMovesList('AC', 'AA') == \
            ['1:AB', '2:CA', '1:BA']
        
        # print(h_classic.getMovesList('ABC','AAA'))
        assert h_classic.getMinMoves('ABC', 'AAA') == 5
        assert h_classic.getMinMovesOf('ABC', 'AAA', 1) == 3
        assert h_classic.getMinMovesOf('ABC', 'AAA', 2) == 1
        assert h_classic.getMinMovesOf('ABC', 'AAA', 3) == 1
        assert h_classic.getMovesList('ABC', 'AAA') == \
            ['1:AB', '3:CA', '1:BC', '2:BA', '1:CA']

        # print(h_classic.getMovesList('CBCC','AAAA'))
        assert h_classic.getMinMoves('CBCC', 'AAAA') == 14
        assert h_classic.getMinMovesOf('CBCC', 'AAAA', 1) == 7
        assert h_classic.getMinMovesOf('CBCC', 'AAAA', 2) == 4
        assert h_classic.getMinMovesOf('CBCC', 'AAAA', 3) == 2
        assert h_classic.getMinMovesOf('CBCC', 'AAAA', 4) == 1
        assert h_classic.getMovesList('CBCC', 'AAAA') == \
            ['2:BA', '1:CA', '3:CB', '1:AC', '2:AB', '1:CB', '4:CA', '1:BA', '2:BC', '1:AC', '3:BA', '1:CB', '2:CA', '1:BA']


        # TEST getAvailableMovesIn()
        assert h_classic.getAvailableMovesIn(HanoiState('A')) == \
            ['1:AB', '1:AC']
        assert h_classic.getAvailableMovesIn(HanoiState('AA')) == \
            ['1:AB', '1:AC']
        assert h_classic.getAvailableMovesIn(HanoiState('AB')) == \
            ['1:AB', '1:AC', '2:BC']
        assert h_classic.getAvailableMovesIn(HanoiState('AAA')) == \
            ['1:AB', '1:AC']
        assert h_classic.getAvailableMovesIn(HanoiState('ABB')) == \
            ['1:AB', '1:AC', '2:BC']
        assert h_classic.getAvailableMovesIn(HanoiState('ABC')) == \
            ['1:AB', '1:AC', '2:BC']
        

        # TESTS general
        general_test(h_classic, enable_advanced_tests, print_feedback, seed, n_max, num_tests, num_tests_not_optimal, size_offset)
        print("FINISH TEST CLASSIC")



    # TODDLER
    if enable_test_toddler:
        print("START  TEST TODDLER")
        h_toddler = HanoiTowerProblem(version='toddler')


        # TEST checkMoveList()
        # print(h_toddler.getMovesList('AA', 'CC'))
        moves = ['1:AB', '2:AC', '1:BC'] #optimal
        assert h_toddler.checkMoveList(moves, 'AA', 'CC') == ('admissible', None)

        moves = ['1:AC', '1:CB', '2:AC', '1:BC'] # admissible without loops
        assert h_toddler.checkMoveList(moves, 'AA', 'CC') == ('move_wrong', ('1:CB', 5))


        # TEST getMinMoves(), getMinMovesOf() and getMovesList()
        # print(h_toddler.getMovesList('A', 'A'))
        assert h_toddler.getMinMoves('A', 'A') == 0
        assert h_toddler.getMinMovesOf('A', 'A', 1) == 0
        assert h_toddler.getMovesList('A', 'A') == \
            []
        
        # print(h_toddler.getMovesList('A', 'C'))
        assert h_toddler.getMinMoves('A', 'C') == 1
        assert h_toddler.getMinMovesOf('A', 'C', 1) == 1
        assert h_toddler.getMovesList('A', 'C') == \
            ['1:AC']
        
        # print(h_toddler.getMovesList('AA', 'CC'))
        assert h_toddler.getMinMoves('AA', 'CC') == 3
        assert h_toddler.getMinMovesOf('AA', 'CC', 1) == 2
        assert h_toddler.getMinMovesOf('AA', 'CC', 2) == 1
        assert h_toddler.getMovesList('AA', 'CC') == \
            ['1:AB', '2:AC', '1:BC']
        
        # print(h_toddler.getMovesList('AAA', 'CCC'))
        assert h_toddler.getMinMoves('AAA', 'CCC') == 7
        assert h_toddler.getMinMovesOf('AAA', 'CCC', 1) == 4
        assert h_toddler.getMinMovesOf('AAA', 'CCC', 2) == 2
        assert h_toddler.getMinMovesOf('AAA', 'CCC', 3) == 1
        assert h_toddler.getMovesList('AAA', 'CCC') == \
            ['1:AC', '2:AB', '1:CB', '3:AC', '1:BA', '2:BC', '1:AC']
        
        # print(h_toddler.getMovesList('AAAA', 'CCCC'))
        assert h_toddler.getMinMoves('AAAA', 'CCCC') == 15
        assert h_toddler.getMinMovesOf('AAAA', 'CCCC', 1) == 8
        assert h_toddler.getMinMovesOf('AAAA', 'CCCC', 2) == 4
        assert h_toddler.getMinMovesOf('AAAA', 'CCCC', 3) == 2
        assert h_toddler.getMinMovesOf('AAAA', 'CCCC', 4) == 1
        assert h_toddler.getMovesList('AAAA', 'CCCC') == \
            ['1:AB', '2:AC', '1:BC', '3:AB', '1:CA', '2:CB', '1:AB', '4:AC', '1:BC', '2:BA', '1:CA', '3:BC', '1:AB', '2:AC', '1:BC']

        # print(h_toddler.getMovesList('AA', 'BB'))
        assert h_toddler.getMinMoves('AA', 'BB') == 3
        assert h_toddler.getMinMovesOf('AA', 'BB', 1) == 2
        assert h_toddler.getMinMovesOf('AA', 'BB', 2) == 1
        assert h_toddler.getMovesList('AA', 'BB') == \
            ['1:AC', '2:AB', '1:CB']
        
        # print(h_toddler.getMovesList('AAA', 'BBB'))
        assert h_toddler.getMinMoves('AAA', 'BBB') == 7
        assert h_toddler.getMinMovesOf('AAA', 'BBB', 1) == 4
        assert h_toddler.getMinMovesOf('AAA', 'BBB', 2) == 2
        assert h_toddler.getMinMovesOf('AAA', 'BBB', 3) == 1
        assert h_toddler.getMovesList('AAA', 'BBB') == \
            ['1:AB', '2:AC', '1:BC', '3:AB', '1:CA', '2:CB', '1:AB']
        
        # print(h_toddler.getMovesList('AA', 'AC'))
        assert h_toddler.getMinMoves('AA', 'AC') == 3
        assert h_toddler.getMinMovesOf('AA', 'AC', 1) == 2
        assert h_toddler.getMinMovesOf('AA', 'AC', 2) == 1
        assert h_toddler.getMovesList('AA', 'AC') == \
            ['1:AB', '2:AC', '1:BA']
        
        # print(h_toddler.getMovesList('AAA', 'ABC'))
        assert h_toddler.getMinMoves('AAA', 'ABC') == 5
        assert h_toddler.getMinMovesOf('AAA', 'ABC', 1) == 3
        assert h_toddler.getMinMovesOf('AAA', 'ABC', 2) == 1
        assert h_toddler.getMinMovesOf('AAA', 'ABC', 3) == 1
        assert h_toddler.getMovesList('AAA', 'ABC') == \
            ['1:AC', '2:AB', '1:CB', '3:AC', '1:BA']
        
        # print(h_toddler.getMovesList('AAAA', 'CBCC'))
        assert h_toddler.getMinMoves('AAAA', 'CBCC') == 14
        assert h_toddler.getMinMovesOf('AAAA', 'CBCC', 1) == 7
        assert h_toddler.getMinMovesOf('AAAA', 'CBCC', 2) == 4
        assert h_toddler.getMinMovesOf('AAAA', 'CBCC', 3) == 2
        assert h_toddler.getMinMovesOf('AAAA', 'CBCC', 4) == 1
        assert h_toddler.getMovesList('AAAA', 'CBCC') == \
            ['1:AB', '2:AC', '1:BC', '3:AB', '1:CA', '2:CB', '1:AB', '4:AC', '1:BC', '2:BA', '1:CA', '3:BC', '1:AC', '2:AB']
        
        # print(h_toddler.getMovesList('AC', 'AA'))
        assert h_toddler.getMinMoves('AC', 'AA') == 3
        assert h_toddler.getMinMovesOf('AC', 'AA', 1) == 2
        assert h_toddler.getMinMovesOf('AC', 'AA', 2) == 1
        assert h_toddler.getMovesList('AC', 'AA') == \
            ['1:AB', '2:CA', '1:BA']
        
        # print(h_toddler.getMovesList('ABC', 'AAA'))
        assert h_toddler.getMinMoves('ABC', 'AAA') == 5
        assert h_toddler.getMinMovesOf('ABC', 'AAA', 1) == 3
        assert h_toddler.getMinMovesOf('ABC', 'AAA', 2) == 1
        assert h_toddler.getMinMovesOf('ABC', 'AAA', 3) == 1
        assert h_toddler.getMovesList('ABC', 'AAA') == \
            ['1:AB', '3:CA', '1:BC', '2:BA', '1:CA']


        # print(h_toddler.getMovesList('CBCC', 'AAAA'))
        assert h_toddler.getMinMoves('CBCC', 'AAAA') == 15
        assert h_toddler.getMinMovesOf('CBCC', 'AAAA', 1) == 8
        assert h_toddler.getMinMovesOf('CBCC', 'AAAA', 2) == 4
        assert h_toddler.getMinMovesOf('CBCC', 'AAAA', 3) == 2
        assert h_toddler.getMinMovesOf('CBCC', 'AAAA', 4) == 1
        assert h_toddler.getMovesList('CBCC', 'AAAA') == \
            ['2:BA', '1:CB', '1:BA', '3:CB', '1:AC', '2:AB', '1:CB', '4:CA', '1:BA', '2:BC', '1:AC', '3:BA', '1:CB', '2:CA', '1:BA']
        
        # print(h_toddler.getMovesList('AABB', 'CBBA'))
        assert h_toddler.getMinMoves('AABB', 'CBBA', False) == 12
        assert h_toddler.getMinMovesOf('AABB', 'CBBA', 1) == 6
        assert h_toddler.getMinMovesOf('AABB', 'CBBA', 2) == 3
        assert h_toddler.getMinMovesOf('AABB', 'CBBA', 3) == 2
        assert h_toddler.getMinMovesOf('AABB', 'CBBA', 4) == 1
        assert h_toddler.getMovesList('AABB', 'CBBA') == \
            ['3:BC', '1:AC', '1:CB', '2:AC', '1:BC', '4:BA', '1:CB', '2:CA', '1:BA', '3:CB', '1:AC', '2:AB']
        

        # TEST getAvailableMovesIn()
        state = HanoiState('A') #Daddy
        assert h_toddler.getAvailableMovesIn(state) == \
            ['1:AB', '1:AC']
        state = HanoiState('B') #Toddler
        state.update(1, 'A')
        assert h_toddler.getAvailableMovesIn(state) == \
            []

        state = HanoiState('AA') #Daddy
        assert h_toddler.getAvailableMovesIn(state) == \
            ['1:AB', '1:AC']
        state = HanoiState('BA') #Toddler
        state.update(1, 'A')
        assert h_toddler.getAvailableMovesIn(state) == \
            []
        state = HanoiState('AB') #Toddler
        state.update(2, 'C')
        assert h_toddler.getAvailableMovesIn(state) == \
            ['1:AB', '1:AC']

        state = HanoiState('AB') #Daddy
        assert h_toddler.getAvailableMovesIn(state) == \
            ['1:AB', '1:AC', '2:BC']
        state = HanoiState('CB') #Toddler
        state.update(1, 'A')
        assert h_toddler.getAvailableMovesIn(state) == \
            ['2:BC']
        state = HanoiState('AC') #Toddler
        state.update(2, 'B')
        assert h_toddler.getAvailableMovesIn(state) == \
            ['1:AB', '1:AC']


        state = HanoiState('AAA') #Daddy
        assert h_toddler.getAvailableMovesIn(state) == \
            ['1:AB', '1:AC']
        state = HanoiState('BAA') #Toddler
        state.update(1, 'A')
        assert h_toddler.getAvailableMovesIn(state) == \
            []
        state = HanoiState('ABA') #Toddler
        state.update(2, 'C')
        assert h_toddler.getAvailableMovesIn(state) == \
            ['1:AB', '1:AC']
        state = HanoiState('AAB') #Toddler
        state.update(3, 'C')
        assert h_toddler.getAvailableMovesIn(state) == \
            ['1:AB', '1:AC']


        # TEST checkMove()
        state = HanoiState('CA')
        state.update(1, 'A')
        assert h_toddler.checkMove(state, 1, 'A', 'B') == \
                (False, 5) # "Invalid move: Toddler can't move last disk"


        # TESTS general
        general_test(h_toddler, enable_advanced_tests, print_feedback, seed, n_max, num_tests, num_tests_not_optimal, size_offset)
        print("FINISH TEST TODDLER")



    # CLOCKWISE
    if enable_test_clockwise:
        print("START  TEST CLOCKWISE")
        h_clockwise = HanoiTowerProblem(version='clockwise')


        # TEST checkMoveList()
        # print(h_clockwise.getMovesList('AA', 'CC'))
        moves = ['1:AB', '1:BC', '2:AB', '1:CA', '2:BC', '1:AB', '1:BC'] #optimal
        assert h_clockwise.checkMoveList(moves, 'AA', 'CC') == ('admissible', None)

        moves = ['1:AB', '1:BC', '1:CA', '1:AB', '1:BC', '2:AB', '1:CA', '2:BC', '1:AB', '1:BC']
        assert h_clockwise.checkMoveList(moves, 'AA', 'CC') == ('admissible', {'AA': 2, 'BA': 2, 'CA': 2})

        moves = ['1:AC', '2:AB', '1:CA', '2:BC', '1:AB', '1:BC']
        assert h_clockwise.checkMoveList(moves, 'AA', 'CC') == ('move_wrong', ('1:AC', 6))


        # TEST getMinMoves(), getMinMovesOf() and getMovesList()
        # print(h_clockwise.getMovesList('A','A'))
        assert h_clockwise.getMinMoves('A', 'A') == 0
        assert h_clockwise.getMinMovesOf('A', 'A', 1) == 0
        assert h_clockwise.getMovesList('A', 'A') == \
            []
        
        # print(h_clockwise.getMovesList('A','C'))
        assert h_clockwise.getMinMoves('A', 'C') == 2
        assert h_clockwise.getMinMovesOf('A', 'C', 1) == 2
        assert h_clockwise.getMovesList('A', 'C') == \
            ['1:AB', '1:BC']
        
        # print(h_clockwise.getMovesList('AA','CC'))
        assert h_clockwise.getMinMoves('AA', 'CC') == 7
        assert h_clockwise.getMinMovesOf('AA', 'CC', 1) == 5
        assert h_clockwise.getMinMovesOf('AA', 'CC', 2) == 2
        assert h_clockwise.getMovesList('AA', 'CC') == \
            ['1:AB', '1:BC', '2:AB', '1:CA', '2:BC', '1:AB', '1:BC']
        
        # print(h_clockwise.getMovesList('AAA','CCC'))
        assert h_clockwise.getMinMoves('AAA', 'CCC') == 21
        assert h_clockwise.getMinMovesOf('AAA', 'CCC', 1) == 14
        assert h_clockwise.getMinMovesOf('AAA', 'CCC', 2) == 5
        assert h_clockwise.getMinMovesOf('AAA', 'CCC', 3) == 2
        assert h_clockwise.getMovesList('AAA', 'CCC') == \
            ['1:AB', '1:BC', '2:AB', '1:CA', '2:BC', '1:AB', '1:BC', '3:AB', '1:CA', '1:AB', '2:CA', '1:BC', '1:CA', '3:BC', '1:AB', '1:BC', '2:AB', '1:CA', '2:BC', '1:AB', '1:BC']
        
        # print(h_clockwise.getMovesList('AA','BB'))
        assert h_clockwise.getMinMoves('AA', 'BB') == 5
        assert h_clockwise.getMinMovesOf('AA', 'BB', 1) == 4
        assert h_clockwise.getMinMovesOf('AA', 'BB', 2) == 1
        assert h_clockwise.getMovesList('AA', 'BB') == \
            ['1:AB', '1:BC', '2:AB', '1:CA', '1:AB']
        
        # print(h_clockwise.getMovesList('AAA','BBB'))
        assert h_clockwise.getMinMoves('AAA', 'BBB') == 15
        assert h_clockwise.getMinMovesOf('AAA', 'BBB', 1) == 10
        assert h_clockwise.getMinMovesOf('AAA', 'BBB', 2) == 4
        assert h_clockwise.getMinMovesOf('AAA', 'BBB', 3) == 1
        assert h_clockwise.getMovesList('AAA', 'BBB') == \
            ['1:AB', '1:BC', '2:AB', '1:CA', '2:BC', '1:AB', '1:BC', '3:AB', '1:CA', '1:AB', '2:CA', '1:BC', '2:AB', '1:CA', '1:AB']
        
        # print(h_clockwise.getMovesList('AA','AC'))
        assert h_clockwise.getMinMoves('AA', 'AC') == 5
        assert h_clockwise.getMinMovesOf('AA', 'AC', 1) == 3
        assert h_clockwise.getMinMovesOf('AA', 'AC', 2) == 2
        assert h_clockwise.getMovesList('AA', 'AC') == \
            ['1:AB', '1:BC', '2:AB', '1:CA', '2:BC']
        
        # print(h_clockwise.getMovesList('AAA','ABC'))
        assert h_clockwise.getMinMoves('AAA', 'ABC') == 18
        assert h_clockwise.getMinMovesOf('AAA', 'ABC', 1) == 12
        assert h_clockwise.getMinMovesOf('AAA', 'ABC', 2) == 4
        assert h_clockwise.getMinMovesOf('AAA', 'ABC', 3) == 2
        assert h_clockwise.getMovesList('AAA', 'ABC') == \
            ['1:AB', '1:BC', '2:AB', '1:CA', '2:BC', '1:AB', '1:BC', '3:AB', '1:CA', '1:AB', '2:CA', '1:BC', '1:CA', '3:BC', '1:AB', '1:BC', '2:AB', '1:CA']
        
        # print(h_clockwise.getMovesList('AC','AA'))
        assert h_clockwise.getMinMoves('AC', 'AA') == 4
        assert h_clockwise.getMinMovesOf('AC', 'AA', 1) == 3
        assert h_clockwise.getMinMovesOf('AC', 'AA', 2) == 1
        assert h_clockwise.getMovesList('AC', 'AA') == \
            ['1:AB', '2:CA', '1:BC', '1:CA']
        
        # print(h_clockwise.getMovesList('ABC','AAA'))
        assert h_clockwise.getMinMoves('ABC', 'AAA') == 9
        assert h_clockwise.getMinMovesOf('ABC', 'AAA', 1) == 6
        assert h_clockwise.getMinMovesOf('ABC', 'AAA', 2) == 2
        assert h_clockwise.getMinMovesOf('ABC', 'AAA', 3) == 1
        assert h_clockwise.getMovesList('ABC', 'AAA') == \
            ['1:AB', '3:CA', '1:BC', '1:CA', '2:BC', '1:AB', '2:CA', '1:BC', '1:CA']


        # TEST getAvailableMovesIn()
        assert h_clockwise.getAvailableMovesIn(HanoiState('A')) != \
            ['1:AB', '1:AC']
        assert h_clockwise.getAvailableMovesIn(HanoiState('A')) == \
            ['1:AB']
        assert h_clockwise.getAvailableMovesIn(HanoiState('AA')) != \
            ['1:AB', '1:AC']
        assert h_clockwise.getAvailableMovesIn(HanoiState('AA')) == \
            ['1:AB']
        assert h_clockwise.getAvailableMovesIn(HanoiState('AB')) != \
            ['1:AB', '1:AC', '2:BC']
        assert h_clockwise.getAvailableMovesIn(HanoiState('AB')) == \
            ['1:AB', '2:BC']
        assert h_clockwise.getAvailableMovesIn(HanoiState('AAA')) != \
            ['1:AB', '1:AC']
        assert h_clockwise.getAvailableMovesIn(HanoiState('AAA')) == \
            ['1:AB']
        assert h_clockwise.getAvailableMovesIn(HanoiState('ABB')) != \
            ['1:AB', '1:AC', '2:BC']
        assert h_clockwise.getAvailableMovesIn(HanoiState('ABB')) == \
            ['1:AB', '2:BC']
        assert h_clockwise.getAvailableMovesIn(HanoiState('ABC')) != \
            ['1:AB', '1:AC', '2:BC']
        assert h_clockwise.getAvailableMovesIn(HanoiState('ABC')) == \
            ['1:AB', '2:BC']


        # TEST checkMove()
        state = HanoiState('AA')
        assert h_clockwise.checkMove(state, 1, 'A', 'B') == \
                (True, 0) # "Correct"
        assert h_clockwise.checkMove(state, 1, 'A', 'C') == \
                (False, 6) # "Invalid move: can't make a counterclockwise move"


        # TESTS general
        general_test(h_clockwise, enable_advanced_tests, print_feedback, seed, n_max, num_tests, num_tests_not_optimal, size_offset)
        print("FINISH TEST CLOCKWISE")
