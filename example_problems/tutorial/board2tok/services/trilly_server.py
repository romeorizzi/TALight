#!/usr/bin/env python3
from sys import exit

import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('k',int),
    ('left_out_cell_must_be_a_corner_cell',bool),
    ('left_out_cell_row',str),
    ('left_out_cell_col',str),
    ('goal_coverage', str),
    ('goal_min_calls_to_standard_moves',str),
    ('goal_min_calls_to_trilly',str),
    ('trilly_assertivity', str),
    ('display_tiling', bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
LANG.print_opening_msg()

# START CODING YOUR SERVICE: 

board = [['0' for _ in range(2**ENV['k'])] for _ in range(2**ENV['k'])]
macromoves_challenge = True
macromove_line = [0]
stopping_command_set="#end"
count_standard_moves = 0
count_trilly_calls = 0

def choose_empty_cell():
    if ENV['left_out_cell_must_be_a_corner_cell']:
        row_empty_cell_coordinate = (2**ENV['k'] - 1) * random.randint(0, 1)
        col_empty_cell_coordinate = (2**ENV['k'] - 1) * random.randint(0, 1)
    else:
        row_empty_cell_coordinate = random.randint(0, 2**ENV['k'] - 1)
        col_empty_cell_coordinate = random.randint(0, 2**ENV['k'] - 1)
    return row_empty_cell_coordinate, col_empty_cell_coordinate

def check_values(line, sub_board_dimension, row_coordinate, col_coordinate, hole_row, hole_col):

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

    if line[0] >= sub_board_dimension:
        TAc.print(LANG.render_feedback('challenge-sub-board-dimension', '#ERROR: The sub-board dimension you have chosen is greater equal than the one of the challenge.'), 'red', ['bold'])
        exit(0)

    if line[1] >= 2**sub_board_dimension + row_coordinate:
        TAc.print(LANG.render_feedback('sub-board-out-of-challenge-row-dimension', '#ERROR: The row coordinates you have chosen are out of the challenge board dimension.'), 'red', ['bold'])
        exit(0)

    if line[2] >= 2**sub_board_dimension + col_coordinate:
        TAc.print(LANG.render_feedback('sub-board-out-of-challenge-col-dimension', '#ERROR: The column coordinates you have chosen are out of the challenge board dimension.'), 'red', ['bold'])
        exit(0)

    if line[1] <= hole_row < (line[1] + 2**h - 1) and line[2] <= hole_col < (line[2] + 2**h - 1):
        if hole_row != line[3]:
            TAc.print(LANG.render_feedback('row-empty-cell-covering', '#ERROR: Your row hole coordinate covers the orignal cell coordinate that you must leave empty.'), 'red', ['bold'])
            exit(0)
        if hole_col != line[4]:
            TAc.print(LANG.render_feedback('column-empty-cell-covering', '#ERROR: Your column hole coordinate covers the orignal cell coordinate that you must leave empty.'), 'red', ['bold'])
            exit(0)

def check_is_empty(line):
    for i in range(2**line[0]):
        for j in range(2**line[0]):
            if line[1] + i != line[3] or line[2] + j != line[4]:
                if board[line[1] + i][line[2] + j] != '0':
                    TAc.print(LANG.render_feedback('error-non-empty-sub-board', '#ERROR: The sub-board you asked to fill up is not empty.'), 'red', ['bold'])
                    exit(0)

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

def trilly_moves(tab, board_dimension, row_coordinates, col_coordinates, hole_row, hole_column):
    
    global macromoves_challenge
    global macromove_line
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

    TAc.print(LANG.render_feedback('suggested-standard-move', f'{tab}{move}'), 'green')

    if macromoves_challenge and board_dimension > 1 and ENV['trilly_assertivity'] == 'might_pose_smaller_macromoves_in_reply':
        macromoves_challenge = False
        rnd = random.randint(0, 3)
        if rnd == 0:
            macromove_line = [(board_dimension - 1), row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0]]
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'{tab}macro {board_dimension - 1} {row_coordinates} {col_coordinates} {row_holes[0][0]} {col_holes[0][0]}'), 'green', ['bold'])
            trilly_moves(tab, board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
            trilly_moves(tab, board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
            trilly_moves(tab, board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
        elif rnd == 1:
            macromove_line = [(board_dimension - 1), row_coordinates, (col_coordinates + half_k), row_holes[0][1], col_holes[0][1]]
            trilly_moves(tab, board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'{tab}macro {board_dimension - 1} {row_coordinates} {col_coordinates + half_k} {row_holes[0][1]} {col_holes[0][1]}'), 'green', ['bold'])
            trilly_moves(tab, board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
            trilly_moves(tab, board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
        elif rnd == 2:
            macromove_line = [(board_dimension - 1), (row_coordinates + half_k), col_coordinates, row_holes[1][0], col_holes[1][0]]
            trilly_moves(tab, board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
            trilly_moves(tab, board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'{tab}macro {board_dimension - 1} {row_coordinates + half_k} {col_coordinates} {row_holes[1][0]} {col_holes[1][0]}'), 'green', ['bold'])
            trilly_moves(tab, board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
        else:
            macromove_line = [(board_dimension - 1), (row_coordinates + half_k), (col_coordinates + half_k), row_holes[1][1], col_holes[1][1]]
            trilly_moves(tab, board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
            trilly_moves(tab, board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
            trilly_moves(tab, board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'{tab}macro {board_dimension - 1} {row_coordinates + half_k} {col_coordinates + half_k} {row_holes[1][1]} {col_holes[1][1]}'), 'green', ['bold'])
    else:
        trilly_moves(tab, board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
        trilly_moves(tab, board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
        trilly_moves(tab, board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
        trilly_moves(tab, board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])

def check_coverage(row_starting_point, col_starting_point, board_dimension):
    count_empty_cells = 0
    line = ['0'] * 2**ENV['k']
    for r in range(row_starting_point, 2**board_dimension + row_starting_point):
        prev_line = line
        line = board[r]
        if line[0] in {'3','4','E'}: 
            TAc.print(LANG.render_feedback("left-margin", f"The first character of a line can not be a '{line[0]}' for otherwise its tromino exits the left border of your grid."), "red", ["bold"])
            exit(0)
        if line[2**ENV['k'] - 1] in {'1','2','W'}: 
            TAc.print(LANG.render_feedback("right-margin", f"The last character of a line can not be a '{line[2**ENV['k'] - 1]}' for otherwise its tromino exits the right border of your grid."), "red", ["bold"])
            exit(0)
        for j in range(col_starting_point, 2**board_dimension + col_starting_point):
            if line[j] == '0':
                count_empty_cells += 1
            if (line[j] in {'1','2'} and line[j + 1] != 'E') or \
            (j < 2**board_dimension - 1 and line[j + 1] == 'E' and line[j] not in {'1','2'}) or \
            (line[j] == 'W' and line[j + 1] not in {'3','4'}) or \
            (j < 2**board_dimension - 1 and line[j + 1] in {'3','4'} and line[j] != 'W'):
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
        for j in range(col_starting_point, 2**board_dimension + col_starting_point):
            if (line[j] in {'1','4'} and prev_line[j] not in {'0','N'}) or \
            (prev_line[j] == 'N' and line[j] not in {'1','4'}) or \
            (line[j] == 'S' and prev_line[j] not in {'0','2','3'}) or \
            (prev_line[j] in {'2','3'} and line[j] != 'S'):
                TAc.print(LANG.render_feedback("inconsistent-tromino-col", f"You can not have a `{prev_line[j]}` character just above a `{line[j]}` character (check the characters in column {j}, indexes starting from 0)."), "red", ["bold"])
                exit(0)
    return count_empty_cells

def sub_board_moves(tab, sub_board_dimension, row_coordintate, col_coordinate, hole_row, hole_col, line=[0]):
    global count_standard_moves
    global count_trilly_calls
    global macromoves_challenge
    global macromove_line

    while line[0] != stopping_command_set:
        
        TAc.print(LANG.render_feedback('sub-board-information', f"{tab}# You are working on the sub-board of dimension: {sub_board_dimension}, you must leave the cell ({hole_row}, {hole_col}) empty.\n{tab}When you have completed the sub-board, write the stopping command '#end'."), 'yellow')

        line = TALinput(int, num_tokens = 5, exceptions = stopping_command_set, TAc = TAc)
        if line[0] != stopping_command_set:
            check_values(line, sub_board_dimension, row_coordintate, col_coordinate, hole_row, hole_col)
            check_is_empty(line)
            if ENV['left_out_cell_must_be_a_corner_cell']:
                check_corner_cell(line)

            if line[0] == 0:
                count_standard_moves += 1
                standard_move(line[1], line[2], line[3], line[4])
                TAc.print(LANG.render_feedback('standard-moves-call', f'{tab}# You have acted a `standard move` ({line}).'), 'white')
            if line[0] >= 1:
                count_trilly_calls += 1
                if random.randint(0, 1) and ENV['trilly_assertivity'] == 'might_bounch_your_macromoves_back_to_you':
                    TAc.print(LANG.render_feedback('suggested-macro-moves', f'{tab}macro {line[0]} {line[1]} {line[2]} {line[3]} {line[4]}'), 'green', ['bold'])
                    macromoves_challenge = False
                    macromove_line = line
                else:
                    trilly_moves(tab, line[0], line[1], line[2], line[3], line[4])
                TAc.print(LANG.render_feedback('trilly-call', f'{tab}# You have called `trilly` ({line}).'), 'white')
            if not macromoves_challenge:
                macromoves_challenge = True
                sub_board_moves(f"{tab}\t", macromove_line[0], macromove_line[1], macromove_line[2], macromove_line[3], macromove_line[4])
        else:
            if len(tab) > 0:
                TAc.print(LANG.render_feedback('sub-board-exiting', f"{tab}# You are exiting the current sub-board of dimension: {sub_board_dimension}."), 'blue')
                count_empty_cells = check_coverage(row_coordintate, col_coordinate, sub_board_dimension)
                TAc.print(LANG.render_feedback('sub-boar-left-out-cells', f"{tab}# You have left out uncovered {count_empty_cells} of the current sub-board cells (This is an intermediate value)."), 'blue')

if ENV['left_out_cell_row'] == "service_to_choose" and ENV['left_out_cell_col'] == "service_to_choose":
    row_empty_cell_coordinate, col_empty_cell_coordinate = choose_empty_cell()
elif ENV['left_out_cell_row'] == "service_to_choose" or ENV['left_out_cell_col'] == "service_to_choose":
    TAc.print(LANG.render_feedback('error-partial-spec-empty-cell', f'#ERROR: The argument values \'left_out_cell_row\'= {ENV["left_out_cell_row"]}  and  \'left_out_cell_col\'= {ENV["left_out_cell_col"]}  are NOT compatible! Eithere both or none should be left to the default value "service_to_choose".'), 'red', ['bold'])
    exit(0)
else:
    row_empty_cell_coordinate = int(ENV['left_out_cell_row'])
    col_empty_cell_coordinate = int(ENV['left_out_cell_col'])
    check_corner_cell([ENV['k'], 0, 0, row_empty_cell_coordinate, col_empty_cell_coordinate])


sub_board_moves("", ENV['k'], 0, 0, row_empty_cell_coordinate, col_empty_cell_coordinate)

if ENV['display_tiling']:
    for i in range(2**ENV['k']):
        TAc.print(LANG.render_feedback('printing-sub-board', board[i][:2**ENV['k']]), 'white')
# uncomment if TA_receive_files_bot.py works with TAlinput
# else:
#     from bot_interface import service_server_to_send_files

#     dict_of_files = { f"tiling.txt": '\n'.join(' '.join(map(str, board[i][:2**ENV['k']])) for i in range(2**ENV['k'])).encode('ascii') }
#     service_server_to_send_files(dict_of_files)          

count_empty_cells = check_coverage(0, 0, ENV['k'])
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
