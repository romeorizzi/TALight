#!/usr/bin/env python3
from os import POSIX_FADV_NOREUSE, RTLD_NOW
from sys import stderr, exit

import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import board2tok_utilities as utilities

# METADATA OF THIS TAL_SERVICE:
problem="board2tok"
service="trilly_server"
args_list = [
    ('k',int),
    ('left_out_cell_must_be_a_corner_cell',int),
    ('goal_min_calls_to_standard_moves',str),
    ('goal_min_calls_to_trilly',str),
    ('trilly_requests', str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
LANG.print_opening_msg()
    
# START CODING YOUR SERVICE: 

board = [['0' for _ in range(2**ENV['k'])] for _ in range(2**ENV['k'])]

def check_corner_cell(line):
    corner_cells = list()
    corner_cells.append((f'{line[1]}', f'{line[2]}'))
    corner_cells.append((f'{line[1]}', f'{2**line[0] + line[2] - 1}'))
    corner_cells.append((f'{2**line[0] + line[1] - 1}', f'{line[2]}'))
    corner_cells.append((f'{2**line[0] + line[1] - 1}', f'{2**line[0] + line[2] - 1}'))

    if (f'{line[3]}', f'{line[4]}') not in corner_cells:
        TAc.print(LANG.render_feedback('error-corner-cell', 'The left-out-cell you have chosen is not a corner cell.'), 'red', ['bold'])
        exit(0)

def check_values(line):
    if line[0] < 0 or line[1] < 0 or line[2] < 0 or line[3] < 0 or line[4] < 0:
        TAc.print(LANG.render_feedback('error-negative-number', 'One or more values that you have inserted are negative.'), 'red', ['bold'])
        exit(0)

    if line[0] >= ENV['k']:
        TAc.print(LANG.render_feedback('out-of-board', 'The sub-board dimension you have chosen is greater equal than the original board dimension.'), 'red', ['bold'])
        exit(0)
    if line[0] == 0:
        TAc.print(LANG.render_feedback('board-to-small', 'The sub-board dimension you have chosen is to small.'), 'red', ['bold'])
        exit(0)

    if line[1] >= 2**ENV['k']:
        TAc.print(LANG.render_feedback('row-coordinates-out-of-board', 'The row coordinates you have chosen are out of the original board dimension.'), 'red', ['bold'])
        exit(0)
    if line[1] >= 2**ENV['k'] - 1:
        TAc.print(LANG.render_feedback('rpw-sub-board-out-of-original', 'The row coordinates you have chosen are out of the original board.'), 'red', ['bold'])
        exit(0)

    if line[2] >= 2**ENV['k']:
        TAc.print(LANG.render_feedback('column-coordinates-out-of-board', 'The column coordinates you have chosen are out of the original board dimension.'), 'red', ['bold'])
        exit(0)
    if line[2] >= 2**ENV['k'] - 1:
        TAc.print(LANG.render_feedback('column-sub-board-out-of-board', 'The column coordinates you have chosen are out of the original board.'), 'red', ['bold'])
        exit(0)

    if line[3] > line[1] + 2**line[0] - 1 or line[3] < line[1]:
        TAc.print(LANG.render_feedback('row-hole-coordinates-exceeding-sub-board', 'The row hole coordinates you have chosen exceed the sub-board horizontally.'), 'red', ['bold'])
        exit(0)

    if line[4] > line[2] + 2**line[0] - 1 or line[4] < line[2]:
        TAc.print(LANG.render_feedback('column-hole-coordinates-exceeding-sub-board', 'The column hole coordinates you have chosen exceed the sub-board vertically.'), 'red', ['bold'])
        exit(0)

def check_is_empty(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column):
    for i in range(2**board_dimension):
        for j in range(2**board_dimension):
            if row_coordinates + i != hole_row or col_coordinates + j != hole_column:
                if board[row_coordinates + i][col_coordinates + j] != '0':
                    TAc.print(LANG.render_feedback('error-non-emty-sub-board', 'The sub-board you choose is not empty.'), 'red', ['bold'])
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

    if board_dimension <= 2 or ENV['trilly_requests'] == 'poses_only_the_starting_problem':
        trilly_moves(board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
        trilly_moves(board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
        trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
        trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
    if board_dimension > 2 and ENV['trilly_requests'] == 'might_pose_non_bigger_problems_in_reply':
        TAc.print(LANG.render_feedback('suggested-macro-moves', f'#macro {board_dimension - 1} {row_coordinates} {col_coordinates} {row_holes[0][0]} {col_holes[0][0]}'), 'green')
        TAc.print(LANG.render_feedback('suggested-macro-moves', f'#macro {board_dimension - 1} {row_coordinates} {col_coordinates + half_k} {row_holes[0][1]} {col_holes[0][1]}'), 'green')
        TAc.print(LANG.render_feedback('suggested-macro-moves', f'#macro {board_dimension - 1} {row_coordinates + half_k} {col_coordinates} {row_holes[1][0]} {col_holes[1][0]}'), 'green')
        TAc.print(LANG.render_feedback('suggested-macro-moves', f'#macro {board_dimension - 1} {row_coordinates + half_k} {col_coordinates + half_k} {row_holes[1][1]} {col_holes[1][1]}'), 'green')
    if board_dimension > 2 and ENV['trilly_requests'] == 'might_pose_smaller_problems_in_reply':
        # sceglie in modo casuale cosa fare
        if random.randint(0, 1):
            trilly_moves(board_dimension - 1, row_coordinates, col_coordinates, row_holes[0][0], col_holes[0][0])
        else:
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'#macro {board_dimension - 1} {row_coordinates} {col_coordinates} {row_holes[0][0]} {col_holes[0][0]}'), 'green')
        if random.randint(0, 1):
            trilly_moves(board_dimension - 1, row_coordinates, col_coordinates + half_k, row_holes[0][1], col_holes[0][1])
        else:
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'#macro {board_dimension - 1} {row_coordinates} {col_coordinates + half_k} {row_holes[0][1]} {col_holes[0][1]}'), 'green')
        if random.randint(0, 1):
            trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates, row_holes[1][0], col_holes[1][0])
        else:
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'#macro {board_dimension - 1} {row_coordinates + half_k} {col_coordinates} {row_holes[1][0]} {col_holes[1][0]}'), 'green')
        if random.randint(0, 1):
            trilly_moves(board_dimension - 1, row_coordinates + half_k, col_coordinates + half_k, row_holes[1][1], col_holes[1][1])
        else:
            TAc.print(LANG.render_feedback('suggested-macro-moves', f'#macro {board_dimension - 1} {row_coordinates + half_k} {col_coordinates + half_k} {row_holes[1][1]} {col_holes[1][1]}'), 'green')        

