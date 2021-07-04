#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="check_opt_num_moves"
args_list = [
    ('start', str),
    ('final', str),
    ('n',int),
    ('v',str),
    ('goal',str),
    ('silent',bool),
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# INITIALIZATION
# Check arguments errors
if ENV['version'] == 'classic' and (\
    ENV['start'] != 'all_A' or \
    ENV['start'] != 'all_B' or \
    ENV['start'] != 'all_C' ):
    TAc.print(LANG.render_feedback("arg-classic-start-err", f"classic version wants start=all_A/B/C"), "red", ["bold"])
    exit(0)
if ENV['version'] == 'classic' and (\
    ENV['final'] != 'all_A' or \
    ENV['final'] != 'all_B' or \
    ENV['final'] != 'all_C' ):
    TAc.print(LANG.render_feedback("arg-classic-final-err", f"classic version wants final=all_A/B/C"), "red", ["bold"])
    exit(0)

# Get Start config
start = get_input_from(ENV['start'], ENV['n'])
if start == "err":
    TAc.print(LANG.render_feedback("arg-all-err", f"Wrong n for start_config"), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("print_start", f'# Start config: {start}'), "yellow", ["bold"])

# Get Final config
final = get_input_from(ENV['final'], ENV['n'])
if final == "err":
    TAc.print(LANG.render_feedback("arg-all-err", f"Wrong n for final_config"), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("print_start", f'# Final config: {final}'), "yellow", ["bold"])

# Check configs error
if len(start) != len(final):
    TAc.print(LANG.render_feedback("arg-config-err", f"len(start) != len(final)"), "red", ["bold"])
    exit(0)

# Init Hanoi Tower
hanoi = HanoiTowerProblem(ENV['v'])

# Start the game
TAc.print(LANG.render_feedback("format_moves", f'# Use format: N:FROM->TO and print "#end" as last move. (example: 1:A->B)'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("start_game", f'Start the Game'), "yellow", ["bold"])

# Get user moves
user_moves = list()
while True:
    move, = TALinput(str, sep="\n", regex="^\d{1,1000}: (A|B|C)->(A|B|C)$", regex_explained="N: FROM->TO", exceptions={"end"}, TAc=TAc)
    if move == 'end':
        break
    user_moves.append(move)

# Get correct moves
corr_moves = hanoi.move_tower(start, final)
if (len(user_moves) < len(corr_moves)):
    TAc.print(LANG.render_feedback("sol-wrong-less", f'The solution is wrong. len(user_moves) < len(corr_moves)'), "red", ["bold"])
    exit(0)


# Process data
if ENV['goal'] == 'optimal':
    # check equality
    diff = None
    for i in range(len(corr_moves)):
        if user_moves[i] != corr_moves[i]:
            diff = [i+1, user_moves[i], corr_moves[i]]
            break
    
    if diff == None:
        if ENV['silent'] == 0:
            TAc.print(LANG.render_feedback("sol-opt", f'The solution is optimal'), "green", ["bold"])

    else:
        TAc.print(LANG.render_feedback("sol-not-opt", f'The solution is not optimal'), "red", ["bold"])

        # provide feedback
        if ENV['feedback'] == 'spot_first_non_optimal_move':
            TAc.print(LANG.render_feedback("gimme-diff", f'diff: {diff}'), "red", ["bold"])

        elif ENV['feedback'] == 'gimme_optimal_solution':
            TAc.print(LANG.render_feedback("gimme-optimal", f'corr-sol: {corr_moves}'), "red", ["bold"])

        elif ENV['feedback'] == 'gimme_shorter_solution':
            TAc.print(LANG.render_feedback("gimme-admissible", f'adm-sol: {hanoi.get_not_opt_sol(start, final)}'), "red", ["bold"])


elif ENV['goal'] == 'any':
    # check admissibility
    move_not_valid = None
    state = list(start)
    for e in user_moves:
        disk, tmp = e.split(": ")
        disk = int(disk)
        c, t = tmp.split("->")
        if not hanoi.is_valid(state, disk, c, t):
            move_not_valid = e
            break
        state[disk-1] = t
    
    if move_not_valid != None:
        TAc.print(LANG.render_feedback("sol-not-valid", f'Invalid move: {move_not_valid}'), "red", ["bold"])
    else:
        if final == ''.join(state):
            if ENV['silent'] == 0:
                TAc.print(LANG.render_feedback("sol-admissible", f'The solution is admissible'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("sol-wrong-final", f'Wrong final state'), "red", ["bold"])

    # provide feedback
    if ENV['feedback'] == 'spot_first_non_optimal_move':
        diff = None
        for i in range(len(corr_moves)):
            if user_moves[i] != corr_moves[i]:
                diff = [i+1, user_moves[i], corr_moves[i]]
                break
        
        if diff == None:
            if ENV['silent'] == 0:
                TAc.print(LANG.render_feedback("sol-opt", f'The solution is optimal'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("gimme-diff", f'diff: {diff}'), "red", ["bold"])

    elif ENV['feedback'] == 'gimme_optimal_solution':
        TAc.print(LANG.render_feedback("gimme-optimal", f'corr-sol: {corr_moves}'), "red", ["bold"])

    elif ENV['feedback'] == 'gimme_shorter_solution':
        TAc.print(LANG.render_feedback("gimme-admissible", f'adm-sol: {hanoi.get_not_opt_sol(start, final)}'), "red", ["bold"])


exit(0)