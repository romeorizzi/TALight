#!/usr/bin/env python3

import random, copy
import re
from sys import exit


# CONSTANTS:
NO_SOL = 'NO SOLUTION'


# CONVERTERS FUNCTIONS:
def subset_to_seq(subset_sol):
    """Convert subset solution (e.g.: [[0,1],[0,0]]) into sequence solution (e.g.: ['r2'])"""
    if subset_sol == NO_SOL:
        return NO_SOL
    m = len(subset_sol[0])
    n = len(subset_sol[1])
    seq_sol = list()
    for i in range(m):
        if subset_sol[0][i]:
            seq_sol.append(f"r{i+1}")
    for j in range(n):
        if subset_sol[1][j]:
            seq_sol.append(f"c{j+1}")
    return seq_sol


def seq_to_subset(seq_sol, m, n):
    """Convert sequence solution (e.g.: ['r2']) into subset solution (e.g.: [[0,1],[0,0]])"""
    if seq_sol == NO_SOL:
        return NO_SOL
    subset_sol = [[0]*m,[0]*n]
    for e in seq_sol:
        if e[0] == 'r':
            subset_sol[0][int(e[1:])-1] = 1
        elif e[0] == 'c':
            subset_sol[1][int(e[1:])-1] = 1
        else:
            raise RuntimeError(f'This seq_sol is bad written: {seq_sol}')
    return subset_sol


# TO_STRING and FROM_STRING FUNCTIONS:
def seq_to_str(seq_sol):
    """From a sequence solution (e.g.: ['r2']) returns its string form (e.g.: 'r2')"""
    if seq_sol == NO_SOL:
        return NO_SOL
    return ' '.join(seq_sol)


def subset_to_str(subset_sol):
    """From a subset solution (e.g.: [[0,1],[0,0]]) returns a list with the rows string and the columns string (e.g.: ['0 1', '0 0']) or NO_SOL"""
    if subset_sol == NO_SOL:
        return NO_SOL
    return [' '.join([str(e) for e in subset_sol[0]]), \
            ' '.join([str(e) for e in subset_sol[1]])]


def get_pirellone_from_str(str):
    """From a string, this function returns a pirellone instance in list form."""
    pirellone = list()
    rows = str.split('\n')
    for cols in rows:
        pirellone.append([int(e) for e in cols.split()])
    return pirellone


def pirellone_to_str(pirellone):
    """From a pirellone instance, this function returns its string rappresentation."""
    return '\n'.join((' '.join(str(col) for col in row) for row in pirellone))


# PIRELLLONE GENERATORS FUNCTIONS:
def is_solvable_seed(seed):
    """If this seed is associated to a solvable pirellone instance return True, False otherwise."""
    # We reserve those seed divisible by 3 to the NOT solvable instances
    return (seed % 3) != 0


def gen_pirellone_seed(solvable=None):
    """This function returns a seed to generate a pirellone instance with the specificated solvability."""
    random.seed()
    seed = random.randint(100002,999999)
    # Check solvability
    if solvable == None:
        solvable = random.choice([False, True])
    # adust seed if not suitable
    if solvable != is_solvable_seed(seed):
        # We reserve those seed divisible by 3 to the NOT solvable instances
        if solvable:
            seed -= random.randrange(1, 3)   
        else:
            seed -= (seed % 3)  
    return seed


