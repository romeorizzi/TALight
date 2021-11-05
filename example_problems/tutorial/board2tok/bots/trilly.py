#!/usr/bin/env python3

import random

k = 4
left_out_cell_must_be_a_corner_cell = 1
number_of_total_moves_before_end = 100
macro_moves = []
board = [['0' for _ in range(2**k)] for _ in range(2**k)]

def check_is_empty(board_dimension, row_coordinates, col_coordinates, hole_row, hole_column):
    for i in range(2**board_dimension):
        for j in range(2**board_dimension):
            if row_coordinates + i != hole_row or col_coordinates + j != hole_column:
                if board[row_coordinates + i][col_coordinates + j] != '0':
                    return True
    return False

def make_move(row_coordinates, col_coordinates, hole_row, hole_column):
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

def set_move():
    sub_board_dimension = random.randint(1, k - 1)
    row_coordinates = random.randrange(0, 2**k - 1)
    if row_coordinates + 2**sub_board_dimension > 2**k - 1:
        row_coordinates -= row_coordinates % 2**sub_board_dimension
    column_coordinates = random.randrange(0, 2**k - 1)
    if column_coordinates + 2**sub_board_dimension > 2**k - 1:
        column_coordinates -= column_coordinates % 2**sub_board_dimension
    if left_out_cell_must_be_a_corner_cell:
        hole_row = (2**sub_board_dimension - 1) * random.randint(0, 1) + row_coordinates
        hole_column = (2**sub_board_dimension - 1) * random.randint(0, 1) + column_coordinates
    else:
        hole_row = random.randint(0, 2**sub_board_dimension - 1) + row_coordinates
        hole_column = random.randint(0, 2**sub_board_dimension - 1) + column_coordinates
    if sub_board_dimension == 1:
        sub_board_dimension = random.randint(0,1)
    return sub_board_dimension, row_coordinates, column_coordinates, hole_row, hole_column

def start_algo():
    global number_of_total_moves_before_end
    while number_of_total_moves_before_end > 0:
        empty = True
        check_empty = (2**k - 1) * (2**k - 1)
        if len(macro_moves) == 0:
            while empty == True:
                sub_board_dimension, row_coordinates, column_coordinates, hole_row, hole_column = set_move()
                empty = check_is_empty(sub_board_dimension, row_coordinates, column_coordinates, hole_row, hole_column)
                check_empty -= 1
                if check_empty <= 0:
                    print('#end')
                    spoon = input().strip()
                    while spoon[:len("# ")] == "# ":
                        spoon = input().strip()
                    exit(0)
            move = f'{sub_board_dimension} {row_coordinates} {column_coordinates} {hole_row} {hole_column}'
            make_move(row_coordinates, column_coordinates, hole_row, hole_column)
        else:
            move_id = random.randint(0, len(macro_moves) - 1)
            move = macro_moves[move_id]
            macro_moves.pop(move_id)
        print(move)
        if sub_board_dimension > 1:
            spoon = input().strip()
            while spoon[:len("# ")] != "# ":
                make_move(int(spoon.split()[1]), int(spoon.split()[2]), int(spoon.split()[3]), int(spoon.split()[4]))
                if spoon[:len('macro')] == 'macro':
                    macro_moves.append(spoon[len('macro '):])
                spoon = input().strip()
        else:
            spoon = input().strip()
        number_of_total_moves_before_end -= 1

    print('#end')
    spoon = input().strip()
    while spoon[:len("# ")] == "# ":
        spoon = input().strip()

spoon = input().strip()
while spoon[:len("# ")] == "# ":
    spoon = input().strip()
start_algo()
