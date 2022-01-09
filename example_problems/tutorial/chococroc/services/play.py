#!/usr/bin/env python3
import sys

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import chococroc_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="chococroc"
service="play"

args_list = [
    ('m',int),
    ('n',int),
    ('player',int),
    ('watch_value',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

m=ENV['m']
n=ENV['n']

if(ENV['watch_value'] == 'watch_winner'):
    if(cl.grundy_val(m,n) > 0):
        TAc.print(LANG.render_feedback("watch-winner-user-after-server", f'You want to watch the winner: starting from this configuration ({m}, {n}) you will win the game'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("watch-winner-server-after-server", f'You want to watch the winner: starting from this configuration ({m}, {n}) i will win the game'), "green", ["bold"])
elif ENV['watch_value'] == 'num_winning_moves' :
    win_moves = cl.winning_moves(m,n)
    win_moves.discard((None, None))
    if len(win_moves) >= 1:
        TAc.print(LANG.render_feedback("num-winning-moves-n", f'You want to know the number of winning moves: for the current configuration ({m}, {n}) the number of winning moves is {len(win_moves)}'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("num-winning-moves-0", f'You want to know the number of winning moves: for the current configuration ({m}, {n}) there are not winning moves'), "green", ["bold"])
elif(ENV['watch_value'] == 'list_winning_moves'):
    win_moves = cl.winning_moves(m, n)
    win_moves.discard((None, None))
    if len(win_moves) > 1:
        TAc.print(LANG.render_feedback("list-multiple-winning-moves", f'You want to know the winning moves: for the current configuration ({m}, {n}) the winning moves are {win_moves}'), "green", ["bold"])
    elif len(win_moves) == 1:
        TAc.print(LANG.render_feedback("list-one-winning-moves", f'You want to know the winning moves: for the current configuration ({m}, {n}) the winning move is {win_moves}'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("list-none-winning-moves", f'You want to know the winning moves: for the current configuration ({m}, {n}) there are not winning moves'), "green", ["bold"])
elif(ENV['watch_value'] == 'watch_grundy_val'):
    TAc.print(LANG.render_feedback("watch-grundy-after-server", f'You want to watch the grundy value: for the current configuration ({m}, {n}) the grundy value is {cl.grundy_val(m,n)}'), "green", ["bold"])

if ENV['player'] == 1: #se l'utente vuole giocare per secondo
    if m==1 and n==1: #inserisce una configurazione 1x1 il computer non ha mosse quindi vince l'utente
        TAc.print(LANG.render_feedback("you-have-won", f'It is my turn to move, on conf (1,1). Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("you-won", f'You won!'), "green", ["bold"])        
        exit(0)
    new_m,new_n=cl.computer_move(m,n) #altrimenti il computer fa la sua mossa e m, n assumono i nuovi valori
    TAc.print(LANG.render_feedback("server-move", f'My move is from conf ({m},{n}) to conf ({new_m},{new_n}).\nThe turn is now to you, on conf ({new_m},{new_n})'), "green", ["bold"])
    
    if ENV['watch_value'] == 'watch_winner':
        if cl.grundy_val(new_m, new_n) > 0 :
            TAc.print(LANG.render_feedback("watch-winner-user-after-server", f'You want to watch the winner: starting from this configuration ({new_m}, {new_n}) you will win the game'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("watch-winner-server-after-server", f'You want to watch the winner: starting from this configuration ({new_m}, {new_n}) i will win the game'), "green", ["bold"])
    elif ENV['watch_value'] == 'num_winning_moves' :
        win_moves = cl.winning_moves(new_m, new_n)
        win_moves.discard((None, None))
        if len(win_moves) >= 1:
            TAc.print(LANG.render_feedback("num-winning-moves-n", f'You want to know the number of winning moves: for the current configuration ({new_m}, {new_n}) the number of winning moves is {len(win_moves)}'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("num-winning-moves-0", f'You want to know the number of winning moves: for the current configuration ({new_m}, {new_n}) there are not winning moves'), "green", ["bold"])
    elif(ENV['watch_value'] == 'list_winning_moves'):
        win_moves = cl.winning_moves(new_m, new_n)
        win_moves.discard((None, None))
        if len(win_moves) > 1:
            TAc.print(LANG.render_feedback("list-multiple-winning-moves", f'You want to know the winning moves: for the current configuration ({new_m}, {new_n}) the winning moves are {win_moves}'), "green", ["bold"])
        elif len(win_moves) == 1:
            TAc.print(LANG.render_feedback("list-one-winning-moves", f'You want to know the winning moves: for the current configuration ({new_m}, {new_n}) the winning move is {win_moves}'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("list-none-winning-moves", f'You want to know the winning moves: for the current configuration ({new_m}, {new_n}) there are not winning moves'), "green", ["bold"])
    elif(ENV['watch_value'] == 'watch_grundy_val'):
        TAc.print(LANG.render_feedback("watch-grundy-server-move", f'You want to watch the grundy value: for the current configuration ({new_m}, {new_n}) the grundy value is {cl.grundy_val(new_m, new_n)}'), "green", ["bold"])

    m,n=new_m,new_n

while True:
    if m==1 and n==1: #se la mossa del computer porta ad avere 1x1 l'utente non ha mosse quindi vince il computer
        TAc.print(LANG.render_feedback("you-have-lost", f'It is your turn to move, on conf (1,1). Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("you-lost", f'You lost!'), "green", ["bold"])        
        exit(0)
    TAc.print(LANG.render_feedback("your-turn", f'It is your turn to move from conf ({m},{n}) to a new conf (m,n).'), "yellow", ["bold"]) #altrimenti l'utente fa la sua mossa
    TAc.print(LANG.render_feedback("user-move", f'Please, insert the two integers m and n separated by spaces: '), "yellow", ["bold"])
    new_m,new_n = TALinput(int, 2, TAc=TAc)
    if new_m != m and new_n != n: #se sono cambiate sia m che n allora è una mossa invalida perchè può cambiare solo una alla volta
        TAc.print(LANG.render_feedback("not-valid", f'No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("double-move", f'You are cheating. A move can not alter both the number of rows (from {m} to {new_m}) and the number of columns (from {n} to {new_n})).'), "red", ["bold"])
        exit(0)
    if new_m == m and new_n == n: #se rimangono invariate entrambe è una mossa invalida perchè almeno una deve cambiare
        TAc.print(LANG.render_feedback("not-valid", f'No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("dull-move", f'You are cheating. Your move must either reduce the number of rows or the number of columns. Otherwise, you have not really moved but simply passed.'), "red", ["bold"])
        exit(0)
    if new_m != m:
        pos = m
        new_pos = new_m
    else:
        pos = n
        new_pos = new_n
    if new_pos > pos: #se la nuova situazione è maggiore della precedente è una mossa invalida
        TAc.print(LANG.render_feedback("not-valid", f'No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("increasing-move", f'With a move the value of a coordinate can not increase from {pos} to {new_pos}. On the contrary, precisely one coordinate must be decreased.'), "red", ["bold"])
        exit(0)
    if new_pos < pos - (pos//2): #se la nuova situazione è minore rispetto la metà della posizione precedente è una mossa invalida
        TAc.print(LANG.render_feedback("not-valid", f'No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("excessive-move", f'No! No valid move can more than half the value of a coordinate. (Here, 2*{new_pos}={2*new_pos} < {pos}).'), "red", ["bold"])
        exit(0)

    if new_m==1 and new_n==1: #se siamo rimasti con una sola riga e una sola colonna il computer non ha più mosse e vince l'utente
        TAc.print(LANG.render_feedback("you-have-won", 'It is my turn to move, on conf (1,1). Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("you-won", f'You won!'), "green", ["bold"])        
        exit(0)
    
    if(ENV['watch_value'] == 'watch_winner'):
        if(cl.grundy_val(new_m, new_n) == 0):
            TAc.print(LANG.render_feedback("watch-winner-user-after-user", f'You want to watch the winner: starting from this configuration ({new_m}, {new_n}) you will win the game'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("watch-winner-server-after-user", f'You want to watch the winner: starting from this configuration ({new_m}, {new_n}) i will win the game'), "green", ["bold"])
    elif ENV['watch_value'] == 'num_winning_moves' :
        win_moves = cl.winning_moves(new_m, new_n)
        win_moves.discard((None, None))
        if len(win_moves) >= 1:
            TAc.print(LANG.render_feedback("num-winning-moves-n", f'You want to know the number of winning moves: for the current configuration ({new_m}, {new_n}) the number of winning moves is {len(win_moves)}'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("num-winning-moves-0", f'You want to know the number of winning moves: for the current configuration ({new_m}, {new_n}) there are not winning moves'), "green", ["bold"])
    elif(ENV['watch_value'] == 'list_winning_moves'):
        win_moves = cl.winning_moves(new_m, new_n)
        win_moves.discard((None, None))
        if len(win_moves) > 1:
            TAc.print(LANG.render_feedback("list-multiple-winning-moves", f'You want to know the winning moves: for the current configuration ({new_m}, {new_n}) the winning moves are {win_moves}'), "green", ["bold"])
        elif len(win_moves) == 1:
            TAc.print(LANG.render_feedback("list-one-winning-moves", f'You want to know the winning moves: for the current configuration ({new_m}, {new_n}) the winning move is {win_moves}'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("list-none-winning-moves", f'You want to know the winning moves: for the current configuration ({new_m}, {new_n}) there are not winning moves'), "green", ["bold"])
    elif (ENV['watch_value'] == 'watch_grundy_val'):
        TAc.print(LANG.render_feedback("watch-grundy-after-user", f'You want to watch the grundy value: for the current configuration ({new_m}, {new_n}) the grundy value is {cl.grundy_val(new_m, new_n)}'), "green", ["bold"])

    m,n=cl.computer_move(new_m,new_n) #altrimenti il computer fa la sua mossa
    TAc.print(LANG.render_feedback("server-move", f'My move is from conf ({new_m},{new_n}) to conf ({m},{n}).\nThe turn is now to you, on conf ({m},{n})'), "green", ["bold"])
    
    if(ENV['watch_value'] == 'watch_winner'):
        if(cl.grundy_val(m,n) > 0):
            TAc.print(LANG.render_feedback("watch-winner-user-after-server", f'You want to watch the winner: starting from this configuration ({m}, {n}) you will win the game'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("watch-winner-server-after-server", f'You want to watch the winner: starting from this configuration ({m}, {n}) i will win the game'), "green", ["bold"])
    elif ENV['watch_value'] == 'num_winning_moves' :
        win_moves = cl.winning_moves(m,n)
        win_moves.discard((None, None))
        if len(win_moves) >= 1:
            TAc.print(LANG.render_feedback("num-winning-moves-n", f'You want to know the number of winning moves: for the current configuration ({m}, {n}) the number of winning moves is {len(win_moves)}'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("num-winning-moves-0", f'You want to know the number of winning moves: for the current configuration ({m}, {n}) there are not winning moves'), "green", ["bold"])
    elif(ENV['watch_value'] == 'list_winning_moves'):
        win_moves = cl.winning_moves(m, n)
        win_moves.discard((None, None))
        if len(win_moves) > 1:
            TAc.print(LANG.render_feedback("list-multiple-winning-moves", f'You want to know the winning moves: for the current configuration ({m}, {n}) the winning moves are {win_moves}'), "green", ["bold"])
        elif len(win_moves) == 1:
            TAc.print(LANG.render_feedback("list-one-winning-moves", f'You want to know the winning moves: for the current configuration ({m}, {n}) the winning move is {win_moves}'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("list-none-winning-moves", f'You want to know the winning moves: for the current configuration ({m}, {n}) there are not winning moves'), "green", ["bold"])
    elif(ENV['watch_value'] == 'watch_grundy_val'):
        TAc.print(LANG.render_feedback("watch-grundy-after-server", f'You want to watch the grundy value: for the current configuration ({m}, {n}) the grundy value is {cl.grundy_val(m,n)}'), "green", ["bold"])