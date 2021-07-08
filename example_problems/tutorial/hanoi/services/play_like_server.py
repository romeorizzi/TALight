#!/usr/bin/env python3
from sys import stderr, exit, argv
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem, get_description_of


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="play_like"
args_list = [
    ('role',str),
    ('start', str),
    ('final', str),
    ('n',int),
    ('help', str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")


# INITIALIZATION
N = ENV['n']

# Check arguments errors
if (ENV['start'] != "all_A" and ENV['start'] != "all_B" and ENV['start'] != "all_C"):
    N = len(ENV['start'])
elif (ENV['final'] != "all_A" and ENV['final'] != "all_B" and ENV['final'] != "all_C"):
    N = len(ENV['final'])
elif (N == -1):
    TAc.print(LANG.render_feedback("arg-err", f"N!=-1 if start=all_X and final=all_X"), "red", ["bold"])
    exit(0)

# Get configurations
start = get_input_from(ENV['start'], N)
final = get_input_from(ENV['final'], N)

# Check configs error
if len(start) != len(final):
    TAc.print(LANG.render_feedback("arg-config-err", f"len(start) != len(final)"), "red", ["bold"])
    exit(0)

# Init Hanoi Tower
hanoi = HanoiTowerProblem('toddler')

# Start the game
TAc.print(LANG.render_feedback("start_config", f'# Start config: {start}'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("final_config", f'# Final config: {final}'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("format_moves", f'# Use format: N:FROM->TO (example: 1:A->B)'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("start_game", f'Start the Game'), "yellow", ["bold"])


# PLAY GAME
# define global vars
state = start
turn = 0
player = 0
last_disk = 1

# define global functions
def start_turn():
    global hanoi, turn, player
    TAc.print(LANG.render_feedback("turn", f'\n#-----------\n# turn:   {turn+1}'), "blue", ["bold"])
    TAc.print(LANG.render_feedback("player", f'# player: {hanoi.names[player]}'), "blue", ["reverse"])
    TAc.print(LANG.render_feedback("state", f'# state:  {state}'), "blue", ["reverse"])

def ai_turn(move):
    global hanoi, state, turn, player, last_disk
    disk, c, t, _ = hanoi.parseMove(move)
    TAc.print(LANG.render_feedback("ai_move", f'{hanoi.getStdMove(move)}'), "green", ["bold"])
    last_disk = disk
    state = state[:disk-1] + t + state[disk:]
    turn += 1
    player = (player + 1) % 2

def user_turn(available_moves):
    global hanoi, state, turn, player, last_disk
    if ENV['help'] == 'gimme_moves_available':
        TAc.print(LANG.render_feedback("help", 'This are the moves available:'), "yellow", ["bold"])
        for e in available_moves:
            TAc.print(LANG.render_feedback("help-line", f'{hanoi.getStdMove(e)}'), "yellow", ["reverse"])
    # get user move
    user_move, = TALinput(str, sep="\n", regex="^\d{1,1000}:(A|B|C)(A|B|C)$", regex_explained="N:FT  where N=DISK, F=FROM and T=TO. Use 'end' to quit", exceptions={"end"}, TAc=TAc)
    if user_move == 'end':
        end_game()
    # parse user move
    user_move = hanoi.names[player] + "|" + user_move
    disk, c, t, _ = hanoi.parseMove(user_move)
    # check correctness of move
    code = hanoi.checkMove(state, disk, c, t, player, last_disk)
    if code == 0:
        last_disk = disk
        state = state[:disk-1] + t + state[disk:]
        turn += 1
        player = (player + 1) % 2
    else:
        TAc.print(LANG.render_feedback("invalid_move", f'{get_description_of(code)}\nRetry...'), "red", ["bold"])

def end_game():
    TAc.print(LANG.render_feedback("end-game", '\nEnd Game'), "blue", ["bold"])
    exit(0)

# play the game
opt_moves = hanoi.getMovesList(start, final)
while state != final:
    start_turn()
    available_moves = hanoi.getAvailableMovesIn(state, player, last_disk)
    
    if ENV['role'] == 'daddy' and player == 1:
        # AI play like toddler and is the Toddler turn
        ai_turn(move=random.choice(available_moves)) 
    
    elif ENV['role'] == 'toddler' and player == 0:
        # AI play like Daddy and is the Daddy turn
        ai_turn(move=opt_moves[turn])                

    else:
        # Other case
        user_turn(available_moves)

end_game()