def gen_pirellone(m, n, seed, with_yes_certificate=False):
    """From (m,n,seed), this functions returns a pirellone instance, with eventually the certificate."""
    assert m >= 0
    assert n >= 0
    solvable = is_solvable_seed(seed)
    # Generate pirellone
    random.seed(seed)
    switches_row = [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    pirellone = [ [ (switches_col[j] + switches_row[i]) % 2 for j in range(n) ] for i in range(m)]
    if not solvable:
        if m < 2 or n < 2:
            # In this case, the pirellone is always solvable
            raise RuntimeError('invalid-unsolvable-dimensions')
        num_altered_rows = random.randrange(1, m)
        altered_rows= random.sample(range(m), num_altered_rows)
        for row in altered_rows:
            col = random.randrange(0, n)
            pirellone[row][col] = 1 - pirellone[row][col] 
    if with_yes_certificate:
        return pirellone, switches_row, switches_col
    else:
        return pirellone


# GET_SOL FUNCTIONS:
# TODO: manage NO_SOL case
def get_opt_sol_from(switches_row, switches_col):
    """Returns the optimal solution of solvable pirellone in the specificated style.
    Note: for unsolvable instances is not guaranteed optimality."""
    m = len(switches_row)
    n = len(switches_col)
    num_one = sum(switches_col) + sum(switches_row)
    if num_one > (m + n - num_one):
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    return [switches_row, switches_col]


# TODO: manage NO_SOL case
def get_opt_sol(pirellone):
    """Returns the optimal solution of solvable pirellone.
    Note: for unsolvable instances is not guaranteed optimality."""
    switches_col = pirellone[0].copy()
    m = len(pirellone)
    n = len(switches_col)
    if switches_col[0]:
        switches_row = [1-pirellone[_][0] for _ in range(m)]
    else:
        switches_row = [pirellone[_][0] for _ in range(m)]
    if sum(switches_row) + sum(switches_col) > ((m + n) // 2):
        switches_row = [1-switches_row[_] for _ in range(m)]
        switches_col = [1-switches_col[_] for _ in range(n)]
    return [switches_row, switches_col]


# UTILITIES FUNCTIONS:
def switch_row(i, pirellone):
    """It switch the lights of i-row of the given pirellone instance."""
    for j in range(len(pirellone[0])):
        pirellone[i][j] = int(not pirellone[i][j])


def switch_col(j, pirellone):
    """It switch the lights of i-col of the given pirellone instance."""
    for i in range(len(pirellone)):
        pirellone[i][j] = int(not pirellone[i][j])


def are_equiv(sol1, sol2):
    """Return True if two solutions are strictly equivalent."""
    if sol1 == sol2:
        return True
    if sol1 == NO_SOL or sol2 == NO_SOL:
        return False
    # Check complement
    return [[1-e for e in sol1[0]], [1-e for e in sol1[1]]] == sol2


def is_solvable(pirellone):
    """From a pirellone instance, this functions returns True if it is solvable, False otherwise."""
    for i in range(len(pirellone)):
        inv = (pirellone[0][0] != pirellone[i][0])
        for j in range(len(pirellone[0])):
            if inv:
                v = not pirellone[i][j]
            else:
                v = pirellone[i][j]
            if v != pirellone[0][j]:
                return False
    return True


def get_padded_sol_seq(m, n, sol, pad_size):
    """From a solution and (m,n), this functions returns a solution longer than at least pad_size."""
    if sol == NO_SOL:
        return NO_SOL
    padded_sol = sol.copy()
    diff = pad_size
    turn = 0
    while diff > 0:
        if turn == 0:
            # add fake random row move
            num = f"r{random.randint(1, m)}"
        else:
            # add fake random col move
            num = f"c{random.randint(1, n)}"
        padded_sol.append(num)
        padded_sol.append(num)
        turn = (turn + 1) % 2
        diff -= 2
    random.shuffle(padded_sol)
    return padded_sol


#TODO: to be tested
def get_padded_sol_subset(m, n, sol, pad_size):
    """From a solution and (m,n), this functions returns a solution longer than at least pad_size."""
    if sol == NO_SOL:
        return NO_SOL
    padded_sol = sol.copy()
    small_dim = m if m < n else n
    diff = pad_size
    while diff > 0:
        index = random.randrange[0, small_dim]
        padded_sol[0][index] = (1 - padded_sol[0][index]) #switch row
        padded_sol[1][index] = (1 - padded_sol[0][index]) #switch col
        diff -= 2
    return padded_sol


# CHECK_LIGHTS FUNCTIONS:
def get_light_on_after(pirellone, sol):
    """This function applies on pirellone instance the specified solution and then it counts lighs-on"""
    if sol == NO_SOL:
        return None
    m = len(pirellone)
    n = len(pirellone[0])
    assert len(sol[0]) == m
    assert len(sol[1]) == n
    # Perform solution
    pirellone_after = copy.deepcopy(pirellone)
    for i in range(m):
        if sol[0][i] == 1:
            switch_row(i, pirellone_after)
    for j in range(n):
        if sol[1][j] == 1:
            switch_col(j, pirellone_after)
    # Check the results obtained
    lights = 0
    for cols in range(len(pirellone_after)):
        lights += sum(pirellone_after[cols])
    return lights


#NOTE: da problemi quando il pirellone ha una diagonale di 1
def get_min_lights_on(pirellone):
    """Return the minimum number of lights that must be turn off manually"""
    test = copy.deepcopy(pirellone)
    s = 0
    h = 1
    k = 1
    while h != 0 or k != 0:
        h = 0
        k = 0
        for i in range(len(test)):
            if sum(test[i]) > (len(test) - sum(test[i])):
                switch_row(i, test)
                h += 1      
        for j in range(len(test[0])):
            for i in range(len(test)):
                s += test[i][j]
            if s > (len(test[0]) - s):
                switch_col(j, test)
                k += 1
            s = 0   
    light = 0
    for i in range(len(test)):
        light += sum(test[i]) 
    return light


##################################################
#NOTE: ancora da controllare
def extract_sol(line, m, n, LANG, TAc):
    matched = re.match("^((\n*(r|c)[1-9][0-9]{0,3})*\n*)$", line)
    if not bool(matched):
        TAc.print(LANG.render_feedback("wrong-sol-line",f'# Error! The line with your solution ({line}) is not accordant (it does not match the regular expression "^((\n*(r|c)[1-9][0-9]{0,3})*\n*)$"'), "red", ["bold"])
        exit(0)
    switch_rows = [0]*m
    switch_cols = [0]*n
    moves = line.split()
    for move,i in zip(moves,len(moves)):
        index = int(move[1:])
        if move[0] == "r":
            if index > m:
                TAc.print(LANG.render_feedback("row-index-exceeds-m",f'# Error! In your solution line ({line}) the {i}-th move ({move}) is not applicable. Indeed, {index}>{m}=m.'), "red", ["bold"])
                exit(0)
            switch_rows[index] = 1-switch_rows[index]
        if move[0] == "c":
            if index > n:
                TAc.print(LANG.render_feedback("column-index-exceeds-n",f'# Error! In your solution line ({line}) the {i}-th move ({move}) is not applicable. Indeed, {index}>{n}=n.'), "red", ["bold"])
                exit(0)
            switch_cols[index] = 1-switch_cols[index]
    return switch_rows, switch_cols
  

#NOTE: forse non corretta la seguente funzione      
def solution_irredundant(pirellone,switches_row,switches_col,smallest=True):
    assert is_solvable(pirellone)
    m = len(switches_row)
    n = len(switches_col)
    switches_row = pirellone[0]
    if pirellone[0][0] == 0:
        switches_col = pirellone[0]
    else:    
        switches_row = [ 1-pirellone[i][0] for i in range(m) ]
    if smallest != (sum(switches_col)+sum(switches_row) <= (m+n)//2):
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    
    [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    pirellone = [ [ (switches_col[j] + switches_row[i]) % 2 for j in range(n) ] for i in range(m)]

    lista=[]
    for i in range(m):
        if switches_row[i]:
            lista.append(f"r{i+1}")
    for j in range(n):
        if switches_col[j]:
            lista.append(f"c{j+1}")
    return lista




# TESTS
if __name__ == "__main__":

    print('Test: subset_to_seq()')
    assert subset_to_seq([[0, 0, 1], [0, 1, 0]]) == ['r3', 'c2']
    assert subset_to_seq(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: seq_to_subset()')
    assert seq_to_subset(['r3', 'c2'], 4, 4) == [[0, 0, 1, 0], [0, 1, 0, 0]]
    assert seq_to_subset(NO_SOL, 4, 4) == NO_SOL
    print('==> OK\n')


    print('Test: seq_to_str()')
    assert seq_to_str(['r3', 'c2']) == 'r3 c2'
    assert seq_to_str(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: subset_to_str()')
    assert subset_to_str([[0, 0, 1], [0, 1, 0]]) == ['0 0 1', '0 1 0']
    assert subset_to_str(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: pirellone_to_str()')
    assert pirellone_to_str([[0, 0], [1, 1]]) == '0 0\n1 1'
    print('==> OK\n')


    print('Test: get_pirellone_from_str()')
    assert get_pirellone_from_str('0 0\n1 1') == [[0, 0], [1, 1]]
    print('==> OK\n')


    print('Test: is_solvable_seed()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: gen_pirellone_seed()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: gen_pirellone()')
    print('MAYBE TODO?')
    print('==> OK\n')


    print('Test: get_opt_sol_from()')
    print('MAYBE TODO?')
    print('==> OK\n')


    print('Test: get_opt_sol() in solvable instances')
    assert get_opt_sol([[0, 0], [0, 0]]) == [[0, 0],[0, 0]]
    assert get_opt_sol([[0, 0], [1, 1]]) == [[0, 1],[0, 0]]
    assert get_opt_sol([[0, 1], [0, 1]]) == [[0, 0],[0, 1]]
    assert get_opt_sol([[0, 1], [1, 0]]) in [[[1, 0],[1, 0]],
                                             [[0, 1],[0, 1]]]
    assert get_opt_sol([[1, 0], [0, 1]]) in [[[1, 0],[0, 1]],
                                             [[0, 1],[1, 0]]]
    assert get_opt_sol([[1, 0], [1, 0]]) == [[0, 0],[1, 0]]
    assert get_opt_sol([[1, 1], [0, 0]]) == [[1, 0],[0, 0]]
    assert get_opt_sol([[1, 1], [1, 1]]) in [[[1, 1],[0, 0]],
                                             [[0, 0],[1, 1]]]
    print('Test: get_opt_sol() in NOT solvable instances')
    print('THIS BEHAVIOR HAS YET TO BE IMPLEMENTATED')
    # assert get_opt_sol([[0, 0], [0, 1]]) == NO_SOL
    # assert get_opt_sol([[0, 0], [1, 0]]) == NO_SOL
    # assert get_opt_sol([[0, 1], [0, 0]]) == NO_SOL
    # assert get_opt_sol([[0, 1], [1, 1]]) == NO_SOL
    # assert get_opt_sol([[1, 0], [0, 0]]) == NO_SOL
    # assert get_opt_sol([[1, 0], [1, 1]]) == NO_SOL
    # assert get_opt_sol([[1, 1], [0, 1]]) == NO_SOL
    # assert get_opt_sol([[1, 1], [1, 0]]) == NO_SOL
    print('==> OK\n')


    print('Test: switch_row()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: switch_col()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: are_equiv()')
    assert are_equiv([[0, 0], [0, 1]], [[0, 0], [0, 1]])
    assert are_equiv(NO_SOL, NO_SOL)
    assert are_equiv([[0, 0], [0, 1]], [[1, 1], [1, 0]])
    assert are_equiv([[1, 0], [0, 1]], [[0, 1], [1, 0]])
    assert not are_equiv([[0, 0], [0, 1]], NO_SOL)
    assert not are_equiv(NO_SOL, [[0, 0], [0, 1]])
    assert not are_equiv([[0, 0], [0, 1]], [[0, 0], [1, 0]])
    print('==> OK\n')


    print('Test: is_solvable() in solvable instances')
    assert is_solvable([[0, 0], [0, 0]])
    assert is_solvable([[0, 0], [1, 1]])
    assert is_solvable([[0, 1], [0, 1]])
    assert is_solvable([[0, 1], [1, 0]])
    assert is_solvable([[1, 0], [0, 1]])
    assert is_solvable([[1, 0], [1, 0]])
    assert is_solvable([[1, 1], [0, 0]])
    assert is_solvable([[1, 1], [1, 1]])
    print('==> OK\n')
    print('Test: is_solvable() in NOT solvable instances')
    assert not is_solvable([[0, 0], [0, 1]])
    assert not is_solvable([[0, 0], [1, 0]])
    assert not is_solvable([[0, 1], [0, 0]])
    assert not is_solvable([[0, 1], [1, 1]])
    assert not is_solvable([[1, 0], [0, 0]])
    assert not is_solvable([[1, 0], [1, 1]])
    assert not is_solvable([[1, 1], [0, 1]])
    assert not is_solvable([[1, 1], [1, 0]])
    print('==> OK\n')


    print('Test: get_padded_sol_seq()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: get_padded_sol_subset()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: get_light_on_after() in solvable instances')
    assert get_light_on_after([[0, 0], [0, 0]], get_opt_sol([[0, 0], [0, 0]])) == 0
    assert get_light_on_after([[0, 0], [1, 1]], get_opt_sol([[0, 0], [1, 1]])) == 0
    assert get_light_on_after([[0, 1], [0, 1]], get_opt_sol([[0, 1], [0, 1]])) == 0
    assert get_light_on_after([[0, 1], [1, 0]], get_opt_sol([[0, 1], [1, 0]])) == 0
    assert get_light_on_after([[1, 0], [0, 1]], get_opt_sol([[1, 0], [0, 1]])) == 0
    assert get_light_on_after([[1, 0], [1, 0]], get_opt_sol([[1, 0], [1, 0]])) == 0
    assert get_light_on_after([[1, 1], [0, 0]], get_opt_sol([[1, 1], [0, 0]])) == 0
    assert get_light_on_after([[1, 1], [1, 1]], get_opt_sol([[1, 1], [1, 1]])) == 0
    assert get_light_on_after([[1, 1], [1, 1]], [[0, 0], [0, 0]]) == 4
    assert get_light_on_after([[1, 1], [1, 1]], [[1, 0], [0, 0]]) == 2
    assert get_light_on_after([[1, 1], [1, 1]], [[1, 1], [0, 0]]) == 0
    print('==> OK\n')
    print('Test: check_off_lights() in NOT solvable instances')
    assert not get_light_on_after([[0, 0], [0, 1]], get_opt_sol([[0, 0], [0, 1]])) == None
    assert not get_light_on_after([[0, 0], [1, 0]], get_opt_sol([[0, 0], [1, 0]])) == None
    assert not get_light_on_after([[0, 1], [0, 0]], get_opt_sol([[0, 1], [0, 0]])) == None
    assert not get_light_on_after([[0, 1], [1, 1]], get_opt_sol([[0, 1], [1, 1]])) == None
    assert not get_light_on_after([[1, 0], [0, 0]], get_opt_sol([[1, 0], [0, 0]])) == None
    assert not get_light_on_after([[1, 0], [1, 1]], get_opt_sol([[1, 0], [1, 1]])) == None
    assert not get_light_on_after([[1, 1], [0, 1]], get_opt_sol([[1, 1], [0, 1]])) == None
    assert not get_light_on_after([[1, 1], [1, 0]], get_opt_sol([[1, 1], [1, 0]])) == None


    print('Test: get_min_lights_on() in solvable instances')
    # assert get_min_lights_on([[0, 0], [0, 0]]) == 0
    # assert get_min_lights_on([[0, 0], [1, 1]]) == 0
    # assert get_min_lights_on([[0, 1], [0, 1]]) == 0
    # assert get_min_lights_on([[0, 1], [1, 0]]) == 0
    # assert get_min_lights_on([[1, 0], [0, 1]]) == 0
    # assert get_min_lights_on([[1, 0], [1, 0]]) == 0
    # assert get_min_lights_on([[1, 1], [0, 0]]) == 0
    # assert get_min_lights_on([[1, 1], [1, 1]]) == 0
    print('THIS BEHAVIOR HAS YET TO BE IMPLEMENTATED')
    print('==> OK\n')
    print('Test: get_min_lights_on() in NOT solvable instances')
    print('THIS BEHAVIOR HAS YET TO BE IMPLEMENTATED')
    print('==> OK\n')

