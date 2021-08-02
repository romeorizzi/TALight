#!/usr/bin/env python3
from sys import stderr, exit, argv
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator, HanoiTowerProblem, HanoiState
from error_code import print_move_error


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="play_like"
args_list = [
    ('role',str),
    ('start', str),
    ('final', str),
    ('n',int),
    ('format',str),
    ('help', str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
# LANG.manage_opening_msg()



# START CODING YOUR SERVICE: 
# Get configurations
gen = ConfigGenerator()
start, final, error = gen.getConfigs(ENV['start'], ENV['final'], ENV['n'])

# Check errors
if error == 'n_not_valid':
    TAc.print(LANG.render_feedback("n_not_valid", f"If you use the all_* form for start and final, you must use a N >= 0."), "red", ["bold"])
    exit(0)
elif error == 'different_len':
    TAc.print(LANG.render_feedback("different_len", f'If you use a custom configuration for start and final, the length of start must be equal to the length of final'), "red", ["bold"])
    exit(0)


# Get format
if format == 'extended':
    regex="^move \d{1,1000} from [A-Z] peg to [A-Z] peg$"
    regex_explained="move D from C peg to T peg (where N=DISK, F=FROM and T=TO)"
    def print_move(d, c, t):
        TAc.print(LANG.render_feedback("ai_move", f'move {d} from {c} peg to {t} peg.'), "green", ["bold"])
else:
    regex="^\d{1,1000}:[A-Z][A-Z]$"
    regex_explained="D:CT (where N=DISK, F=FROM and T=TO)"
    def print_move(d, c, t):
        TAc.print(LANG.render_feedback("ai_move", f'{d}:{c}{t}'), "green", ["bold"])


# Init Hanoi Tower
hanoi = HanoiTowerProblem('toddler')

# Start the game
TAc.print(LANG.render_feedback("start_config", f'# Start config: {start}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("final_config", f'# Final config: {final}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("start_game", f'Start!'), "yellow", ["bold"])


# play the game
names = ['Daddy', 'Toddler']
opt_moves = hanoi.getMovesList(start, final)
state = HanoiState(start)

while not state.isEqualTo(final):
    # Initialize turn
    TAc.print(LANG.render_feedback("turn", f'\n#-----------\n# turn:   {state.turn}'), "blue", ["bold"])
    TAc.print(LANG.render_feedback("player", f'# player: {names[state.turn % 2]}'), "blue", ["reverse"])
    TAc.print(LANG.render_feedback("state", f'# state:  {state.getString()}'), "blue", ["reverse"])

    # Get availables moves
    available_moves = hanoi.getAvailableMovesIn(state)

    # This is the Daddy turn and AI play like Daddy:
    if (state.turn % 2 == 0) and ENV['role'] == 'toddler':
        d, c, t = hanoi.parseMove(opt_moves[state.turn])
        print_move(d, c, t)
        state.update(d, t)
    
    # This is the Toddler turn and AI play like Toddler
    elif (state.turn % 2 == 1) and ENV['role'] == 'daddy':
        d, c, t = hanoi.parseMove(random.choice(available_moves))
        print_move(d, c, t)
        state.update(d, t)

    # Other cases
    else:
        # help
        if ENV['help'] == 'gimme_moves_available':
            TAc.print(LANG.render_feedback("help", 'These are the moves available:'), "yellow", ["bold"])
            for e in available_moves:
                print_move(*hanoi.parseMove(e))
        # get user move
        user_move, = TALinput(str, sep="\n", regex=regex, regex_explained=regex_explained, exceptions={"end"}, TAc=TAc)
        if user_move == 'end':
            break
        # parse user move
        d, c, t = hanoi.parseMove(user_move)
        # check correctness of move
        success, code = hanoi.checkMove(state, d, c, t)
        if success:
            state.update(d, t)
        else:
            TAc.print(LANG.render_feedback("move-wrong", f'Error in current move.'), "red", ["bold"])
            print_move_error(code, TAc, LANG)

TAc.print(LANG.render_feedback("end_game", '\nFinish!'), "yellow", ["bold"])
exit(0)
