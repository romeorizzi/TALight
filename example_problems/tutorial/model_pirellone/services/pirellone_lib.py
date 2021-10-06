#!/usr/bin/env python3

import random, copy
import re
from sys import exit



def get_pirellone_from_str(str):
    l = list()
    rows = str.split('\n')
    for cols in rows:
        l.append(cols.split())
    return l


def get_str_from_pirellone(pirellone):
    return '\n'.join((' '.join(str(col) for col in row) for row in pirellone))


def get_str_from_sol(sol, mode='seq'):
    assert mode == 'seq' or mode == 'subset'
    if mode == 'seq':
        return ' '.join(sol)
    elif mode == 'subset':
        return ' '.join(sol)
        


def is_solvable_seed(seed):
    return (seed % 3) != 0


def gen_pirellone_seed(solvable=None):
    random.seed()
    seed = random.randint(100002,999999)
    # Check solvability
    if solvable == None:
        solvable = random.choice([False, True])
    # adust seed if not suitable
    if solvable != is_solvable_seed(seed):
        if solvable:
            seed -= random.randrange(1, 3)   
        else:
            seed -= (seed % 3)  
    return seed


def gen_pirellone(m, n, seed, with_yes_certificate=False):
    """we reserve those seed divisible by 3 to the NOT solvable instances"""
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


def is_solvable(pirellone):
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


def get_padded_sol(m, n, sol, pad_size):
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


def switch_row(i, pirellone):
    for j in range(len(pirellone[0])):
        pirellone[i][j] = int(not pirellone[i][j])


def switch_col(j, pirellone):
    for i in range(len(pirellone)):
        pirellone[i][j] = int(not pirellone[i][j])


def get_sol_from(switches_row, switches_col):
    """Return the optimal solution of solvable pirellone"""
    m = len(switches_row)
    n = len(switches_col)
    num_one = sum(switches_col) + sum(switches_row)
    if num_one > (m + n - num_one):
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    sol = list()
    for i in range(m):
        if switches_row[i]:
            sol.append(f"r{i+1}")
    for j in range(n):
        if switches_col[j]:
            sol.append(f"c{j+1}")
    return sol


