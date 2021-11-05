#!/usr/bin/env python3
from sys import stderr, exit

import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('k',int),
    ('left_out_cell_must_be_a_corner_cell',int),
    ('goal_coverage', str),
    ('goal_min_calls_to_standard_moves',str),
    ('goal_min_calls_to_trilly',str),
    ('trilly_assertivity', str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
LANG.print_opening_msg()

# START CODING YOUR SERVICE: 

board = [['0' for _ in range(2**ENV['k'])] for _ in range(2**ENV['k'])]
count_empty_cells = 0

def check_corner_cell(line):
    h = line[0]
    if h == 0:
        h = 1
    corner_cells = list()
    corner_cells.append((f'{line[1]}', f'{line[2]}'))
    corner_cells.append((f'{line[1]}', f'{2**h + line[2] - 1}'))
    corner_cells.append((f'{2**h + line[1] - 1}', f'{line[2]}'))
    corner_cells.append((f'{2**h + line[1] - 1}', f'{2**h + line[2] - 1}'))

    if (f'{line[3]}', f'{line[4]}') not in corner_cells:
        TAc.print(LANG.render_feedback('error-corner-cell', '#ERROR: The left-out-cell you have chosen is not a corner cell.'), 'red', ['bold'])
        exit(0)

def check_values(line):
    if line[0] < 0 or line[1] < 0 or line[2] < 0 or line[3] < 0 or line[4] < 0:
        TAc.print(LANG.render_feedback('error-negative-number', '#ERROR: One or more values that you have inserted are negative.'), 'red', ['bold'])
        exit(0)

    h = line[0]
    if h == 0:
        h = 1
    if h >= ENV['k'] > 1:
        TAc.print(LANG.render_feedback('too-big-sub-board', '#ERROR: The sub-board dimension you have chosen is greater or equal than the original board dimension.'), 'red', ['bold'])
        exit(0)

    if line[1] >= 2**ENV['k']:
        TAc.print(LANG.render_feedback('row-coordinates-out-of-board', f'#ERROR: The row coordinate you have entered ({line[1]}) falls out of the original board.'), 'red', ['bold'])
        exit(0)
    if line[1] + 2**h > 2**ENV['k']:
        TAc.print(LANG.render_feedback('row-sub-board-out-of-original', '#ERROR: The row coordinates you have chosen are out of the original board.'), 'red', ['bold'])
        exit(0)

    if line[2] >= 2**ENV['k']:
        TAc.print(LANG.render_feedback('column-coordinates-out-of-board', f'#ERROR: The column coordinate you have entered ({line[2]}) falls out of the original board.'), 'red', ['bold'])
        exit(0)
    if line[2] + 2**h > 2**ENV['k']:
        TAc.print(LANG.render_feedback('column-sub-board-out-of-board', '#ERROR: The column coordinates you have chosen are out of the original board.'), 'red', ['bold'])
        exit(0)

    if line[3] > line[1] + 2**h - 1 or line[3] < line[1]:
        TAc.print(LANG.render_feedback('row-hole-coordinates-exceeding-sub-board', '#ERROR: Your row hole coordinate falls outside the sub-board.'), 'red', ['bold'])
        exit(0)

    if line[4] > line[2] + 2**h - 1 or line[4] < line[2]:
        TAc.print(LANG.render_feedback('column-hole-coordinates-exceeding-sub-board', '#ERROR: Your column hole coordinate falls outside the sub-board.'), 'red', ['bold'])
        exit(0)

def check_is_empty(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column):
    for i in range(2**board_dimension):
        for j in range(2**board_dimension):
            if row_coordinates + i != hole_row or col_coordinates + j != hole_column:
                if board[row_coordinates + i][col_coordinates + j] != '0':
                    TAc.print(LANG.render_feedback('error-non-emty-sub-board', '#ERROR: The sub-board you asked Trilly to fill up is not empty.'), 'red', ['bold'])
                    exit(0)

def standard_move(row_coordinates, col_coordinates, hole_row, hole_column):
    if hole_row - row_coordinates == 0 and hole_column - col_coordinates == 0:
        board[row_coordinates][col_coordinates + 1] = 'N'
        board[row_coordinates + 1][col_coordinates] = 'W'
        board[row_coordinates + 1][col_coordinates + 1] = '4'
    if hole_row - row_coordinates == 0 and hole_column - col_coordinates == 1:
        board[row_coordinates][col_coordinates] = 'N'
        board[row_coordinates + 1][col_coordinates] = '1'
        board[row_coordinates + 1][col_coordinates + 1] = 'E'
    if hole_row - row_coordinates == 1 and hole_column - col_coordinates == 0:
        board[row_coordinates][col_coordinates] = 'W'
        board[row_coordinates][col_coordinates + 1] = '3'
        board[row_coordinates + 1][col_coordinates + 1] = 'S'
    if hole_row - row_coordinates == 1 and hole_column - col_coordinates == 1:
        board[row_coordinates][col_coordinates] = '2'
        board[row_coordinates][col_coordinates + 1] = 'E'
        board[row_coordinates + 1][col_coordinates] = 'S'

def trilly_moves(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column):
    k = 2**board_dimension

    if k <= 1:
        return

    half_k = int(k / 2)

    row_holes = [['0' for i in range(2)] for j in range(2)]
    col_holes = [['0' for i in range(2)] for j in range(2)]
    row_holes[0][0] = row_coordinates + half_k - 1
    col_holes[0][0] = col_coordinates + half_k - 1
    row_holes[0][1] = row_coordinates + half_k - 1
    col_holes[0][1] = col_coordinates + half_k
    row_holes[1][0] = row_coordinates + half_k
    col_holes[1][0] = col_coordinates + half_k - 1
    row_holes[1][1] = row_coordinates + half_k
    col_holes[1][1] = col_coordinates + half_k

    if (hole_row < row_coordinates + half_k and hole_column < col_coordinates + half_k ):
        row_holes[0][0] = hole_row
        col_holes[0][0] = hole_column
        standard_move(row_coordinates + half_k - 1, col_coordinates + half_k - 1, row_coordinates + half_k - 1, col_coordinates + half_k - 1)
        move = f"1 {row_coordinates + half_k - 1} {col_coordinates + half_k - 1} {row_coordinates + half_k - 1} {col_coordinates + half_k - 1}"

    if (hole_row < row_coordinates + half_k and hole_column >= col_coordinates + half_k):
        row_holes[0][1] = hole_row
        col_holes[0][1] = hole_column
        standard_move(row_coordinates + half_k - 1, col_coordinates + half_k - 1, row_coordinates + half_k - 1, col_coordinates + half_k)
        move = f"1 {row_coordinates + half_k - 1} {col_coordinates + half_k - 1} {row_coordinates + half_k - 1} {col_coordinates + half_k}"

    if (hole_row >= row_coordinates + half_k and hole_column < col_coordinates + half_k ):
        row_holes[1][0] = hole_row
        col_holes[1][0] = hole_column
        standard_move(row_coordinates + half_k - 1, col_coordinates + half_k - 1, row_coordinates + half_k, col_coordinates + half_k -1)
        move = f"1 {row_coordinates + half_k - 1} {col_coordinates + half_k - 1} {row_coordinates + half_k} {col_coordinates + half_k - 1}"

    if (hole_row >= row_coordinates + half_k and hole_column >= col_coordinates + half_k):
        row_holes[1][1] = hole_row
        col_holes[1][1] = hole_column
        standard_move(row_coordinates + half_k - 1, col_coordinates + half_k - 1, row_coordinates + half_k, col_coordinates + half_k)
        move = f"1 {row_coordinates + half_k - 1} {col_coordinates + half_k - 1} {row_coordinates + half_k} {col_coordinates + half_k}"

    TAc.print(LANG.render_feedback('suggested-standard-move', f'{move}'), 'green')

    if board_dimension <= 2 or ENV['trilly_assertivity'] == 'plain_executor':
        trilly_moves(board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
        trilly_moves(board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
        trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
        trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
    if board_dimension > 2 and ENV['trilly_assertivity'] == 'might_pose_smaller_macromoves_in_reply':
        rnd = random.randint(0, 3)
        if rnd == 0:
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'macro {board_dimension - 1} {row_coordinates} {col_coordinates} {row_holes[0][0]} {col_holes[0][0]}'), 'green')
            trilly_moves(board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
            trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
            trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
        elif rnd == 1:
            trilly_moves(board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'macro {board_dimension - 1} {row_coordinates} {col_coordinates + half_k} {row_holes[0][1]} {col_holes[0][1]}'), 'green')
            trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
            trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
        elif rnd == 2:
            trilly_moves(board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
            trilly_moves(board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'macro {board_dimension - 1} {row_coordinates + half_k} {col_coordinates} {row_holes[1][0]} {col_holes[1][0]}'), 'green')
            trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
        else:
            trilly_moves(board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
            trilly_moves(board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
            trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'macro {board_dimension - 1} {row_coordinates + half_k} {col_coordinates + half_k} {row_holes[1][1]} {col_holes[1][1]}'), 'green')

def trilly(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column):
    check_is_empty(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column)
    trilly_moves(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column)

def check_coverage():
    global count_empty_cells
    line = ['0'] * 2**ENV['k']
    for r in range(2**ENV['k']):
        prev_line = line
        line = board[r]
        if line[0] in {'3','4','E'}: 
            TAc.print(LANG.render_feedback("left-margin", f"The first character of a line can not be a '{line[0]}' for otherwise its tromino exits the left border of your grid."), "red", ["bold"])
            exit(0)
        if line[2**ENV['k'] - 1] in {'1','2','W'}: 
            TAc.print(LANG.render_feedback("right-margin", f"The last character of a line can not be a '{line[2**ENV['k'] - 1]}' for otherwise its tromino exits the right border of your grid."), "red", ["bold"])
            exit(0)
        for j in range(2**ENV['k']):
            if line[j] == '0':
                count_empty_cells += 1
            if (line[j] in {'1','2'} and line[j + 1] != 'E') or \
            (j < 2**ENV['k'] - 1 and line[j + 1] == 'E' and line[j] not in {'1','2'}) or \
            (line[j] == 'W' and line[j + 1] not in {'3','4'}) or \
            (j < 2**ENV['k'] - 1 and line[j + 1] in {'3','4'} and line[j] != 'W'):
                TAc.print(LANG.render_feedback("inconsistent-tromino-row", f"You can not have a `{line[j + 1]}` character at the immidiate right of a `{line[j]}` character (see the characters in position {j} and {j + 1} of your line)."), "red", ["bold"])
                exit(0)
        if r == 0:
            for char in line:
                if char in {'1','4','S'}: 
                    TAc.print(LANG.render_feedback("top-margin", f"No character of the first (topmost) line can be a '{char}' for otherwise its tromino exits the top border of your grid."), "red", ["bold"])
                    exit(0)
        if r == 2**ENV['k'] - 1:
            for char in line:
                if char in {'2','3','N'}: 
                    TAc.print(LANG.render_feedback("bottom-margin", f"No character of the last (bottom) line can be a '{char}' for otherwise its tromino exits the bottom border of your grid."), "red", ["bold"])
                    exit(0)
        for j in range(2**ENV['k']):
            if (line[j] in {'1','4'} and prev_line[j] != 'N') or \
            (prev_line[j] == 'N' and line[j] not in {'1','4'}) or \
            (line[j] == 'S' and prev_line[j] not in {'2','3'}) or \
            (prev_line[j] in {'2','3'} and line[j] != 'S'):
                TAc.print(LANG.render_feedback("inconsistent-tromino-col", f"You can not have a `{prev_line[j]}` character just above a `{line[j]}` character (check the characters in column {j}, indexes starting from 0)."), "red", ["bold"])
                exit(0)

count_standard_moves = 0
count_trilly_calls = 0

stopping_command_set="#end"
line = [0]
TAc.print(LANG.render_feedback('gimme-action', f"# Waiting for the action.\n When you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete."), 'yellow', ['bold'])

while line[0] != stopping_command_set:
    line = TALinput(int, num_tokens = 5, exceptions = stopping_command_set, TAc = TAc)
    if line[0] != stopping_command_set:
        if ENV['left_out_cell_must_be_a_corner_cell']:
            check_corner_cell(line)
        check_values(line)

        if line[0] == 0:
            count_standard_moves += 1
            standard_move(line[1], line[2], line[3], line[4])
            TAc.print(LANG.render_feedback('standard-moves-call', f'# You have acted a `standard move` ({line}).'), 'yellow', ['bold'])
        if line[0] >= 1:
            count_trilly_calls += 1
            if random.randint(0, 1) and ENV['trilly_assertivity'] == 'might_bounch_your_macromoves_back_to_you':
                TAc.print(LANG.render_feedback('suggested-macro-moves', f'macro {line[0]} {line[1]} {line[2]} {line[3]} {line[4]}'), 'green')
            else:
                trilly(line[0], line[1], line[2], line[3], line[4])
            TAc.print(LANG.render_feedback('trilly-call', f'# You have called `trilly` ({line}).'), 'yellow', ['bold'])

# TODO: il tiling viene restituito su un file
# ora viene stampato altrimenti gli errori non hanno senso
for i in range(2**ENV['k']):
    print(board[i][:2**ENV['k']])

check_coverage()
tot_cells = 2**ENV['k']*2**ENV['k']
coverage = tot_cells - count_empty_cells

if ENV['goal_coverage'] == 'at_least_3' and coverage >= 3:
    TAc.print(LANG.render_feedback('coverage-goal-reached', '# You have respected the coverage goal you set.'), 'green', ['bold'])
elif ENV['goal_coverage'] == 'at_least_one_quarter' and coverage >= int(tot_cells/4):
    TAc.print(LANG.render_feedback('coverage-goal-reached', '# You have respected the coverage goal you set.'), 'green', ['bold'])
elif ENV['goal_coverage'] == 'at_least_half' and coverage >= int(tot_cells/2):
    TAc.print(LANG.render_feedback('coverage-goal-reached', '# You have respected the coverage goal you set.'), 'green', ['bold'])
elif ENV['goal_coverage'] == 'at_least_three_quarters' and coverage >= int(3*tot_cells/4):
    TAc.print(LANG.render_feedback('coverage-goal-reached', '# You have respected the coverage goal you set.'), 'green', ['bold'])
elif ENV['goal_coverage'] == 'all_exept_one' and coverage == tot_cells - 1:
    TAc.print(LANG.render_feedback('coverage-goal-reached', '# You have respected the coverage goal you set.'), 'green', ['bold'])
else:
    TAc.print(LANG.render_feedback('coverage-goal-reached', '# You missed the coverage goal you set.'), 'red', ['bold'])

if ENV['goal_min_calls_to_trilly'] == '4' and count_trilly_calls <= 4:
    TAc.print(LANG.render_feedback('trilly-goal-reached', '# You have respected the trilly calls goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_trilly'] == 'one_and_gain_three_calls_at_every_standard_move' and count_trilly_calls <= (1 + count_standard_moves * 3):
    TAc.print(LANG.render_feedback('trilly-goal-reached', '# You have respected the trilly calls goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_trilly'] == 'gain_three_calls_at_every_standard_move' and count_trilly_calls <= (count_standard_moves * 3):
    TAc.print(LANG.render_feedback('trilly-goal-reached', '# You have respected the trilly calls goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_trilly'] == 'any':
    TAc.print(LANG.render_feedback('trilly-goal-reached', '# You have respected the trilly calls goal you set.'), 'green', ['bold'])
else:
    TAc.print(LANG.render_feedback('trilly-goal-reached', '# You missed the trilly calls goal you set.'), 'red', ['bold'])

if ENV['goal_min_calls_to_standard_moves'] == 'k' and count_standard_moves <= ENV['k']:
    TAc.print(LANG.render_feedback('standard-goal-reached', '# You have respected the standard moves goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_standard_moves'] == '1' and count_standard_moves <= 1:
    TAc.print(LANG.render_feedback('standard-goal-reached', '# You have respected the standard moves goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_standard_moves'] == 'any':
    TAc.print(LANG.render_feedback('standard-goal-reached', '# You have respected the standard moves goal you set.'), 'green', ['bold'])
else:
    TAc.print(LANG.render_feedback('standard-goal-missed', '# You missed the standard moves goal you set.'), 'red', ['bold'])

exit(0)
