#!/usr/bin/env python3
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import chococroc_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="chococroc"
service="play"

args_list = [
    ('m',int),
    ('n',int),
    ('TALight_first_to_move',int),
    ('watch',str),
    ('random',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

def close_service_and_print_term_signal_for_bots():
    TAc.Finished(only_term_signal=True)
    exit(0)

if ENV['random']== 1:
    m=random.randint(1, 1000)
    n=random.randint(1, 1000)
else:
    m=ENV['m']
    n=ENV['n']
        
def I_have_lost():
    TAc.print(LANG.render_feedback("TALight_lost", f'# It is my turn to move, on conf (1,1). Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("you-won", f'# You won!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost():
    TAc.print(LANG.render_feedback("you-have-lost", f'# It is your turn to move, on conf (1,1). Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("you-lost", f'# You lost!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
def watch(m,n, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS] 
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS]
    if ENV["watch"] == 'no_watch':
        return
    TAc.print(f'# watch={ENV["watch"]}: ', "blue", end='')
    if ENV['watch'] == 'watch_winner':
        if(cl.grundy_val(m,n) == 0):
            TAc.print(LANG.render_feedback("watch-winner-who-moves-loses", f'{second_to_move} ahead, since ({m}, {n}) is a who-moves-loses configuration.'), "blue")
        else:
            TAc.print(LANG.render_feedback("watch-winner-who-moves-wins", f'{first_to_move} ahead, since ({m}, {n}) is a who-moves-wins configuration.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        win_moves = cl.winning_moves(m,n)
        win_moves.discard((None, None))
        if len(win_moves) > 0:
            TAc.print(LANG.render_feedback("num-winning-moves-n", f'# the current configuration ({m}, {n}) admits {len(win_moves)} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("num-winning-moves-0", f'# the current configuration ({m}, {n}) admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        win_moves = cl.winning_moves(m, n)
        win_moves.discard((None, None))
        if len(win_moves) > 1:
            TAc.print(LANG.render_feedback("list-multiple-winning-moves", f'# for the current configuration ({m}, {n}) the winning moves are {win_moves}'), "blue")
        elif len(win_moves) == 1:
            TAc.print(LANG.render_feedback("list-one-winning-move", f'# for the current configuration ({m}, {n}) the winning move is {win_moves}'), "blue")
        else:
            TAc.print(LANG.render_feedback("list-none-winning-moves", f'# the current configuration ({m}, {n}) admits no winning move'), "blue")
    elif ENV['watch'] == 'watch_grundy_val':
        TAc.print(LANG.render_feedback("watch-grundy-val", f'# the current configuration ({m}, {n}) has grundy value {cl.grundy_val(m,n)}'), "blue")



if ENV["TALight_first_to_move"] == 1: # if the user plays the match as second to move
    watch(m,n, first_to_move=I_AM, second_to_move=YOU_ARE)
    if m==1 and n==1: # no valid moves on the configuration (1,1). TALight first to move loses the match
        I_have_lost()
        
    # TALight makes its move updating the configuration (m,n):
    new_m,new_n=cl.computer_move(m,n)
    TAc.print(LANG.render_feedback("server-move", f'# My move is from conf ({m},{n}) to conf ({new_m},{new_n}).'), "green", ["bold"])
    m,n=new_m,new_n

while True:
    if m==1 and n==1: # the configuraion (1,1) admits no valid move. The turn is to the user who has no move available and loses the match. TALight wins.
        you_have_lost()
    
    watch(m,n, first_to_move=YOU_ARE, second_to_move=I_AM)    
    TAc.print(LANG.render_feedback("your-turn", f'# It is your turn to move from conf ({m},{n}) to a new conf (m,n).'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("user-move", f'# Please, insert the two integers m and n encoding the new configuration produced by your move just underneath the current position we put you into: '), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("prompt", f'{m} {n}'), "yellow", ["bold"])
    new_m,new_n = TALinput(int, 2, TAc=TAc)
    if new_m != m and new_n != n: # invalid move: at most one of the two coordinates can be changed
        TAc.print(LANG.render_feedback("not-valid", f'# No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("double-move", f'# You are cheating. A move can not alter both the number of rows (from {m} to {new_m}) and the number of columns (from {n} to {new_n})).'), "red", ["bold"])
        exit(0)
    if new_m == m and new_n == n: # invalid move (the game does not allow to pass)
        TAc.print(LANG.render_feedback("not-valid", f'# No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("dull-move", f'# You are cheating. Your move must either reduce the number of rows or the number of columns. Otherwise, you have not really moved but simply passed.'), "red", ["bold"])
        exit(0)
    if new_m != m:
        pos = m
        new_pos = new_m
    else:
        pos = n
        new_pos = new_n
    if new_pos > pos: # invalid move
        TAc.print(LANG.render_feedback("not-valid", f'# No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("increasing-move", f'# With a move the value of a coordinate can not increase from {pos} to {new_pos}. On the contrary, precisely one coordinate must be decreased.'), "red", ["bold"])
        exit(0)
    if new_pos < pos - (pos//2): # invalid move
        TAc.print(LANG.render_feedback("not-valid", f'# No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("excessive-move", f'# No! No valid move can more than half the value of a coordinate. (Here, the double of {new_pos} is {2*new_pos}, but {2*new_pos} < {pos}).'), "red", ["bold"])
        exit(0)

    if new_m==1 and new_n==1: # TALight has no valid move available and loses the match. The user wins.
        I_have_lost()
    
    watch(new_m,new_n, first_to_move=I_AM, second_to_move=YOU_ARE)    
    m,n=cl.computer_move(new_m,new_n) # TALight makes its move
    TAc.print(LANG.render_feedback("server-move", f'# My move is from conf ({new_m},{new_n}) to conf ({m},{n}).'), "green", ["bold"])
