#!/usr/bin/env python3
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

def find_move(m, n, nim=0):
    for s in range(1, m // 2 + 1):
        if not grundy_sum(grundy_val(m - s, n), nim):
            return (0, s)
    for s in range(1, n // 2 + 1):
        if not grundy_sum(grundy_val(m, n - s), nim):
            return (1, s)
    return (None,None)
    
def winning_move(m,n,nim=0):
    (direction, sz) = find_move(m, n, nim)
    if (direction, sz)==(None,None):
        return (None,None)
    if direction:
        return (m,n-sz)
    else:
        return (m-sz,n)

def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup

def winning_moves(m,n,nim=0):
    (direction, sz) = find_move(m, n, nim)
    if (direction, sz)==(None,None):
        return {(None,None)}
    move1=(None,None)
    move2=(None,None)
    if direction: # the move reduces by sz the number n of columns
        move1=(m,n-sz)
    else: # the move reduces by sz the number m of rows
        move1=(m-sz,n)
    (direction, sz) = find_move(n, m, nim)
    if direction: # the move reduces by sz the number m of columns
        move2=(n,m-sz)
    else: # the move reduces by sz the number n of rows
        move2=(n-sz,m)
    if move1==reverse(move2):
        return {move1}
    else:
        return {move1, (move2[1],move2[0])}

def computer_random_choice_chococroc(m,n):
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

def computer_move(m,n):
    assert m > 1 or n > 1
    grundy_value = grundy_val(m,n)
    if grundy_value > 0:
        return winning_move(m,n)
    return computer_random_choice_chococroc(m,n)

def computer_decision_move(m,n,nim):
    chococroc_grundy_value=grundy_val(m,n)
    game_grundy_value=grundy_sum(chococroc_grundy_value, nim)
    if game_grundy_value==0:
        games = []
        if m > 1 or n > 1:
            games.append('chococroc')
        if nim > 0:
            games.append('nim')
        selected_game = random.choice(games)
        if selected_game == 'chococroc':
            new_m,new_n = computer_random_choice_chococroc(m,n)
            return new_m,new_n,nim
        else:
            return m,n,nim-random.randint(1,nim)
    new_m,new_n = winning_move(m,n,nim)
    if (new_m,new_n)!=(None,None):
        return new_m,new_n,nim
    move_on_nim=0
    while grundy_sum(chococroc_grundy_value, nim-move_on_nim)!=0:
        move_on_nim+=1
    return m,n,nim-move_on_nim

def count_winning_moves_nim (m, n, nim):
    chococroc_grundy_value = grundy_val(m, n)
    count=0
    for i in range(1, nim+1):
        if grundy_sum(chococroc_grundy_value, nim-i)==0:
            count +=1
    return count

def winning_moves_nim(m, n, nim):
    chococroc_grundy_value = grundy_val(m, n)
    win_moves={(None,None,None)}
    for i in range(1, nim+1):
        if grundy_sum(chococroc_grundy_value, nim-i)==0:
            win_moves.add((m,n,nim-i))
    win_moves.discard((None,None,None))
    return win_moves

def player_flip(n_player):
    if n_player==1:
        n_player=2
    else:
        n_player=1
    return n_player


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
    print('Test: computer decision move')
    if (7,7,0)==computer_decision_move(7,7,9):
        print('==> OK\n')
