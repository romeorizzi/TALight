#!/usr/bin/env python3

from sys import argv


macro_moves = []
moves = []

def chose_move(board_dimension, first_row, first_col, hole_row, hole_col):
    k = 2**board_dimension
    new_moves = []

    if k <= 1:
        return

    half_k = int(k / 2)

    row_holes = [['0' for i in range(2)] for j in range(2)]
    col_holes = [['0' for i in range(2)] for j in range(2)]
    row_holes[0][0] = first_row + half_k - 1
    col_holes[0][0] = first_col + half_k - 1
    row_holes[0][1] = first_row + half_k - 1
    col_holes[0][1] = first_col + half_k
    row_holes[1][0] = first_row + half_k
    col_holes[1][0] = first_col + half_k - 1
    row_holes[1][1] = first_row + half_k
    col_holes[1][1] = first_col + half_k

    if (hole_row < first_row + half_k and hole_col < first_col + half_k ):
        row_holes[0][0] = hole_row
        col_holes[0][0] = hole_col
        new_moves.insert(0,(1, first_row + half_k - 1, first_col + half_k - 1, first_row + half_k - 1, first_col + half_k - 1))

    if (hole_row < first_row + half_k and hole_col >= first_col + half_k):
        row_holes[0][1] = hole_row
        col_holes[0][1] = hole_col
        new_moves.insert(0,(1, first_row + half_k - 1, first_col + half_k - 1, first_row + half_k - 1, first_col + half_k))

    if (hole_row >= first_row + half_k and hole_col < first_col + half_k ):
        row_holes[1][0] = hole_row
        col_holes[1][0] = hole_col
        new_moves.insert(0,(1, first_row + half_k - 1, first_col + half_k - 1, first_row + half_k, first_col + half_k -1))

    if (hole_row >= first_row + half_k and hole_col >= first_col + half_k):
        row_holes[1][1] = hole_row
        col_holes[1][1] = hole_col
        new_moves.insert(0,(1, first_row + half_k - 1, first_col + half_k - 1, first_row + half_k, first_col + half_k))

    new_moves.insert(0,(board_dimension - 1, first_row, first_col, row_holes[0][0], col_holes[0][0]))
    new_moves.insert(0,(board_dimension - 1, first_row, first_col + half_k, row_holes[0][1], col_holes[0][1]))
    new_moves.insert(0,(board_dimension - 1, first_row + half_k, first_col, row_holes[1][0], col_holes[1][0]))
    new_moves.insert(0,(board_dimension - 1, first_row + half_k, first_col + half_k, row_holes[1][1], col_holes[1][1]))
    moves.insert(0, new_moves)

def start_algo():
    do_end = False
    chose_move(int(arguments.get('k')), 0, 0, int(arguments.get('row_hole')), int(arguments.get('col_hole')))
    while len(moves) > 0:
        move = moves[0][0]
        print(f'{move[0]} {move[1]} {move[2]} {move[3]} {move[4]}')
        moves[0].pop(0)
        if len(moves[0]) == 0:
            moves.pop(0)
            do_end = True
        spoon = input().strip()
        while not spoon.startswith("# "):
            if spoon.startswith("macro"):
                macro_moves.insert(0,spoon[len("macro"):].split())
            spoon = input().strip()
        while spoon.startswith("# "):
            spoon = input().strip()
        if len(macro_moves) > 0:
            if int(macro_moves[0][0]) - 1 == 0:
                moves.insert(0,[(0, int(macro_moves[0][1]), int(macro_moves[0][2]), int(macro_moves[0][3]), int(macro_moves[0][4]))])
            else:
                chose_move(int(macro_moves[0][0]), int(macro_moves[0][1]), int(macro_moves[0][2]), int(macro_moves[0][3]), int(macro_moves[0][4]))
            macro_moves.pop(0)
        if do_end:
            print('#end')
            spoon = input().strip()
            while spoon.startswith("# "):
                spoon = input().strip()
            do_end = False

    print("#end")
    spoon = input().strip()
    while spoon.startswith("# "):
        spoon = input().strip()

if len(argv) > 0:
    arguments = { var.split("=")[0] : var.split("=")[1] for var in argv[1:] }
spoon = input().strip()
while spoon.startswith("# "):
    if len(argv) == 1:
        if spoon.startswith("#  with arguments:"):
            variables = spoon[len("#  with arguments: "):spoon.find(", ISATTY")].replace("(i.e., False)", "").replace("(i.e., True)", "").split(", ")
            arguments = { var.split("=")[0] : var.split("=")[1] for var in variables }
    if spoon.endswith(") empty."):
        hole_coordinates = spoon.split("(")[-1].split(")")[0].split(", ")
        arguments['row_hole'] = hole_coordinates[0]
        arguments['col_hole'] = hole_coordinates[1]
    spoon = input().strip()
start_algo()
