#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator, HanoiTowerProblem, parse_move
from utils_lang import print_move_error, get_regex, get_std_move, get_formatted_move


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="check_one_sol"
args_list = [
    ('v',str),
    ('start',str),
    ('final',str),
    ('n',int),
    ('format',str),
    ('goal',str),
    ('ignore_peg_from',bool),
    ('ignore_peg_to',bool),
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))



# START CODING YOUR SERVICE: 
def provide_feedback_and_exit(info):
    if ENV['feedback'] == 'spot_first_non_optimal_move':
        # Check diff
        diff = [None, None]
        for i in range(len(opt_sol)):
            if user_sol[i] != opt_sol[i]:
                diff = [i+1, user_sol[i], opt_sol[i]]
        TAc.print(LANG.render_feedback("spot-first-diff", f'Line {diff[0]}:\nYour wrong move: {diff[1]}.\nCorrect move: {diff[2]}'), "yellow", ["bold"])

    elif ENV['feedback'] == 'gimme_optimal_solution':
        TAc.print(LANG.render_feedback("gimme-optimal", f'This is the optimal moves list.'), "yellow", ["reverse"])
        for e in opt_sol:
            disk, current, target = parse_move(e)
            TAc.print(LANG.render_feedback("gimme-optimal-line", f'Move disk {disk} from {current} peg to {target} peg.'), "yellow", ["reverse"])

    elif ENV['feedback'] == 'gimme_shorter_solution' and info != 'wrong':
        TAc.print(LANG.render_feedback("gimme-admissible", f'This is a shorter admissible moves list:'), "yellow", ["reverse"])
        for e in hanoi.getNotOptimalMovesList(start, final, desired_size=len(user_sol)-1):
            disk, current, target = parse_move(e)
            TAc.print(LANG.render_feedback("gimme-admissible-line", f'Move disk {disk} from {current} peg to {target} peg.'), "yellow", ["reverse"])
    exit(0)


# Get configurations
gen = ConfigGenerator()
start, final, error = gen.getConfigs(ENV['start'], ENV['final'], ENV['n'])

# Check errors
if error == 'n_not_valid':
    TAc.print(LANG.render_feedback("n_not_valid", f'If you use the all_* form for the arguments \'start\' and \'final\', then you must use a value other than -1 for the argument \'n\'.'), "red", ["bold"])
    exit(0)
elif error == 'different_len':
    TAc.print(LANG.render_feedback("different_len", f'If you use a custom configuration for start and final, the length of start must be equal to the length of final'), "red", ["bold"])
    exit(0)


# Init Hanoi Tower
hanoi = HanoiTowerProblem(ENV['v'])

# Start the game
TAc.print(LANG.render_feedback("start_config", f'# Start config: {start}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("final_config", f'# Final config: {final}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("start_game", f'Start!'), "yellow", ["reverse"])

# Get user moves
user_sol = list()
regex, explain = get_regex(ENV['format'], ENV['lang'])
while True:
    user_move, = TALinput(str, sep="\n", regex=regex, regex_explained=explain, exceptions={"end"}, TAc=TAc)
    if user_move == 'end':
        break
    user_sol.append(get_std_move(user_move, ENV['format'], ENV['lang']))

# Get optimal moves
opt_sol = hanoi.getMovesList(start, final)


# PROCESS DATA
# Check optimality
if ENV['goal'] == 'optimal':
    # check if the user solution is surely wrong
    if len(user_sol) != len(opt_sol):
        TAc.print(LANG.render_feedback("sol-len-wrong-equal", f'Your number of moves is different from the optimal number of moves. Use check_opt_num_moves service for check it.'), "red", ["bold"])
        provide_feedback_and_exit('not_optimal')

    # check if the user solution is optimal
    if ENV['ignore_peg_from'] == 0 and ENV['ignore_peg_to'] == 0:
        # check both pegs
        if (user_sol != opt_sol):
            TAc.print(LANG.render_feedback("sol-wrong-opt", f'Your solution is not optimal.'), "red", ["bold"])
            provide_feedback_and_exit('not_optimal')
        else:
            TAc.print(LANG.render_feedback("sol-correct-opt", f'Your solution is optimal.'), "green", ["bold"])
            exit(0)
    else:
        # ignore the specificated pegs
        must_exit = False
        for i in range(len(opt_sol)):
            disk_user, from_user, to_user = parse_move(user_sol[i])
            disk_opt, from_opt, to_opt = parse_move(opt_sol[i])
            # check disk
            if disk_user != disk_opt:
                TAc.print(LANG.render_feedback("sol-wrong-disk", f'You moved some wrong disk.'), "red", ["bold"])
                must_exit = True
            # check peg from
            if ENV['ignore_peg_from'] and from_user != from_opt:
                TAc.print(LANG.render_feedback("sol-wrong-peg-from", f'You moved some disk from wrong peg.'), "red", ["bold"])
                must_exit = True
            # check peg to
            if ENV['ignore_peg_to'] and to_user != to_opt:
                TAc.print(LANG.render_feedback("sol-wrong-peg-to", f'You moved some disk to wrong peg.'), "red", ["bold"])
                must_exit = True
            # exit?
            if must_exit:
                provide_feedback_and_exit('not_optimal')

# check if the user solution is surely not admissible
if (len(user_sol) < len(opt_sol)):
    TAc.print(LANG.render_feedback("sol-wrong-less", f'Your number of moves is less than the optimal number of moves. Use check_opt_num_moves service for check it.'), "red", ["bold"])
    provide_feedback_and_exit('wrong')

# Check admissibility
res, info = hanoi.checkMoveList(user_sol, start, final)
if (res == 'move_wrong'):
    TAc.print(LANG.render_feedback("move-wrong", f'Error in move {info[0]}.'), "red", ["bold"])
    print_move_error(info[1], TAc, LANG)
    provide_feedback_and_exit('wrong')
elif (res == 'final_wrong'):
    TAc.print(LANG.render_feedback("final-wrong", f'Your solution finish in configuration: {info}.\nIt is different from the correct final configuration: {final}.'), "red", ["bold"])
    provide_feedback_and_exit('wrong')
   
if ENV['goal'] == 'admissible':
    TAc.print(LANG.render_feedback("sol-admissible", f'Your solution is admissible.'), "green", ["bold"])
    # check if also optimal
    if len(user_sol) == len(opt_sol):
        TAc.print(LANG.render_feedback("sol-correct-opt", f'Your solution is optimal.'), "green", ["bold"])
        exit(0)
    else:
        provide_feedback_and_exit('admissible')

if ENV['goal'] == 'simple_walk':
    # check if is a simple walk
    if (info != None):
        TAc.print(LANG.render_feedback("sol-not-simplewalk", f'Your solution is not a simple walk.\nThis states are repeated:'), "red", ["bold"])
        for k,v in info.items():
            TAc.print(LANG.render_feedback("occ-line", f'State {k} repeated {v} times.'), "red", ["reverse"])
    else:
        TAc.print(LANG.render_feedback("sol-simplewalk", f'Your solution is a simple walk.'), "green", ["bold"])
        # check if also optimal
        if len(user_sol) == len(opt_sol):
            TAc.print(LANG.render_feedback("sol-correct-opt", f'Your solution is optimal.'), "green", ["reverse"])
            exit(0)
