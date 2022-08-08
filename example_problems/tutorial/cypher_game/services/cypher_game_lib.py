#!/usr/bin/env python3
import random
from itertools import count, filterfalse

def player_flip(n_player):
    if n_player==1:
        n_player=2
    else:
        n_player=1
    return n_player

def find_all_moves(n, rmv_dup=False):
    t=n
    moves=[]
    while t>0:
        sub=t%10
        if sub!=0:
            moves.append(n-sub)
        t=t//10
    if rmv_dup:
        moves=list(dict.fromkeys(moves))
    return moves

def find_move(n):
    return random.choice(find_all_moves(n, True))

def find_winning_move(n):
    if grundy_val(n)==0:
        return []
    return [n-n%10]

def computer_move(n):
    if grundy_val(n)==0:
        return find_move(n)
    return find_winning_move(n)[0]

def find_winning_moves_nim(n, nim=0, rmv_dup=False):
    t=n
    moves=[]
    while t>0:
        sub=t%10
        if sub!=0 and grundy_sum(grundy_val(n-sub),nim)==0:
            moves.append(n-sub)
        t=t//10
    if rmv_dup:
        moves=list(dict.fromkeys(moves))
    return moves

def find_winning_move_nim(n, nim=0):
    t=n
    while t>0:
        sub=t%10
        if sub!=0 and grundy_sum(grundy_val(n-sub),nim)==0:
            return n-sub
        t=t//10
    return None

def find_winning_moves_cypher_game_nim(n,nim=0,rmv_dup=False):
    win_moves = find_winning_moves_nim(n,nim,rmv_dup)
    win_moves_with_nim={(None,None)}
    for move in win_moves:
        move_t=move,+nim
        win_moves_with_nim.add(move_t)
    win_moves_with_nim.discard((None,None))
    win_moves_with_nim.update(winning_moves_nim(n, nim))
    return win_moves_with_nim

def winning_moves_nim(n, nim):
    cypher_game_grundy_value = grundy_val(n)
    win_moves={(None,None)}
    for i in range(1, nim+1):
        if grundy_sum(cypher_game_grundy_value, nim-i)==0:
            win_moves.add((n,nim-i))
    win_moves.discard((None,None))
    return win_moves

def computer_move_nim(n, nim):
    n_grundy_val=grundy_val(n)
    if grundy_sum(n_grundy_val, nim) == 0:
        games = []
        if n != 0:
            games.append('cypher_game')
        if nim > 0:
            games.append('nim')
        selected_game = random.choice(games)
        if selected_game == 'cypher_game':
            new_n=random.choice(find_all_moves(n, True))
            return new_n,nim
        else:
            return n,nim-random.randint(1,nim)
    if n!=0:
        new_n=find_winning_move_nim(n,nim)
    else:
        new_n=None
    if new_n!=None:
        return new_n,nim
    move_on_nim=0
    while grundy_sum(n_grundy_val, nim-move_on_nim) !=0:
        move_on_nim+=1
    return n,nim-move_on_nim

def grundy_val(n):
    if n%10==0:
        return 0
    t=n
    cyphers=[]
    while t>0:
        sub=t%10
        if sub!=0:
            cyphers.append(sub)
        t=t//10
    if len(set(cyphers))==1 or (n>0 and n<10) or (len(set(cyphers))==2 and 0 in set(cyphers)):
        return 1
    val1=[0,1,1,1,1,1,1,1,1,1]
    val2=[]
    for num in range(10,n+1,10):
        for i in range(10):
            actual_num=num+i
            moves=find_all_moves(actual_num,True)
            values=[]
            for move in moves:
                cypher2=actual_num%10
                if move<actual_num-cypher2:
                    values.append(val1[move%10])
                else:
                    values.append(val2[move%10])
            val2.append(min_value(values))
            if actual_num==n:
                return val2[n%10]
        val1=val2
        val2=[]

def min_value(list):
    if 0 not in list:
        return 0
    return next(filterfalse(set(list).__contains__, count(1)))

def grundy_sum(val1:int, val2:int):
    return val1 ^ val2

def verify_move(n, new_n):
    moves=find_all_moves(n,True)
    for move in moves:
        if new_n==move:
            return True
    return False

# TESTS
if __name__ == "__main__":
    # GRUNDY-SPRAGUE THEORY FUNCTIONS:
    print('Test: grundy_val(n)')
    ns = [10,0,5,3,55,105,12980,114,121,129,12]
    ref_values = [0,0,1,1,1,1,0,2,2,3,2]
    for index,n in enumerate(ns):
        assert grundy_val(n) == ref_values[index]
    print('==> OK')
