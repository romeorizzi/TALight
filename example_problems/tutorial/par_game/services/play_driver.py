#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import par_game_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="par_game"
service="play"

args_list = [
    ('formula',str),
    ('TALight_first_to_move',int),
    ('watch',str),
    ('random',int),
    ('length',int)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

def close_service_and_print_term_signal_for_bots():
    TAc.Finished(only_term_signal=True)
    exit(0)

if ENV['random']==1:
    if ENV['length']%2!=0:
        TAc.print(LANG.render_feedback("par-wrong-length", f'# The length is not correct. I need an even number to generate a correct formula.'), "red", ["bold"])
        exit(0)
    else:
        formula=pl.random_wff(ENV['length'])
else:
    formula=ENV['formula']

if not pl.recognize(formula, TAc, LANG):
    exit(0)

TAc.print(LANG.render_feedback("par-void-formula", f'# Remember that if you want give input a void formula, you must use the formula \')(\'.'), "yellow", ["bold"])

def I_have_lost():
    TAc.print(LANG.render_feedback("par-TALight_lost", f'# It is my turn to move, on a void formula. Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-you-won", f'# You won!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost():
    TAc.print(LANG.render_feedback("par-you-have-lost", f'# It is your turn to move, on a void formula. Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-you-lost", f'# You lost!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
def watch(formula, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS] 
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS]
    if ENV["watch"] == 'no_watch':
        return
    TAc.print(f'# watch={ENV["watch"]}: ', "blue", end='')
    if ENV["watch"] == 'watch_winner':
        if(pl.grundy_val(formula) == 0):
            TAc.print(LANG.render_feedback("par-watch-winner-who-moves-loses", f'{second_to_move} ahead, since \'{formula}\' is a who-moves-loses configuration.'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-watch-winner-who-moves-wins", f'{first_to_move} ahead, since \'{formula}\' is a who-moves-wins configuration.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        win_moves = pl.find_moves(formula)
        if len(win_moves) > 0:
            TAc.print(LANG.render_feedback("par-num-winning-moves-n", f'the current formula \'{formula}\' admits {len(win_moves)} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-num-winning-moves-0", f'the current formula \'{formula}\' admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        win_moves = pl.find_moves(formula, True)
        if len(win_moves) > 1:
            TAc.print(LANG.render_feedback("par-list-multiple-winning-moves", f'for the current formula \'{formula}\' the winning moves are {win_moves}'), "blue")
            TAc.print('# The duplicates are removed, if the result formula is the same', "blue")
        elif len(win_moves) == 1:
            TAc.print(LANG.render_feedback("par-list-one-winning-move", f'for the current formula \'{formula}\' the winning move is {win_moves}'), "blue")
            TAc.print('# The duplicates are removed, if the result formula is the same', "blue")
        else:
            TAc.print(LANG.render_feedback("par-list-none-winning-moves", f'the current formula \'{formula}\' admits no winning move'), "blue")
    elif ENV['watch'] == 'watch_grundy_val':
        TAc.print(LANG.render_feedback("par-watch-grundy-val", f'the current formula \'{formula}\' has grundy value {pl.grundy_val(formula)}'), "blue")



if ENV["TALight_first_to_move"] == 1: # if the user plays the match as second to move
    watch(formula, first_to_move=I_AM, second_to_move=YOU_ARE)
    if formula=='': # no valid moves on the formula ''. TALight first to move loses the match
        I_have_lost()
        
    # TALight makes its move updating the new formula:
    new_formula=pl.computer_move(formula)
    TAc.print(LANG.render_feedback("par-server-move", f'# My move is from formula \'{formula}\' to new formula \'{new_formula}\'.'), "green", ["bold"])
    formula=new_formula

while True:
    if formula=='': # the formula '' admits no valid move. The turn is to the user who has no move available and loses the match. TALight wins.
        you_have_lost()
    
    watch(formula, first_to_move=YOU_ARE, second_to_move=I_AM)    
    TAc.print(LANG.render_feedback("par-your-turn", f'# It is your turn to move from formula \'{formula}\' to a new formula.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-user-move", f'# Please, insert the new formula just underneath the current formula we put you into: '), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-prompt", f'{formula}'), "yellow", ["bold"])
    new_formula, = TALinput(str, 1, TAc=TAc)
    
    if not pl.verify_char(new_formula):
        TAc.print(LANG.render_feedback("par-stranger-char", "We have a problem. The formula has one or more char that is not a parentheses."), "red", ["bold"])
        exit(0)
    if not pl.verify_moves(formula, new_formula):
        TAc.print(LANG.render_feedback("par-illegal-move", "We have a problem. Your move is not valid. You must remove ONE well made formula."), "red", ["bold"])
        if new_formula!=')(':
            pl.recognize(new_formula, TAc, LANG)
        exit(0)
    if new_formula==')(': # TALight has no valid move available and loses the match. The user wins.
        I_have_lost()
    
    watch(new_formula, first_to_move=I_AM, second_to_move=YOU_ARE)    
    formula=pl.computer_move(new_formula) # TALight makes its move
    TAc.print(LANG.render_feedback("par-server-move", f'# My move is from formula \'{new_formula}\' to new formula \'{formula}\'.'), "green", ["bold"])
