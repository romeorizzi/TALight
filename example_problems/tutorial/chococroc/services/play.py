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
    ('value',int)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
grundy_val = cl.grundy_val(ENV['m'], ENV['n'])
#print(f"grundy_val={grundy_val}")

m=ENV['m']
n=ENV['n']

user_will_lose=False

print_nim=False

if ENV['value']==1:
    print_nim=True

if ENV['player']==0 and grundy_val==0:
    TAc.print(LANG.render_feedback("user-play-first", f'You will play first.'), "yellow", ["bold"])
    user_will_lose=True
    
    while m>1 or n>1:
        (m,n)=cl.player_move(m,n,TAc,LANG)
        if print_nim:
            TAc.print(LANG.render_feedback("nim-conf", f'Single NIM tower: {cl.grundy_val(m,n)}.'), "yellow", ["bold"])
        
        (m,n)=cl.winning_move(m,n)
        TAc.print(LANG.render_feedback("pc-move", f'My move: {m} x {n}.'), "yellow", ["bold"])
        if print_nim:
            TAc.print(LANG.render_feedback("nim-conf", f'Single NIM tower: {cl.grundy_val(m,n)}.'), "yellow", ["bold"])
                
elif ENV['player'] == 1 and grundy_val == 0:
    TAc.print(LANG.render_feedback("bot-play-first", f'I will play first.'), "yellow", ["bold"])
    #user_will_lose=False
    
    while m>1 or n>1:
        (m,n)=cl.computer_decision_move(m,n,TAc,LANG)
        if print_nim:
            TAc.print(LANG.render_feedback("nim-conf", f'Single NIM tower: {cl.grundy_val(m,n)}.'), "yellow", ["bold"])
        user_will_lose=True
            
        if m>1 or n>1:
            (m,n)=cl.player_move(m,n,TAc,LANG)
            if print_nim:
                TAc.print(LANG.render_feedback("nim-conf", f'Single NIM tower: {cl.grundy_val(m,n)}.'), "yellow", ["bold"])
            user_will_lose=False

elif ENV['player'] == 1 and grundy_val > 0:
    TAc.print(LANG.render_feedback("bot-play-first", f'I will play first.'), "yellow", ["bold"])
    user_will_lose=True
    
    while m>1 or n>1:
        (m,n)=cl.winning_move(m, n)
        TAc.print(LANG.render_feedback("pc-move", f'My move: {m} x {n}.'), "yellow", ["bold"])
        if print_nim:
            TAc.print(LANG.render_feedback("nim-conf", f'Single NIM tower: {cl.grundy_val(m,n)}.'), "yellow", ["bold"])
        
        if m>1 or n>1:
            (m,n)=cl.player_move(m,n,TAc,LANG)
            if print_nim:
                TAc.print(LANG.render_feedback("nim-conf", f'Single NIM tower: {cl.grundy_val(m,n)}.'), "yellow", ["bold"])

elif ENV['player'] == 0 and grundy_val > 0:

    TAc.print(LANG.render_feedback("user-play-first", f'You will play first.'), "yellow", ["bold"])
    user_will_lose=False
    
    while m>1 or n>1:
        (m,n)=cl.player_move(m,n,TAc,LANG)
        if print_nim:
            TAc.print(LANG.render_feedback("nim-conf", f'Single NIM tower: {cl.grundy_val(m,n)}.'), "yellow", ["bold"])
        user_will_lose=False
              
        if m>1 or n>1:        
            (m,n)=cl.computer_decision_move(m,n,TAc,LANG)
            if print_nim:
                TAc.print(LANG.render_feedback("nim-conf", f'Single NIM tower: {cl.grundy_val(m,n)}.'), "yellow", ["bold"])
            user_will_lose=True
                    
    
    
if user_will_lose:
    TAc.print(LANG.render_feedback("pc-win", f'You lose.'), "red", ["bold"])

else:
    TAc.print(LANG.render_feedback("user-win", f'You win.'), "green", ["bold"])
        

exit(0)

