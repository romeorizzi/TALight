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
    ('watch_value',str),
    ('game',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

m=ENV['m']
n=ENV['n']
if ENV['player'] == 1:
    if m==1 and n==1:
        TAc.print(LANG.render_feedback("you-won", 'It is my turn to move, on conf (1,1). Since this configuration admits no valid move, then I have lost this match.'), "white", ["bold"])
        TAc.print(LANG.render_feedback("you-won", f'You won!'), "green", ["bold"])        
        exit(0)
    new_m,new_n=cl.computer_move(m,n)
    TAc.print(LANG.render_feedback("server-move", f'My move is from conf ({m},{n}) to conf ({new_m},{new_n}).\nThe turn is now to you, on conf ({new_m},{new_n})'), "green", ["bold"])
    m,n=new_m,new_n    
while True:
    if m==1 and n==1:
        TAc.print(LANG.render_feedback("you-have-lost", f'It is your turn to move, on conf (1,1). Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("you-lost", f'You lost!'), "green", ["bold"])        
        exit(0)
    TAc.print(LANG.render_feedback("your-turn", f'It is your turn to move from conf ({m},{n}) to a new conf (m,n).'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("server-move", f'Please, insert the two integers m and n separated by spaces: '), "yellow", ["bold"])
    new_m,new_n = TALinput(int, 2, TAc=TAc)
    if new_m != m and new_n != n:
        TAc.print(LANG.render_feedback("not-valid", f'No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("double-move", f'You are cheating. A move can not alter both the number of rows (from {m} to {new_m}) and the number of columns (from {n} to {new_n})).'), "red", ["bold"])
        exit(0)
    if new_m == m and new_n == n:
        TAc.print(LANG.render_feedback("not-valid", f'No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("dull-move", f'You are cheating. Your move must either reduce the number of rows or the number of columns. Otherwise, you have not really moved but simply passed.'), "red", ["bold"])
        exit(0)
    if new_m != m:
        pos = m
        new_pos = new_m
    else:
        pos = n
        new_pos = new_n
    if new_pos > pos:
        TAc.print(LANG.render_feedback("not-valid", f'No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("increasing-move", f'With a move the value of a coordinate can not increase from {a} to {new_a}. On the contrary, precisely one coordinate must be decreased.'), "red", ["bold"])
        exit(0)
    if new_pos < pos - (pos//2):
        TAc.print(LANG.render_feedback("not-valid", f'No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("excessive-move", f'No! No valid move can more than halve the value of a coordinate. (Here, 2*{new_pos}={2*new_pos} < {pos}.'), "red", ["bold"])
        exit(0)

    if new_m==1 and new_n==1:
        TAc.print(LANG.render_feedback("you-won", 'It is my turn to move, on conf (1,1). Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("you-won", f'You won!'), "green", ["bold"])        
        exit(0)
    m,n=cl.computer_move(new_m,new_n)
    TAc.print(LANG.render_feedback("server-move", f'My move is from conf ({new_m},{new_n}) to conf ({m},{n}).\nThe turn is now to you, on conf ({m},{n})'), "green", ["bold"])


exit(0)

