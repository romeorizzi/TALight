#!/usr/bin/env python3
import string
import random

def grundy_sum(val1:int, val2:int):
    return val1 ^ val2

def grundy_val(m:int, n:int = 1):
    assert m > 0 and n > 0
    if m > 1 and n > 1:
        return grundy_sum(grundy_val(m), grundy_val(n))
    if m == 1:
        m,n = n,m
    if m == 1:
        return 0
    if m % 2 == 0:
        return m//2
    return grundy_val(m//2)

def find_move(m, n):
    for s in range(1, m // 2 + 1):
        if not grundy_val(m - s, n):
            return (0, s)
    for s in range(1, n // 2 + 1):
        if not grundy_val(m, n - s):
            return (1, s)
    
def winning_move(m,n):
    (direction, sz) = find_move(m, n)
    if direction:
        return (m,n-sz)
    else:
        return (m-sz,n)

def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup

def winning_moves(m,n):
    (direction, sz) = find_move(m, n)
    move1=(None,None)
    move2=(None,None)
    if direction: # the move reduces by sz the number n of columns
        move1=(m,n-sz)
    else: # the move reduces by sz the number m of rows
        move1=(m-sz,n)
    (direction, sz) = find_move(n, m)
    if direction: # the move reduces by sz the number m of columns
        move2=(n,m-sz)
    else: # the move reduces by sz the number n of rows
        move2=(n-sz,m)
    if move1==reverse(move2):
        return move1
    else:
        return {move1, (move2[1],move2[0])}

def computer_move(m,n):
    assert m > 1 or n > 1
    grundy_value = grundy_val(m,n)
    if grundy_value > 0:
        return winning_move(m,n)
    coordinates = []
    if m > 1:
        coordinates.append('rows')
    if n > 1:
        coordinates.append('columns')
    move_coord = random.choice(coordinates)
    if move_coord == 'rows':
        return (m-random.randint(1,m//2), n)
    else:
        return (m, n-random.randint(1,n//2))

def not_a_number(move):
    try:
        int(move)
        return False
    except ValueError:
        return True

def move_control(move, m):
    if not_a_number(move):
        return True
    move=int(move)
    if m%2==0:
        if move>=m or move<m//2:
            return True
        else:
            return False
    else:
        if move>=m or move<(m//2)+1:
            return True
        else:
            return False

def player_move(m,n,TAc,LANG):
    direction=input('Insert your move (rows/columns):\n')
    while direction != 'rows' and direction != 'columns':
        direction=input('Wrong direction. Try again:\n')

    while True:        
        if direction=='rows':
            if m==1:
                TAc.print(LANG.render_feedback("invalid-move", f'You can\'t move in this direction because there is only 1 row.'), "red", ["bold"])
                while direction != 'columns':
                    direction=input('Change direction. Try again:\n')
            else:
                move=input('Insert number of rows remaining:\n')
                while move_control(move,m):
                    move=input('Your move is not correct, try again:\n')
                move=int(move)
                TAc.print(LANG.render_feedback("user-move", f'Your move: {move} x {n}.'), "yellow", ["bold"])
                return (move, n)

        elif direction=='columns':
            if n==1:
                TAc.print(LANG.render_feedback("invalid-move", f'You can\'t move in this direction because there is only 1 column.'), "red", ["bold"])
                while direction != 'rows':
                    direction=input('Change direction. Try again:\n')
            else:
                move=input('Insert number of columns remaining:\n')
                while move_control(move,n):
                    move=input('Your move is not correct, try again:\n')
                move=int(move)
                TAc.print(LANG.render_feedback("user-move", f'Your move: {m} x {move}.'), "yellow", ["bold"])
                return (m, move)

# TESTS
if __name__ == "__main__":
    # GRUNDY-SPRAGUE THEORY FUNCTIONS:
    print('Test: grundy_val(n, 1)')
    ref_values = [0, 1, 0, 2, 1, 3, 0, 4, 2, 5, 1, 6, 3, 7, 0, 8, 4]
    for n in range(1,1+len(ref_values)):
        assert grundy_val(n) == ref_values[n-1]
    print('==> OK\n')

    print('Test: grundy_val(m, n)')
    print('TO BE DONE')



