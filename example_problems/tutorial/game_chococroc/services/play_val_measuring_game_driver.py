#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import random
import chococroc_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="chococroc"
service="play_val_measuring_game"

args_list = [
    ('m',int),
    ('n',int),
    ('nim',int),
    ('TALight_first_to_move',int),
    ('watch',str),
    ('seed', int),
    ('opponent', str)
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
    m = int(round((random.random())*100,0))
    n = int(round((random.random())*100,0))
else:
    m=ENV['m']
    n=ENV['n']
env_m = m
env_n = n
nim=ENV['nim']

def I_have_lost():
    if ENV['opponent'] == 'computer':
        TAc.print(LANG.render_feedback("TALight_lost", f'# It is my turn to move, on conf <chococroc(1,1) + nim(0)> of the MeasuringGame(Chococroc) game, that is, one single square chocolate bar (plus an empty Nim tower). Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("you-won", f'# You won!'), "green", ["bold"])
        if ENV["TALight_first_to_move"] == 0:
            TAc.print(LANG.render_feedback("wrong-grundy-val", f'# Since we played optimally, you have successfully proven that the Grundy value of the Chococroc game configuration chococroc({env_m},{env_n}) is NOT the number {ENV["nim"]}.'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("correct-grundy-val", f'# Since we played optimally, you have successfully proven that the Grundy value of the Chococroc game configuration chococroc({env_m},{env_n}) is precisely {ENV["nim"]}.'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("choco-player-lost-msg-nim", f'# It is the turn of player {cl.player_flip(n_player)} to move, on conf <chococroc(1,1) + nim(0)> of the MeasuringGame(Chococroc) game, that is one single square chocolate bar (plus an empty Nim tower). Since this configuration admits no valid move, then player {cl.player_flip(n_player)} has lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("choco-player-won-nim", f'# Player {n_player} won!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost():
    TAc.print(LANG.render_feedback("you-have-lost", f'# It is your turn to move, on conf <chococroc(1,1) + nim(0)> of the MeasuringGame(Chococroc) game, that is, one single square chocolate bar (plus an empty Nim tower). Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("you-lost", f'# You lost!'), "green", ["bold"])
    if ENV["TALight_first_to_move"] == 0:
        TAc.print(LANG.render_feedback("correct-grundy-val-or-bad-move", f'# The cases are two: either during this play you trew away a win with a bad move, or we have convinced you that the Grundy value of the Chococroc game configuration chococroc({env_m},{env_n}) is precisely {ENV["nim"]}.'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("wrong-grundy-val-or-bad-move", f'# The cases are two: either during this play you trew away a win with a bad move, or we have convinced you that the Grundy value of the Chococroc game configuration chococroc({env_m},{env_n}) is NOT the number {ENV["nim"]}.'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
PLAYER_1_IS = LANG.render_feedback("Player-1-is", 'Player 1 is')
PLAYER_2_IS = LANG.render_feedback("Player-2-is", 'Player 2 is')
def watch(m,n,nim, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS, PLAYER_1_IS, PLAYER_2_IS]
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS, PLAYER_1_IS, PLAYER_2_IS]
    if ENV["watch"] == 'none':
        return
    TAc.print(f'# watch={ENV["watch"]}: ', "blue", end='')
    if ENV["watch"] == 'winner':
        if(cl.grundy_sum(cl.grundy_val(m, n), nim) == 0):
            TAc.print(LANG.render_feedback("watch-winner-who-moves-loses", f'{second_to_move} ahead, since <chococroc({m},{n}) + nim({nim})> is a who-moves-loses configuration.'), "blue")
        else:
            TAc.print(LANG.render_feedback("watch-winner-who-moves-wins", f'{first_to_move} ahead, since <chococroc({m},{n}) + nim({nim})> is a who-moves-wins configuration.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        win_moves = cl.winning_moves(m, n, nim)
        win_moves.discard((None, None))
        count_win_moves=cl.count_winning_moves_nim(m, n, nim)
        if (len(win_moves)+count_win_moves)>0:
            TAc.print(LANG.render_feedback("num-winning-moves-n", f'the current configuration <chococroc({m},{n}) + nim({nim})> admits {len(win_moves)+count_win_moves} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("num-winning-moves-0", f'# the current configuration <chococroc({m},{n}) + nim({nim})> admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        win_moves = cl.winning_moves(m, n, nim)
        win_moves.discard((None, None))
        win_moves_with_nim={(None,None,None)}
        for tuple in win_moves:
            tuple+=(nim,)
            win_moves_with_nim.add(tuple)
        win_moves_with_nim.discard((None,None,None))
        win_moves_with_nim.update(cl.winning_moves_nim(m, n, nim))
        if len(win_moves_with_nim) > 1:
            TAc.print(LANG.render_feedback("list-multiple-winning-moves", f'# for the current configuration <chococroc({m},{n}) + nim({nim})> the winning moves are {win_moves_with_nim}'), "blue")
        elif len(win_moves_with_nim) == 1:
            TAc.print(LANG.render_feedback("list-one-winning-move", f'# for the current configuration <chococroc({m},{n}) + nim({nim})> the winning move is {win_moves_with_nim}'), "blue")
        else:
            TAc.print(LANG.render_feedback("list-none-winning-moves", f'# the current configuration <chococroc({m},{n}) + nim({nim})> admits no winning move'), "blue")
    elif ENV['watch'] == 'grundy_val':
        TAc.print(LANG.render_feedback("watch-grundy-val", f'# the current configuration <chococroc({m},{n}) + nim({nim})> has grundy value {cl.grundy_sum(cl.grundy_val(m, n), nim)}'), "blue")


        
if ENV["TALight_first_to_move"] == 1 and ENV['opponent'] == 'computer': # if the user plays the match as second to move
    if m==1 and n==1 and nim==0: # no valid moves on the configuration (1,1,0). TALight first to move loses the match
        I_have_lost()
        
    watch(m,n,nim, first_to_move='I am', second_to_move='you are')
    
    new_m,new_n,new_nim=cl.computer_decision_move(m,n,nim)
    TAc.print(LANG.render_feedback("server-move-play-val", f'# My move is from conf <chococroc({m},{n}) + nim({nim})> to conf <chococroc({new_m},{new_n}) + nim({new_nim})>.'), "green", ["bold"])
    m,n,nim=new_m,new_n,new_nim
    
n_player=1

while True:
    if m==1 and n==1 and nim==0:
        you_have_lost()
    if ENV['opponent'] == 'computer':
        watch(m,n,nim, first_to_move=YOU_ARE, second_to_move=I_AM)
    else:
        if n_player ==1:
            watch(m, n, nim, first_to_move=PLAYER_1_IS, second_to_move=PLAYER_2_IS)
        else:
            watch(m, n, nim, first_to_move=PLAYER_2_IS, second_to_move=PLAYER_1_IS)
    if ENV['opponent'] == 'computer':
        TAc.print(LANG.render_feedback("your-turn-play-val", f'# It is your turn to move from conf <chococroc(m={m},n={n}) + nim(height={nim})> of the MeasuringGame(Chococroc) game to a new conf of the MeasuringGame(Chococroc) game <chococroc(m\',n\') + nim(height\')>. You should move either on the chococroc component or on the nim component of the game.'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("choco-player-turn-play-val", f'# It is the turn of player {n_player} to move from conf <chococroc({m},{n}) + nim({nim})> of the MeasuringGame(Chococroc) game to a new conf of the MeasuringGame(Chococroc) game <chococroc(m\',n\') + nim(height\')>. Player {n_player} should move either on the chococroc component or on the nim component of the game.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("user-move-play-val", f'# Please, insert the three integers m\', n\' and height\' encoding the new configuration produced by your move just underneath the current position we put you into: '), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("prompt_nim", f'{m} {n} {nim}'), "yellow", ["bold"])
    new_m,new_n,new_nim = TALinput(int, 3, TAc=TAc)
    if new_m != m and new_n != n:
        TAc.print(LANG.render_feedback("not-valid", f'# No! Your move from conf <chococroc({m},{n}) + nim({nim})> to conf <chococroc({new_m},{new_n}) + ({new_nim})> is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("double-move", f'# You are cheating. A move can not alter both the number of rows (from {m} to {new_m}) and the number of columns (from {n} to {new_n})).'), "red", ["bold"])
        exit(0)
    if new_m == m and new_n == n and new_nim == nim:
        TAc.print(LANG.render_feedback("not-valid", f'# No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("not-valid-nim", f'# No! Your move from height {nim} to new height {new_nim} is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("dull-nim-move", f'# You are cheating. Your move must either reduce the number of rows or the number of columns or the height of the nim tower. Otherwise, you have not really moved but simply passed.'), "red", ["bold"])
        exit(0)
    if new_m == m and new_n == n and new_nim > nim:
        TAc.print(LANG.render_feedback("not-valid-nim", f'# No! Your move from height {nim} to new height {new_nim} is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("wrong-grow-move", f'# You are cheating. A move can not increase the height of the nim tower.'), "red", ["bold"])        
        exit(0)
    if new_m == m and new_n == n and new_nim < 0:
        TAc.print(LANG.render_feedback("not-valid-nim", f'# No! Your move from height {nim} to new height {new_nim} is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("negative-move", f'# You are cheating. A move can not decrease the height of the nim tower under 0.'), "red", ["bold"])
        exit(0)
    if new_m != m:
        pos = m
        new_pos = new_m
    else:
        pos = n
        new_pos = new_n
    if new_pos > pos:
        TAc.print(LANG.render_feedback("not-valid", f'# No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("increasing-move", f'# With a move the value of a coordinate can not increase from {pos} to {new_pos}. On the contrary, precisely one coordinate must be decreased.'), "red", ["bold"])
        exit(0)
    if new_pos < pos - (pos//2):
        TAc.print(LANG.render_feedback("not-valid", f'# No! Your move from conf ({m},{n}) to conf ({new_m},{new_n}) is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("excessive-move", f'# No! No valid move can more than halve the value of a coordinate. (Here, 2*{new_pos}={2*new_pos} < {pos}).'), "red", ["bold"])
        exit(0)
    if (new_m!=m or new_n!=n) and new_nim!=nim:
        TAc.print(LANG.render_feedback("not-valid-nim", f'# No! Your move from height {nim} to new height {new_nim} is not valid.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("wrong-nim-move", f'# You are cheating. You can not modify the height of the nim tower if you move on the chococroc game.'), "red", ["bold"])
        exit(0)
    if new_m==1 and new_n==1 and new_nim==0:
        I_have_lost()
        
    if ENV['opponent'] == 'computer':
        watch(new_m,new_n,new_nim, first_to_move=I_AM, second_to_move=YOU_ARE)
        m,n,nim=cl.computer_decision_move(new_m,new_n,new_nim)
        TAc.print(LANG.render_feedback("server-move-play-val", f'# My move is from conf <chococroc({new_m},{new_n}) + nim({new_nim})> to conf <chococroc({m},{n}) + nim({nim})>.'), "green", ["bold"])
    else:
        n_player = cl.player_flip(n_player)
        m,n=new_m, new_n
        nim = new_nim