def trilly(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column):
    check_is_empty(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column)
    trilly_moves(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column)

count_standard_moves = 0
count_trilly_calls = 0

stopping_command_set="#end"
line = [0]
TAc.print(LANG.render_feedback('gimme-action', f"#? waiting for the action.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete."), 'yellow', ['bold'])

while line[0] != stopping_command_set:
    line = TALinput(int, num_tokens = 5, exceptions = stopping_command_set, TAc = TAc)
    if line[0] != stopping_command_set:
        if ENV['left_out_cell_must_be_a_corner_cell']:
            check_corner_cell(line)
        check_values(line)

        if line[0] == 1:
            count_standard_moves += 1
            TAc.print(LANG.render_feedback('standard-moves-call', 'You have chosen to call `standard_moves`.'), 'yellow', ['bold'])
            standard_move(line[1], line[2], line[3], line[4])
        if line[0] > 1:
            count_trilly_calls += 1
            TAc.print(LANG.render_feedback('trilly-call', 'You have chosen to call `trilly`.'), 'yellow', ['bold'])
            trilly(line[0], line[1], line[2], line[3], line[4])

if ENV['goal_min_calls_to_trilly'] == '4' and count_trilly_calls <= 4:
    TAc.print(LANG.render_feedback('trilly-goal-reached', 'You have respected the trilly calls goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_trilly'] == 'one_and_gain_three_calls_at_every_standard_move' and count_trilly_calls <= (1 + count_standard_moves * 3):
    TAc.print(LANG.render_feedback('trilly-goal-reached', 'You have respected the trilly calls goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_trilly'] == 'gain_three_calls_at_every_standard_move' and count_trilly_calls <= (count_standard_moves * 3):
    TAc.print(LANG.render_feedback('trilly-goal-reached', 'You have respected the trilly calls goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_trilly'] == 'any':
    TAc.print(LANG.render_feedback('trilly-goal-reached', 'You have respected the trilly calls goal you set.'), 'green', ['bold'])
else:
    TAc.print(LANG.render_feedback('trilly-goal-reached', 'You missed the trilly calls goal you set.'), 'red', ['bold'])

if ENV['goal_min_calls_to_standard_moves'] == 'k' and count_standard_moves <= ENV['k']:
    TAc.print(LANG.render_feedback('standard-goal-reached', 'You have respected the standard moves goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_standard_moves'] == '1' and count_standard_moves <= 1:
    TAc.print(LANG.render_feedback('standard-goal-reached', 'You have respected the standard moves goal you set.'), 'green', ['bold'])
elif ENV['goal_min_calls_to_standard_moves'] == 'any':
    TAc.print(LANG.render_feedback('standard-goal-reached', 'You have respected the standard moves goal you set.'), 'green', ['bold'])
else:
    TAc.print(LANG.render_feedback('standard-goal-missed', 'You missed the standard moves goal you set.'), 'red', ['bold'])

exit(0)