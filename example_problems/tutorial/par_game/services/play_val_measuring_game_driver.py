#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import par_game_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="par_game"
service="play_val_measuring_game"

args_list = [
    ('formula',str),
    ('nim',int),
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

nim=ENV['nim']

if not pl.recognize(formula, TAc, LANG):
    exit(0)

env_formula=formula
if formula=='':
    formula=')('


def I_have_lost(env_formula):
    TAc.print(LANG.render_feedback("par-TALight_lost", f'# It is my turn to move, on conf <par_game(\'\') + nim(0)> of the MeasuringGame(Par_game) game, that is, a void formula (plus an empty Nim tower). Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-you-won", f'# You won!'), "green", ["bold"])
    if ENV["TALight_first_to_move"] == 0:
        TAc.print(LANG.render_feedback("par-wrong-grundy-val", f'# Since we played optimally, you have successfully proven that the Grundy value of the Par_game game configuration par_game(\'{env_formula}\') is NOT the number {ENV["nim"]}.'), "green", ["bold"])        
    else:
        TAc.print(LANG.render_feedback("par-correct-grundy-val", f'# Since we played optimally, you have successfully proven that the Grundy value of the Par_game game configuration par_game(\'{env_formula}\') is precisely {ENV["nim"]}.'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost(env_formula):
    TAc.print(LANG.render_feedback("par-you-have-lost", f'# It is your turn to move, on conf <par_game(\'\') + nim(0)> of the MeasuringGame(Par_game) game, that is, a void formula (plus an empty Nim tower). Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("par-you-lost", f'# You lost!'), "green", ["bold"])
    if ENV["TALight_first_to_move"] == 0:
        TAc.print(LANG.render_feedback("par-correct-grundy-val-or-bad-move", f'# The cases are two: either during this play you trew away a win with a bad move, or we have convinced you that the Grundy value of the Par_game game configuration par_game(\'{env_formula}\') is precisely {ENV["nim"]}.'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("par-wrong-grundy-val-or-bad-move", f'# The cases are two: either during this play you trew away a win with a bad move, or we have convinced you that the Grundy value of the Par_game game configuration par_game(\'{env_formula}\') is NOT the number {ENV["nim"]}.'), "green", ["bold"])        
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
def watch(formula,nim, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS] 
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS]
    if ENV["watch"] == 'no_watch':
        return
    TAc.print('# watch={ENV["watch"]}: ', "blue", end='')
    if ENV["watch"] == 'watch_winner':
        if formula == '' or formula == ')(':
            formula_grundy_value = 0
        else:
            formula_grundy_value = pl.grundy_val(formula)
        if(pl.grundy_sum(formula_grundy_value, nim) == 0):
            TAc.print(LANG.render_feedback("par-watch-winner-who-moves-loses", f'{second_to_move} ahead, since <par_game(\'{formula}\') + nim({nim})> is a who-moves-loses configuration.'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-watch-winner-who-moves-wins", f'{first_to_move} ahead, since <par_game(\'{formula}\') + nim({nim})> is a who-moves-wins configuration.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        if formula != '' and formula != ')(':
            win_moves = pl.find_moves_par_game(formula, False, nim)
        else:
            win_moves = []
        count_win_moves=pl.count_winning_moves_nim(formula, nim)
        if (len(win_moves)+count_win_moves)>0:
            TAc.print(LANG.render_feedback("par-num-winning-moves-n", f'the current configuration <par_game(\'{formula}\') + nim({nim})> admits {len(win_moves)+count_win_moves} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-num-winning-moves-0", f'the current configuration <par_game(\'{formula}\') + nim({nim})> admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        if formula != '' and formula != ')(':
            win_moves = pl.find_moves_par_game(formula, True, nim)
        else:
            win_moves = []
        win_moves_with_nim={(None,None)}
        for wff in win_moves:
            wff=(wff,nim)
            win_moves_with_nim.add(wff)
        win_moves_with_nim.discard((None,None))
        win_moves_with_nim.update(pl.winning_moves_nim(formula, nim))
        if len(win_moves_with_nim) > 1:
            TAc.print(LANG.render_feedback("par-list-multiple-winning-moves", f'for the current configuration <par_game(\'{formula}\') + nim({nim})> the winning moves are {win_moves_with_nim}'), "blue")
        elif len(win_moves_with_nim) == 1:
            TAc.print(LANG.render_feedback("par-list-one-winning-move", f'for the current configuration <par_game(\'{formula}\') + nim({nim})> the winning move is {win_moves_with_nim}'), "blue")
        else:
            TAc.print(LANG.render_feedback("par-list-none-winning-moves", f'the current configuration <par_game(\'{formula}\') + nim({nim})> admits no winning move'), "blue")
    elif ENV['watch'] == 'watch_grundy_val':
        if formula == '' or formula == ')(':
            formula_grundy_value = 0
        else:
            formula_grundy_value = pl.grundy_val(formula)
        TAc.print(LANG.render_feedback("par-watch-grundy-val", f'the current configuration <par_game(\'{formula}\') + nim({nim})> has grundy value {pl.grundy_sum(formula_grundy_value, nim)}'), "blue")


        
if ENV["TALight_first_to_move"] == 1: # if the user plays the match as second to move
    if (formula=='' or formula==')(') and nim==0: # no valid moves on the configuration '' 0. TALight first to move loses the match
        I_have_lost(env_formula)
    
    watch(formula, nim, first_to_move='I am', second_to_move='you are')
    
    new_formula,new_nim=pl.computer_decision_move(formula,nim)
    TAc.print(LANG.render_feedback("par-server-move-play-val", f'# My move is from conf <par_game(\'{formula}\') + nim({nim})> to conf <par_game(\'{new_formula}\') + nim({new_nim})>.'), "green", ["bold"])
    formula,nim=new_formula,new_nim

while True:
    if (formula==')(' or formula=='') and nim==0:
        you_have_lost(env_formula)    
    watch(formula, nim, first_to_move=YOU_ARE, second_to_move=I_AM)    
    TAc.print(LANG.render_feedback("par-your-turn-play-val", f'# It is your turn to move from conf <par_game(formula=\'{formula}\') + nim(height={nim})> of the MeasuringGame(Par_game) game to a new conf of the MeasuringGame(Par_game) game <par_game(formula\') + nim(height\')>. You should move either on the par_game component or on the nim component of the game.'), "yellow", ["bold"])
    if formula!=')(':
        if pl.verify_move_par_game(formula, ")("):
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
            if not pl.verify_move_par_game(formula, new_formula):
                TAc.print(LANG.render_feedback("par-illegal-move", '# We have a problem. Your move is not valid. You must remove ONE well made formula.'), "red", ["bold"])
                if new_formula!=')(':
                    pl.recognize(new_formula, TAc, LANG)
                exit(0)
        else:
            TAc.print(LANG.render_feedback("par-illegal-void-move", '# We have a problem. Your move is not valid. You can\'t move on the void formula.'), "red", ["bold"])
            exit(0)
    elif new_formula!=formula and new_nim!=nim:
        TAc.print(LANG.render_feedback("par-double-move", '# We have a problem. You can\'t move on both par_game and nim.'), "red", ["bold"])
        exit(0)
    elif new_formula==formula and new_nim==nim:
        TAc.print(LANG.render_feedback("par-dull-move", '# We have a problem. You can\'t pass. You must move at least on ONE of the two games.'), "red", ["bold"])
        exit(0)
    elif new_formula==formula and new_nim>nim:
        TAc.print(LANG.render_feedback("par-grow-nim-move", '# We have a problem. A move can\'t increase the height of the nim tower.'), "red", ["bold"])
        exit(0)
    elif new_formula==formula and new_nim<0:
        TAc.print(LANG.render_feedback("par-negative-nim-move", '# We have a problem. A move can\'t decrease the height of the nim tower under 0.'), "red", ["bold"])
        exit(0)

    if new_formula==')(' and new_nim==0:
        I_have_lost(env_formula)
    
    watch(new_formula,new_nim, first_to_move=I_AM, second_to_move=YOU_ARE)    
    formula,nim=pl.computer_decision_move(new_formula,new_nim)
    TAc.print(LANG.render_feedback("par-server-move-play-val", f'# My move is from conf <par_game(\'{new_formula}\') + nim({new_nim})> to conf <par_game(\'{formula}\') + nim({nim})>.'), "green", ["bold"])
