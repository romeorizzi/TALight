#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import get_input_from, HanoiTowerProblem


# FUNCTIONS
def provide_feedback_and_exit(user_sol, opt_sol, user_sol_is_wrong=False):
    if ENV['feedback'] == 'spot_first_non_optimal_move':
        # Check diff
        diff = None
        if len(opt_sol) == 0:
            diff = [0, user_sol[0], None]
        else:
            for i in range(len(opt_sol)):
                if user_sol[i] != opt_sol[i]:
                    diff = [i+1, user_sol[i], opt_sol[i]]
                    break
        assert diff != None
        TAc.print(LANG.render_feedback("spot-first-diff", f'diff: {diff}'), "yellow", ["bold"])

    elif ENV['feedback'] == 'gimme_optimal_solution':
        TAc.print(LANG.render_feedback("gimme-optimal", f'opt-sol: {opt_sol}'), "yellow", ["bold"])

    elif ENV['feedback'] == 'gimme_shorter_solution' and not user_sol_is_wrong:
            TAc.print(LANG.render_feedback("gimme-admissible", f'adm-sol: {hanoi.getNotOptimalSol(start, final, desired_size=len(user_sol)-1)}'), "yellow", ["bold"])
    exit(0)


# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="check_one_sol"
args_list = [
    ('v',str),
    ('start', str),
    ('final', str),
    ('n',int),
    ('goal',str),
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
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
hanoi = HanoiTowerProblem(ENV['v'])

# Start the game
TAc.print(LANG.render_feedback("start_config", f'# Start config: {start}'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("final_config", f'# Final config: {final}'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("format_moves", f'# Use format: N:FROM->TO and print "end" as last move. (example: "1:AB")'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("start_game", f'Start the Game'), "yellow", ["bold"])

# Get user moves
user_sol = list()
while True:
    move, = TALinput(str, sep="\n", regex="^\d{1,1000}:(A|B|C)(A|B|C)$", regex_explained="N:FT  where N=DISK, F=FROM and T=TO", exceptions={"end"}, TAc=TAc)
    if move == 'end':
        break
    user_sol.append(move)

# Get optimal moves
opt_sol = hanoi.getMovesList(start, final)


# PROCESS DATA
# Check if surely the user_sol is invalid
if (len(user_sol) < len(opt_sol)):
    TAc.print(LANG.render_feedback("sol-wrong-less", f'user_sol is wrong. len(user_sol) < len(corr_moves)'), "red", ["bold"])
    provide_feedback_and_exit(user_sol, opt_sol, user_sol_is_wrong=True)

# Check admissibility
info, error = hanoi.checkSol(user_sol, start, final)
if (info == 'move_not_valid'):
    TAc.print(LANG.render_feedback("move-not-valid", f'In user_sol move_not_valid: {error}'), "red", ["bold"])
    provide_feedback_and_exit(user_sol, opt_sol, user_sol_is_wrong=True)
elif (info == 'final_wrong'):
    TAc.print(LANG.render_feedback("final-wrong", f'In user_sol final_wrong: {error}'), "red", ["bold"])
    provide_feedback_and_exit(user_sol, opt_sol, user_sol_is_wrong=True)
else:
    TAc.print(LANG.render_feedback("sol-admissible", f'user_sol is admissible'), "green", ["bold"])

    # check if is a simple walk
    if (error != None):
        TAc.print(LANG.render_feedback("sol-not-simplewalk", f'user_sol is not a simple walk'), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback("sol-simplewalk", f'user_sol is a simple walk'), "green", ["bold"])

    # check optimality: sol admissible and len(user_sol) == len(opt_sol)
    if len(user_sol) != len(opt_sol):
        TAc.print(LANG.render_feedback("sol-not-opt", f'user_sol is not optimal'), "red", ["bold"])
        provide_feedback_and_exit(user_sol, opt_sol)
    else:
        TAc.print(LANG.render_feedback("sol-opt", f'user_sol is optimal'), "green", ["bold"])
        exit(0)
