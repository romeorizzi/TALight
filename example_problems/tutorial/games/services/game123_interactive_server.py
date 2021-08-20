#!/usr/bin/env python3
from sys import stderr, exit
from random import randrange

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

# METADATA OF THIS TAL_SERVICE:
problem="games"
service="game123_interactive"
args_list = [
    ('instance',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
feedback="" 
i=0
if ENV['instance']=='random':
    s = randrange(5,30)
if ENV['instance']=='my':
    TAc.print("Insert the instance:", "yellow", ["bold"])
    s = TALinput(int, 1, TAc=TAc)[0]  
while s!=0:
    TAc.print(f"Round {i}", "blue", ["bold"])
    TAc.print(f"Number of pawns: {s}. Your move?  ", "yellow", ["bold"])
    a= TALinput(int, 1, TAc=TAc)[0]
    if a>3:
        TAc.NO() 
        TAc.print(LANG.render_feedback("wrong-intput", "Attention! Wrong input!"), "red", ["bold"]) 
        exit(0)
    else:
        if s%4==a and a==0:
            TAc.print(LANG.render_feedback("lose", "You lose"), "red", ["bold"]) 
            exit(0)
        if s%4!=a:
            feedback+=f'{i}'
            feedback+=' '
    s=s-a
    
    
    if s!=0:
        if s%4!=0:
            my_move=s%4
            
        else:
            my_move=randrange(1,4)
        TAc.print(f"Now there are {s} pawns. My move is {my_move}. ", "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("win", "I lose, you win"), "green", ["bold"])
        exit(0)
        
    s=s-my_move
    i=i+1
TAc.print(LANG.render_feedback("lose", "You lose"), "red", ["bold"])
TAc.print(LANG.render_feedback("lose", f"You could have done better in the round: {feedback}"), "green", ["underline"])
exit(0)
