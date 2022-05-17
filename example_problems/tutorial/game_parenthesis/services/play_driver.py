#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import random
import game_parenthesis_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="game-parenthesis"
service="play"

args_list = [
    ('formula',str),
    ('TALight_first_to_move',int),
    ('watch',str),
    ('seed',int),
    ('opponent',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

def close_service_and_print_term_signal_for_bots():
    TAc.Finished(only_term_signal=True)
    exit(0)

if ENV['seed']>0:
    random.seed(ENV['seed'])
    length=int(round((random.random())*100,0))
    if length%2!=0:
        if random.choice([True, False]):
            length+=1
        else:
            length-=1
    formula=pl.random_wff(length)
else:
    formula=ENV['formula']

if not pl.recognize(formula, TAc, LANG):
    exit(0)


def I_have_lost():
    if ENV['opponent'] == 'computer':
        TAc.print(LANG.render_feedback("par-TALight_lost", f'# It is my turn to move, on a void formula. Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("par-you-won", f'# You won!'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("par-player-lost-msg", f'# It is the turn of player {pl.player_flip(n_player)} to move, on a void formula. Since this configuration admits no valid move, then player {pl.player_flip(n_player)} has lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("par-player-won", f'# Player {n_player} won!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost():
    TAc.print(LANG.render_feedback("par-you-have-lost", f'# It is your turn to move, on the void formula configuration. Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-you-lost", f'# You lost!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
PLAYER_1_IS = LANG.render_feedback("Player-1-is", 'Player 1 is')
PLAYER_2_IS = LANG.render_feedback("Player-2-is", 'Player 2 is')
def watch(formula, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS] 
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS]
    if ENV["watch"] == 'no_watch':
        return
    TAc.print(f'# watch={ENV["watch"]}: ', "blue", end='')
    if ENV["watch"] == 'watch_winner':
        if(pl.grundy_val(formula) == 0):
            TAc.print(LANG.render_feedback("par-watch-winner-who-moves-loses", f'{second_to_move} ahead, since \'{formula}\' is a who-moves-loses configuration.'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-watch-winner-who-moves-wins", f'{first_to_move} ahead, since \'{formula}\' is a who-moves-wins configuration.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        win_moves = pl.find_moves_game_parenthesis(formula)
        if len(win_moves) > 0:
            TAc.print(LANG.render_feedback("par-num-winning-moves-n", f'the current formula \'{formula}\' admits {len(win_moves)} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-num-winning-moves-0", f'the current formula \'{formula}\' admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        win_moves = pl.find_moves_game_parenthesis(formula, True)
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



if ENV["TALight_first_to_move"] == 1 and ENV['opponent'] == 'computer': # if the user plays the match as second to move
    if formula=='': # no valid moves on the formula ''. TALight first to move loses the match
        I_have_lost()
    
    watch(formula, first_to_move=I_AM, second_to_move=YOU_ARE)
        
    # TALight makes its move updating the new formula:
    new_formula=pl.computer_move(formula)
    TAc.print(LANG.render_feedback("par-server-move", f'# My move is from formula \'{formula}\' to new formula \'{new_formula}\'.'), "green", ["bold"])
    formula=new_formula

n_player=1

while True:
    if formula=='': # the formula '' admits no valid move. The turn is to the user who has no move available and loses the match. TALight wins.
        you_have_lost()
    if ENV['opponent'] == 'computer':
        watch(formula, first_to_move=YOU_ARE, second_to_move=I_AM)
    else:
        if n_player==1:
            watch(formula, first_to_move=PLAYER_1_IS, second_to_move=PLAYER_2_IS)
        else:
            watch(formula, first_to_move=PLAYER_2_IS, second_to_move=PLAYER_1_IS)
    if ENV['opponent'] == 'computer':  
        TAc.print(LANG.render_feedback("par-your-turn", f'# It is your turn to move from configuration/formula \'{formula}\' to a new configuration of the game. The new configuration must be a well-formed subformula of the current formula.'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("par-player-turn", f'# It is the turn of player {n_player} to move from configuration/formula \'{formula}\' to a new configuration of the game. The new configuration must be a well-formed subformula of the current formula.'), "yellow", ["bold"])
    if pl.verify_move_game_parenthesis(formula, ")("):
        TAc.print(LANG.render_feedback("par-user-move-if-can-terminate", f'# Please, insert the new formula you intend to move to just underneath the current formula. NOTE: Write just the two characters string ")(" if you intend to move to the empty formula.'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("par-user-move", f'# Please, insert the new formula just underneath the current formula as reported here: '), "yellow", ["bold"])

    TAc.print(LANG.render_feedback("par-prompt", f'{formula}'), "yellow", ["bold"])
    new_formula, = TALinput(str, 1, TAc=TAc)
    
    if not pl.verify_char(new_formula):
        TAc.print(LANG.render_feedback("par-stranger-char", '# We have a problem. The formula has one or more char that is not a parentheses.'), "red", ["bold"])
        exit(0)
    if new_formula==formula:
        TAc.print(LANG.render_feedback("par-dull-move", '# We have a problem. You can\'t pass. You must move on the game.'), "red", ["bold"])
        exit(0)
    if not pl.verify_move_game_parenthesis(formula, new_formula):
        TAc.print(LANG.render_feedback("par-illegal-move", '# We have a problem. Your move is not valid. You must remove ONE well made formula.'), "red", ["bold"])
        if new_formula!=')(':
            pl.recognize(new_formula, TAc, LANG)
        exit(0)

    if new_formula==')(': # TALight has no valid move available and loses the match. The user wins.
        I_have_lost()

    if ENV['opponent'] == 'computer':
        watch(new_formula, first_to_move=I_AM, second_to_move=YOU_ARE)
        formula=pl.computer_move(new_formula) # TALight makes its move
        TAc.print(LANG.render_feedback("par-server-move", f'# My move is from formula \'{new_formula}\' to new formula \'{formula}\'.'), "green", ["bold"])
    else:
        n_player=pl.player_flip(n_player)
        formula=new_formula