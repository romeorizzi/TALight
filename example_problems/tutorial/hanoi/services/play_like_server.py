#!/usr/bin/env python3
from sys import stderr, exit, argv
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="play_like"
args_list = [
    ('ai_role',str),
    ('start', str),
    ('final', str),
    ('n',int),
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
hanoi = HanoiTowerProblem('classic')

# Start the game
TAc.print(LANG.render_feedback("start_config", f'# Start config: {start}'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("final_config", f'# Final config: {final}'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("format_moves", f'# Use format: N:FROM->TO (example: 1:A->B)'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("start_game", f'Start the Game'), "yellow", ["bold"])

names = ['Daddy', 'Toddler']


def startTurn(turn, player):
    TAc.print(LANG.render_feedback("turn", f'\n#-----------\n# turn:   {turn}'), "blue", ["bold"])
    TAc.print(LANG.render_feedback("player", f'# player: {names[player]}'), "blue", ["reverse"])
    TAc.print(LANG.render_feedback("state", f'# state:  {state}'), "blue", ["reverse"])


# PLAY GAME
if ENV['ai_role'] == 'daddy':
    opt_moves = hanoi.getMovesList(start, final)
    state = start
    turn = 1
    n_move = 0
    player = 0


    while state != final:
        if player == 0: # Dadday
            startTurn(turn, player)
            disk, c, t = hanoi.parseMove(opt_moves[n_move])
            TAc.print(LANG.render_feedback("ai_move", f'{opt_moves[n_move]}'), "green", ["bold"])
            state = state[:disk-1] + t + state[disk:]
            turn += 1
            n_move += 1
            player = (player + 1) % 2

        else: # Toddler
            startTurn(turn, player)

            # get user move
            user_move, = TALinput(str, sep="\n", regex="^\d{1,1000}: (A|B|C)->(A|B|C)$", regex_explained="N: FROM->TO", exceptions={'end'}, TAc=TAc)
            if user_move == 'end':
                break

            # parse user move
            disk, c, t = hanoi.parseMove(user_move)

            # check validity move
            if hanoi.isValid(state, disk, c, t):
                state = state[:disk-1] + t + state[disk:]
                n_move += 1
            else:
                TAc.print(LANG.render_feedback("invalid_move", 'invalid move'), "red", ["bold"])

            turn += 1
            player = (player + 1) % 2



exit(0)
