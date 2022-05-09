#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import random
import game_parenthesis_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="game-parenthesis"
service="play_val_measuring_game"

args_list = [
    ('formula',str),
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
    length=int(round((random.random())*100,0))
    if length%2!=0:
        if random.choice([True, False]):
            length+=1
        else:
            length-=1
    formula=pl.random_wff(length)
else:
    formula=ENV['formula']

nim=ENV['nim']

if not pl.recognize(formula, TAc, LANG):
    exit(0)

env_formula=formula
if formula=='':
    formula=')('


def I_have_lost(env_formula, n_player_winner):
    if ENV['opponent'] == 'computer':
        TAc.print(LANG.render_feedback("par-TALight_lost-nim", f'# It is my turn to move, on conf <game-parenthesis(\'\') + nim(0)> of the MeasuringGame(Game-parenthesis) game, that is, a void formula (plus an empty Nim tower). Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("par-you-won", f'# You won!'), "green", ["bold"])
        if ENV["TALight_first_to_move"] == 0:
            TAc.print(LANG.render_feedback("par-wrong-grundy-val", f'# Since we played optimally, you have successfully proven that the Grundy value of the Game-parenthesis game configuration game-parenthesis(\'{env_formula}\') is NOT the number {ENV["nim"]}.'), "green", ["bold"])        
        else:
            TAc.print(LANG.render_feedback("par-correct-grundy-val", f'# Since we played optimally, you have successfully proven that the Grundy value of the Game-parenthesis game configuration game-parenthesis(\'{env_formula}\') is precisely {ENV["nim"]}.'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("par-player-lost-msg-nim", f'# It the turn of player {pl.player_flip(n_player_winner)} to move, on conf <game-parenthesis(\'\') + nim(0)> of the MeasuringGame(Game-parenthesis) game, that is, a void formula (plus an empty Nim tower). Since this configuration admits no valid move, then player {pl.player_flip(n_player_winner)} has lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("par-player-won-nim", f'# Player {n_player_winner} won!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost(env_formula):
    TAc.print(LANG.render_feedback("par-you-have-lost-nim", f'# It is your turn to move, on conf <game-parenthesis(\'\') + nim(0)> of the MeasuringGame(Game-parenthesis) game, that is, a void formula (plus an empty Nim tower). Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-you-lost", f'# You lost!'), "green", ["bold"])
    if ENV["TALight_first_to_move"] == 0:
        TAc.print(LANG.render_feedback("par-correct-grundy-val-or-bad-move", f'# The cases are two: either during this play you trew away a win with a bad move, or we have convinced you that the Grundy value of the Game-parenthesis game configuration game-parenthesis(\'{env_formula}\') is precisely {ENV["nim"]}.'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("par-wrong-grundy-val-or-bad-move", f'# The cases are two: either during this play you trew away a win with a bad move, or we have convinced you that the Grundy value of the Game-parenthesis game configuration game-parenthesis(\'{env_formula}\') is NOT the number {ENV["nim"]}.'), "green", ["bold"])        
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
PLAYER_1_IS = LANG.render_feedback("Player-1-is", 'Player 1 is')
PLAYER_2_IS = LANG.render_feedback("Player-2-is", 'Player 2 is')
def watch(formula,nim, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS] 
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS]
    if ENV["watch"] == 'no_watch':
        return
    TAc.print('# watch={ENV["watch"]}: ', "blue", end='')
    if ENV["watch"] == 'watch_winner':
        if formula == '' or formula == ')(':
            formula_grundy_value = 0
        else:
            formula_grundy_value = pl.grundy_val(formula)
        if(pl.grundy_sum(formula_grundy_value, nim) == 0):
            TAc.print(LANG.render_feedback("par-watch-winner-who-moves-loses-nim", f'{second_to_move} ahead, since <game-parenthesis(\'{formula}\') + nim({nim})> is a who-moves-loses configuration.'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-watch-winner-who-moves-wins-nim", f'{first_to_move} ahead, since <game-parenthesis(\'{formula}\') + nim({nim})> is a who-moves-wins configuration.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        if formula != '' and formula != ')(':
            win_moves = pl.find_moves_game_parenthesis(formula, False, nim)
        else:
            win_moves = []
        count_win_moves=pl.count_winning_moves_nim(formula, nim)
        if (len(win_moves)+count_win_moves)>0:
            TAc.print(LANG.render_feedback("par-num-winning-moves-n-nim", f'the current configuration <game-parenthesis(\'{formula}\') + nim({nim})> admits {len(win_moves)+count_win_moves} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-num-winning-moves-0-nim", f'the current configuration <game-parenthesis(\'{formula}\') + nim({nim})> admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        if formula != '' and formula != ')(':
            win_moves = pl.find_moves_game_parenthesis(formula, True, nim)
        else:
            win_moves = []
        win_moves_with_nim={(None,None)}
        for wff in win_moves:
            wff=(wff,nim)
            win_moves_with_nim.add(wff)
        win_moves_with_nim.discard((None,None))
        win_moves_with_nim.update(pl.winning_moves_nim(formula, nim))
        if len(win_moves_with_nim) > 1:
            TAc.print(LANG.render_feedback("par-list-multiple-winning-moves-nim", f'for the current configuration <game-parenthesis(\'{formula}\') + nim({nim})> the winning moves are {win_moves_with_nim}'), "blue")
            TAc.print('# The duplicates are removed, if the result formula is the same', "blue")
        elif len(win_moves_with_nim) == 1:
            TAc.print(LANG.render_feedback("par-list-one-winning-move-nim", f'for the current configuration <game-parenthesis(\'{formula}\') + nim({nim})> the winning move is {win_moves_with_nim}'), "blue")
            TAc.print('# The duplicates are removed, if the result formula is the same', "blue")
        else:
            TAc.print(LANG.render_feedback("par-list-none-winning-moves-nim", f'the current configuration <game-parenthesis(\'{formula}\') + nim({nim})> admits no winning move'), "blue")
    elif ENV['watch'] == 'watch_grundy_val':
        if formula == '' or formula == ')(':
            formula_grundy_value = 0
        else:
            formula_grundy_value = pl.grundy_val(formula)
        TAc.print(LANG.render_feedback("par-watch-grundy-val-nim", f'the current configuration <game-parenthesis(\'{formula}\') + nim({nim})> has grundy value {pl.grundy_sum(formula_grundy_value, nim)}'), "blue")


        
if ENV["TALight_first_to_move"] == 1 and ENV['opponent'] == 'computer': # if the user plays the match as second to move
    if (formula=='' or formula==')(') and nim==0: # no valid moves on the configuration '' 0. TALight first to move loses the match
        I_have_lost(env_formula)
    
    watch(formula, nim, first_to_move='I am', second_to_move='you are')
    
    new_formula,new_nim=pl.computer_decision_move(formula,nim)
    TAc.print(LANG.render_feedback("par-server-move-play-val", f'# My move is from conf <game-parenthesis(\'{formula}\') + nim({nim})> to conf <game-parenthesis(\'{new_formula}\') + nim({new_nim})>.'), "green", ["bold"])
    formula,nim=new_formula,new_nim

n_player=1

while True:
    if (formula==')(' or formula=='') and nim==0:
        you_have_lost(env_formula)
    if ENV['opponent'] == 'computer':    
        watch(formula, nim, first_to_move=YOU_ARE, second_to_move=I_AM)
    else:
        if n_player==1:
            watch(formula, nim, first_to_move=PLAYER_1_IS, second_to_move=PLAYER_2_IS)
        else:
            watch(formula, nim, first_to_move=PLAYER_2_IS, second_to_move=PLAYER_1_IS)
    if ENV['opponent'] == 'computer':  
        TAc.print(LANG.render_feedback("par-your-turn-play-val", f'# It is your turn to move from conf <game-parenthesis(formula=\'{formula}\') + nim(height={nim})> of the MeasuringGame(Game-parenthesis) game to a new conf of the MeasuringGame(Game-parenthesis) game <game-parenthesis(formula\') + nim(height\')>. You should move either on the game-parenthesis component or on the nim component of the game.'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("par-player-turn-play-val", f'# It is the turn of player {n_player} to move from conf <game-parenthesis(formula=\'{formula}\') + nim(height={nim})> of the MeasuringGame(Game-parenthesis) game to a new conf of the MeasuringGame(Game-parenthesis) game <game-parenthesis(formula\') + nim(height\')>. Player {n_player} should move either on the game-parenthesis component or on the nim component of the game.'), "yellow", ["bold"])
    if formula!=')(':
        if pl.verify_move_game_parenthesis(formula, ")("):
            TAc.print(LANG.render_feedback("par-user-move-play-val-if-can-terminate", f'# Please, insert the formula\' and height\' encoding the new configuration produced by your move just underneath the current configuration. NOTE: As for the formula component, write just the two characters string ")(" if you intend to represent the empty formula.'), "yellow", ["bold"])
        else:
            TAc.print(LANG.render_feedback("par-user-move-play-val", f'# Please, insert the formula\' and height\' encoding the new configuration produced by your move just underneath the current configuration as reported here: '), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("par-user-move-play-val-if-can-terminate", f'# Please, insert the formula\' and height\' encoding the new configuration produced by your move just underneath the current configuration. NOTE: As for the formula component, write just the two characters string ")(" if you intend to represent the empty formula.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-prompt_nim", f'{formula} {nim}'), "yellow", ["bold"])
    new_formula,new_nim = TALinput(str, 2, TAc=TAc)

    if not pl.verify_char(new_formula):
        TAc.print(LANG.render_feedback("par-stranger-char", '# We have a problem. The formula has one or more char that is not a parentheses.'), "red", ["bold"])
        exit(0)
    if not new_nim.isdigit():
        TAc.print(LANG.render_feedback("par-stranger-nim", '# We have a problem. The height of the nim tower inserted is not a number.'), "red", ["bold"])
        exit(0)
    new_nim=int(new_nim)
    if new_formula!=formula and new_nim==nim:
        if formula!=')(':
            if not pl.verify_move_game_parenthesis(formula, new_formula):
                TAc.print(LANG.render_feedback("par-illegal-move", '# We have a problem. Your move is not valid. You must remove ONE well made formula.'), "red", ["bold"])
                if new_formula!=')(':
                    pl.recognize(new_formula, TAc, LANG)
                exit(0)
        else:
            TAc.print(LANG.render_feedback("par-illegal-void-move", '# We have a problem. Your move is not valid. You can\'t move on the void formula.'), "red", ["bold"])
            exit(0)
    elif new_formula!=formula and new_nim!=nim:
        TAc.print(LANG.render_feedback("par-double-move", '# We have a problem. You can\'t move on both game-parenthesis and nim.'), "red", ["bold"])
        exit(0)
    elif new_formula==formula and new_nim==nim:
        TAc.print(LANG.render_feedback("par-dull-nim-move", '# We have a problem. You can\'t pass. You must move at least on ONE of the two games.'), "red", ["bold"])
        exit(0)
    elif new_formula==formula and new_nim>nim:
        TAc.print(LANG.render_feedback("par-grow-nim-move", '# We have a problem. A move can\'t increase the height of the nim tower.'), "red", ["bold"])
        exit(0)
    elif new_formula==formula and new_nim<0:
        TAc.print(LANG.render_feedback("par-negative-nim-move", '# We have a problem. A move can\'t decrease the height of the nim tower under 0.'), "red", ["bold"])
        exit(0)

    if new_formula==')(' and new_nim==0:
        I_have_lost(env_formula, n_player)
    
    if ENV['opponent'] == 'computer':
        watch(new_formula,new_nim, first_to_move=I_AM, second_to_move=YOU_ARE)    
        formula,nim=pl.computer_decision_move(new_formula,new_nim)
        TAc.print(LANG.render_feedback("par-server-move-play-val", f'# My move is from conf <game-parenthesis(\'{new_formula}\') + nim({new_nim})> to conf <game-parenthesis(\'{formula}\') + nim({nim})>.'), "green", ["bold"])
    else:
        n_player=pl.player_flip(n_player)
        formula=new_formula
        nim=new_nim