def get_sol(pirellone):
    """Return the optimal solution of solvable pirellone"""
    switches_col = pirellone[0].copy()
    m = len(pirellone)
    n = len(switches_col)
    if switches_col[0]:
        switches_row = [ 1-pirellone[_][0] for _ in range(m)]
    else:
        switches_row = [ pirellone[_][0] for _ in range(m)]
    if sum(switches_row) + sum(switches_col) > ((m + n) // 2):
        switches_row = [ 1-switches_row[_] for _ in range(m)]
        switches_col = [ 1-switches_col[_] for _ in range(n)]
    sol = list()
    for i in range(m):
        if switches_row[i]:
            sol.append(f"r{i+1}")
    for j in range(n):
        if switches_col[j]:
            sol.append(f"c{j+1}")
    return sol
  

def get_light_on_after(pirellone, sol):
    m = len(pirellone)
    n = len(pirellone[0])
    # Use solution for testing
    pirellone_after = copy.deepcopy(pirellone)
    for i in range(0, len(sol)):
        if not sol[i][1:].isdigit():
            raise RuntimeError('invalid-cmd', sol[i])
        if sol[i][0]=='r':
            if int(sol[i][1:]) > m:
                raise RuntimeError('row-index-exceeds-m', sol[i], sol[i][1:], m)
            switch_row(int(sol[i][1:])-1, pirellone_after)
        elif sol[i][0]=='c':
            if int(sol[i][1:]) > n:
                raise RuntimeError('row-index-exceeds-m', sol[i], sol[i][1:], n)
            switch_col(int(sol[i][1:])-1, pirellone_after)
        else:
            raise RuntimeError('invalid-cmd', sol[i])
    # Check the results obtained
    lights = 0
    for i in range(len(pirellone_after)):
        lights += sum(pirellone_after[i])
    return lights


def check_off_lights(pirellone, sol_to_test, opt_sol):
    # Get light on after sol_to_test
    lights = get_light_on_after(pirellone, sol_to_test)
    # Get the min lights on with this pirellone
    min_lights = get_light_on_after(pirellone, opt_sol)
    return lights == min_lights



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


#NOTE: not correct for identity matrix
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



# TESTS
if __name__ == "__main__":

    print('Test: is_solvable()')
    assert is_solvable([[0, 0], [0, 0]])
    assert not is_solvable([[0, 0], [0, 1]])
    assert not is_solvable([[0, 0], [1, 0]])
    assert is_solvable([[0, 0], [1, 1]])
    assert not is_solvable([[0, 1], [0, 0]])
    assert is_solvable([[0, 1], [0, 1]])
    assert is_solvable([[0, 1], [1, 0]])
    assert not is_solvable([[0, 1], [1, 1]])
    assert not is_solvable([[1, 0], [0, 0]])
    assert is_solvable([[1, 0], [0, 1]])
    assert is_solvable([[1, 0], [1, 0]])
    assert not is_solvable([[1, 0], [1, 1]])
    assert is_solvable([[1, 1], [0, 0]])
    assert not is_solvable([[1, 1], [0, 1]])
    assert not is_solvable([[1, 1], [1, 0]])
    assert is_solvable([[1, 1], [1, 1]])
    print('==> OK')


    # print('Test: get_min_lights_on()')
    # assert get_min_lights_on([[0, 0], [0, 0]]) == 0
    # assert get_min_lights_on([[0, 0], [0, 1]]) == 1
    # assert get_min_lights_on([[0, 0], [1, 0]]) == 1
    # assert get_min_lights_on([[0, 0], [1, 1]]) == 0
    # assert get_min_lights_on([[0, 1], [0, 0]]) == 1
    # assert get_min_lights_on([[0, 1], [0, 1]]) == 0
    # assert get_min_lights_on([[0, 1], [1, 0]]) == 0
    # assert get_min_lights_on([[0, 1], [1, 1]]) == 1
    # assert get_min_lights_on([[1, 0], [0, 0]]) == 1
    # assert get_min_lights_on([[1, 0], [0, 1]]) == 0
    # assert get_min_lights_on([[1, 0], [1, 0]]) == 0
    # assert get_min_lights_on([[1, 0], [1, 1]]) == 1
    # assert get_min_lights_on([[1, 1], [0, 0]]) == 0
    # assert get_min_lights_on([[1, 1], [0, 1]]) == 1
    # assert get_min_lights_on([[1, 1], [1, 0]]) == 1
    # assert get_min_lights_on([[1, 1], [1, 1]]) == 0
    # print('==> OK')


    print('Test: len(get_sol()) for solvable Instance')
    assert len(get_sol([[0, 0], [0, 0]])) == 0
    assert len(get_sol([[0, 0], [0, 1]])) == 0
    assert len(get_sol([[0, 0], [1, 1]])) == 1
    assert len(get_sol([[0, 1], [0, 1]])) == 1
    assert len(get_sol([[0, 1], [1, 0]])) == 2
    assert len(get_sol([[1, 0], [0, 1]])) == 2
    assert len(get_sol([[1, 0], [1, 0]])) == 1
    assert len(get_sol([[1, 0], [1, 1]])) == 1
    assert len(get_sol([[1, 1], [0, 0]])) == 1
    assert len(get_sol([[1, 1], [0, 1]])) == 1
    assert len(get_sol([[1, 1], [1, 1]])) == 2
    print('==> OK')

    # print('Test: len(get_sol()) for unsolvable Instance')
    # assert len(get_sol([[1, 1], [1, 0]])) == 1
    # assert len(get_sol([[0, 0], [1, 0]])) == 0
    # assert len(get_sol([[0, 1], [0, 0]])) == 0
    # assert len(get_sol([[0, 1], [1, 1]])) == 1
    # assert len(get_sol([[1, 0], [0, 0]])) == 0
    # print('==> OK')