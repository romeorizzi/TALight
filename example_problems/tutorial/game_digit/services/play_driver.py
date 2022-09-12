#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import random
import game_digit_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="game_digit"
service="play"

args_list = [
    ('number',int),
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
    number=int(round((random.random())*100,0))
    if number<10:
        number=number*10
else:
    number=ENV['number']

def I_have_lost():
    if ENV['opponent'] == 'computer':
        TAc.print(LANG.render_feedback("numb-TALight_lost", f'# It is my turn to move, on the number 0. Since this number admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("numb-you-won", f'# You won!'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("numb-player-lost-msg", f'# It is the turn of player {cl.player_flip(n_player)} to move, on the number 0. Since this number admits no valid move, then player {cl.player_flip(n_player)} has lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("numb-player-won", f'# Player {n_player} won!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost():
    TAc.print(LANG.render_feedback("numb-you-have-lost", f'# It is your turn to move, on the number 0. Since this number admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("numb-you-lost", f'# You lost!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
PLAYER_1_IS = LANG.render_feedback("Player-1-is", 'Player 1 is')
PLAYER_2_IS = LANG.render_feedback("Player-2-is", 'Player 2 is')
def watch(number, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS] 
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS]
    if ENV["watch"] == 'no_watch':
        return
    TAc.print(f'# watch={ENV["watch"]}: ', "blue", end='')
    if ENV["watch"] == 'watch_winner':
        if(cl.grundy_val(number) == 0):
            TAc.print(LANG.render_feedback("numb-watch-winner-who-moves-loses", f'{second_to_move} ahead, since \'{number}\' is a who-moves-loses number.'), "blue")
        else:
            TAc.print(LANG.render_feedback("numb-watch-winner-who-moves-wins", f'{first_to_move} ahead, since \'{number}\' is a who-moves-wins number.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        win_moves = cl.find_winning_move(number)
        if len(win_moves) > 0:
            TAc.print(LANG.render_feedback("numb-num-winning-moves-n", f'the current number \'{number}\' admits {len(win_moves)} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("numb-num-winning-moves-0", f'the current number \'{number}\' admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        win_moves = cl.find_winning_move(number)
        if len(win_moves) > 0:
            TAc.print(LANG.render_feedback("numb-list-one-winning-move", f'for the current number \'{number}\' the winning move is \'{win_moves[0]}\''), "blue")
        else:
            TAc.print(LANG.render_feedback("numb-list-none-winning-moves", f'the current number \'{number}\' admits no winning move'), "blue")
    elif ENV['watch'] == 'watch_grundy_val':
        TAc.print(LANG.render_feedback("numb-watch-grundy-val", f'the current number \'{number}\' has grundy value {cl.grundy_val(number)}'), "blue")



if ENV["TALight_first_to_move"] == 1 and ENV['opponent'] == 'computer': # if the user plays the match as second to move
    if number==0: # no valid moves on the number ''. TALight first to move loses the match
        I_have_lost()
    
    watch(number, first_to_move=I_AM, second_to_move=YOU_ARE)
        
    # TALight makes its move updating the new number:
    new_number=cl.computer_move(number)
    TAc.print(LANG.render_feedback("numb-server-move", f'# My move is from number {number} to the new number {new_number}={number}-{number-new_number} obtained from the previous one by subtracting from it one of its non-zero digits ({number-new_number}).'), "green", ["bold"])
    number=new_number

n_player=1

while True:
    if number==0: # the number '' admits no valid move. The turn is to the user who has no move available and loses the match. TALight wins.
        you_have_lost()
    if ENV['opponent'] == 'computer':
        watch(number, first_to_move=YOU_ARE, second_to_move=I_AM)
    else:
        if n_player==1:
            watch(number, first_to_move=PLAYER_1_IS, second_to_move=PLAYER_2_IS)
        else:
            watch(number, first_to_move=PLAYER_2_IS, second_to_move=PLAYER_1_IS)
    if ENV['opponent'] == 'computer':  
        TAc.print(LANG.render_feedback("numb-your-turn", f'# It is your turn to move from number \'{number}\' to a new number produced according to the rules of the game. Each new number must be obtained from the previous one by subtracting one of its non-zero digits to its value.'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("numb-player-turn", f'# It is the turn of player {n_player} to move from number \'{number}\' to a new number produced according to the rules of the game. Each new number must be obtained from the previous one by subtracting one of its non-zero digits to its value.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("numb-user-move", f'# Please, insert the new number just underneath the current number as reported here: '), "yellow", ["bold"])

    TAc.print(LANG.render_feedback("numb-prompt", f'{number}'), "yellow", ["bold"])
    new_number, = TALinput(int, 1, TAc=TAc)

    if new_number==number:
        TAc.print(LANG.render_feedback("numb-dull-move", '# We have a problem. You can\'t pass. You must move on the game.'), "red", ["bold"])
        exit(0)
    if not cl.verify_move(number, new_number):
        TAc.print(LANG.render_feedback("numb-illegal-move", f'# We have a problem. Your move is not valid. Your viable options were those numbers that could have been obtained from {number} by subtracting to it one of its non-zero digits (as in its decimal representation). That is, you had to choose and subtract from {number} precisely one among {", ".join(str(number - valid_new_number) for valid_new_number in cl.find_all_moves(number,True))}, hence returning one among {", ".join(str(valid_new_number) for valid_new_number in cl.find_all_moves(number,True))}.'), "red", ["bold"])
        exit(0)

    if new_number==0: # TALight has no valid move available and loses the match. The user wins.
        I_have_lost()

    if ENV['opponent'] == 'computer':
        watch(new_number, first_to_move=I_AM, second_to_move=YOU_ARE)
        number=cl.computer_move(new_number) # TALight makes its move
        TAc.print(LANG.render_feedback("numb-server-move", f'# My move is from number {new_number} to the new number {number}={new_number}-{new_number-number} obtained from the previous one by subtracting from it one of its non-zero digits ({new_number-number}).'), "green", ["bold"])
    else:
        n_player=cl.player_flip(n_player)
        number=new_number
