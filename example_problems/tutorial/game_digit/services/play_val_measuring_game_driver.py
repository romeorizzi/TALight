#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import random
import game_digit_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="game_digit"
service="play_val_measuring_game"

args_list = [
    ('number',int),
    ('nim',int),
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

nim=ENV['nim']

env_number=number

def I_have_lost():
    if ENV['opponent'] == 'computer':
        TAc.print(LANG.render_feedback("numb-TALight_lost-nim", f'# It is my turn to move, on conf <game_digit(0) + nim(0)> of the MeasuringGame(game_digit) game, that is, the number \'0\' (plus an empty Nim tower). Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("numb-you-won", f'# You won!'), "green", ["bold"])
        if ENV["TALight_first_to_move"] == 0:
            TAc.print(LANG.render_feedback("numb-wrong-grundy-val", f'# Since we played optimally, you have successfully proven that the Grundy value of the game_digit game configuration game_digit(\'{env_number}\') is NOT the number {ENV["nim"]}.'), "green", ["bold"])        
        else:
            TAc.print(LANG.render_feedback("numb-correct-grundy-val", f'# Since we played optimally, you have successfully proven that the Grundy value of the game_digit game configuration game_digit(\'{env_number}\') is precisely {ENV["nim"]}.'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("numb-player-lost-msg-nim", f'# It is the turn of player {cl.player_flip(n_player)} to move, on conf <game_digit(0) + nim(0)> of the MeasuringGame(game_digit) game, that is, the number \'0\' (plus an empty Nim tower). Since this configuration admits no valid move, then player {cl.player_flip(n_player)} has lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("numb-player-won-nim", f'# Player {n_player} won!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost():
    TAc.print(LANG.render_feedback("numb-you-have-lost-nim", f'# It is your turn to move, on conf <game_digit(0) + nim(0)> of the MeasuringGame(game_digit) game, that is, the number \'0\' (plus an empty Nim tower). Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("numb-you-lost", f'# You lost!'), "green", ["bold"])
    if ENV["TALight_first_to_move"] == 0:
        TAc.print(LANG.render_feedback("numb-correct-grundy-val-or-bad-move", f'# The cases are two: either during this play you trew away a win with a bad move, or we have convinced you that the Grundy value of the game_digit game configuration game_digit(\'{env_number}\') is precisely {ENV["nim"]}.'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("numb-wrong-grundy-val-or-bad-move", f'# The cases are two: either during this play you trew away a win with a bad move, or we have convinced you that the Grundy value of the game_digit game configuration game_digit(\'{env_number}\') is NOT the number {ENV["nim"]}.'), "green", ["bold"])        
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
PLAYER_1_IS = LANG.render_feedback("Player-1-is", 'Player 1 is')
PLAYER_2_IS = LANG.render_feedback("Player-2-is", 'Player 2 is')
def watch(number,nim, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS] 
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS]
    if ENV["watch"] == 'no_watch':
        return
    TAc.print('# watch={ENV["watch"]}: ', "blue", end='')
    if ENV["watch"] == 'watch_winner':
        number_grundy_value = cl.grundy_val(number)
        if(cl.grundy_sum(number_grundy_value, nim) == 0):
            TAc.print(LANG.render_feedback("numb-watch-winner-who-moves-loses-nim", f'{second_to_move} ahead, since <game_digit({number}) + nim({nim})> is a who-moves-loses configuration.'), "blue")
        else:
            TAc.print(LANG.render_feedback("numb-watch-winner-who-moves-wins-nim", f'{first_to_move} ahead, since <game_digit({number}) + nim({nim})> is a who-moves-wins configuration.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        win_moves = cl.find_winning_moves_game_digit_nim(number,nim,False)
        if (len(win_moves))>0:
            TAc.print(LANG.render_feedback("numb-num-winning-moves-n-nim", f'the current configuration <game_digit({number}) + nim({nim})> admits {len(win_moves)} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("numb-num-winning-moves-0-nim", f'the current configuration <game_digit({number}) + nim({nim})> admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        win_moves = cl.find_winning_moves_game_digit_nim(number,nim,True)
        if len(win_moves) > 1:
            TAc.print(LANG.render_feedback("numb-list-multiple-winning-moves-nim", f'for the current configuration <game_digit({number}) + nim({nim})> the winning moves are {win_moves}'), "blue")
            TAc.print('# The duplicates are removed, if the result number is the same', "blue")
        elif len(win_moves) == 1:
            TAc.print(LANG.render_feedback("numb-list-one-winning-move-nim", f'for the current configuration <game_digit({number}) + nim({nim})> the winning move is {win_moves}'), "blue")
            TAc.print('# The duplicates are removed, if the result number is the same', "blue")
        else:
            TAc.print(LANG.render_feedback("numb-list-none-winning-moves-nim", f'the current configuration <game_digit({number}) + nim({nim})> admits no winning move'), "blue")
    elif ENV['watch'] == 'watch_grundy_val':
        number_grundy_value = cl.grundy_val(number)
        TAc.print(LANG.render_feedback("numb-watch-grundy-val-nim", f'the current configuration <game_digit({number}) + nim({nim})> has grundy value {cl.grundy_sum(number_grundy_value, nim)}'), "blue")


        
if ENV["TALight_first_to_move"] == 1 and ENV['opponent'] == 'computer': # if the user plays the match as second to move
    if number==0 and nim==0: # no valid moves on the configuration '' 0. TALight first to move loses the match
        I_have_lost()
    
    watch(number, nim, first_to_move='I am', second_to_move='you are')
    
    new_number,new_nim=cl.computer_move_nim(number,nim)
    TAc.print(LANG.render_feedback("numb-server-move-play-val", f'# My move is from conf <game_digit({number}) + nim({nim})> to conf <game_digit({new_number}) + nim({new_nim})>.'), "green", ["bold"])
    number,nim=new_number,new_nim

n_player=1

while True:
    if number==0 and nim==0:
        you_have_lost()
    if ENV['opponent'] == 'computer':    
        watch(number, nim, first_to_move=YOU_ARE, second_to_move=I_AM)
    else:
        if n_player==1:
            watch(number, nim, first_to_move=PLAYER_1_IS, second_to_move=PLAYER_2_IS)
        else:
            watch(number, nim, first_to_move=PLAYER_2_IS, second_to_move=PLAYER_1_IS)
    if ENV['opponent'] == 'computer':  
        TAc.print(LANG.render_feedback("numb-your-turn-play-val", f'# It is your turn to move from conf <game_digit(number={number}) + nim(height={nim})> of the MeasuringGame(game_digit) game to a new conf of the MeasuringGame(game_digit) game <game_digit(number\') + nim(height\')>. You should move either on the game_digit component or on the nim component of the game.'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("numb-player-turn-play-val", f'# It is the turn of player {n_player} to move from conf <game_digit(number={number}) + nim(height={nim})> of the MeasuringGame(game_digit) game to a new conf of the MeasuringGame(game_digit) game <game_digit(number\') + nim(height\')>. Player {n_player} should move either on the game_digit component or on the nim component of the game.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("numb-user-move-play-val", f'# Please, insert the number\' and height\' encoding the new configuration produced by your move just underneath the current configuration as reported here: '), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("numb-prompt_nim", f'{number} {nim}'), "yellow", ["bold"])
    new_number,new_nim = TALinput(int, 2, TAc=TAc)

    if new_number!=number and new_nim==nim:
        if number!=0:
            if not cl.verify_move(number, new_number):
                TAc.print(LANG.render_feedback("numb-illegal-move", '# We have a problem. Your move is not valid. You must subtract ONE digit of the number.'), "red", ["bold"])
                exit(0)
        else:
            TAc.print(LANG.render_feedback("numb-illegal-void-move", '# We have a problem. Your move is not valid. You can\'t move on the number \'0\'.'), "red", ["bold"])
            exit(0)
    elif new_number!=number and new_nim!=nim:
        TAc.print(LANG.render_feedback("numb-double-move", '# We have a problem. You can\'t move on both game_digit and nim.'), "red", ["bold"])
        exit(0)
    elif new_number==number and new_nim==nim:
        TAc.print(LANG.render_feedback("numb-dull-nim-move", '# We have a problem. You can\'t pass. You must move at least on ONE of the two games.'), "red", ["bold"])
        exit(0)
    elif new_number==number and new_nim>nim:
        TAc.print(LANG.render_feedback("numb-grow-nim-move", '# We have a problem. A move can\'t increase the height of the nim tower.'), "red", ["bold"])
        exit(0)
    elif new_number==number and new_nim<0:
        TAc.print(LANG.render_feedback("numb-negative-nim-move", '# We have a problem. A move can\'t decrease the height of the nim tower under 0.'), "red", ["bold"])
        exit(0)

    if new_number==0 and new_nim==0:
        I_have_lost()
    
    if ENV['opponent'] == 'computer':
        watch(new_number,new_nim, first_to_move=I_AM, second_to_move=YOU_ARE)    
        number,nim=cl.computer_move_nim(new_number,new_nim)
        TAc.print(LANG.render_feedback("numb-server-move-play-val", f'# My move is from conf <game_digit({new_number}) + nim({new_nim})> to conf <game_digit({number}) + nim({nim})>.'), "green", ["bold"])
    else:
        n_player=cl.player_flip(n_player)
        number=new_number
        nim=new_nim
