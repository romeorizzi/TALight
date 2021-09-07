#!/usr/bin/env python3
from os import RTLD_NOW
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
    ('only_corner_cell',int),
    ('goal_min_calls_to_place_tile',str),
    ('goal_min_calls_to_trilly',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
LANG.print_opening_msg()
    
# START CODING YOUR SERVICE: 

your_board = [['0' for _ in range(1024)] for _ in range(1024)]
k=ENV['k']
exceptions={'end'}

def set_empty_cell():    
    if ENV['only_corner_cell'] == 0:
        r = random.randint(0, 2**k)
        c = random.randint(0, 2**k)
    else:
        r = (2**k - 1) * random.randint(0, 1)
        c = (2**k - 1) * random.randint(0, 1)
    return r, c

r, c = set_empty_cell()
TAc.print(LANG.render_feedback("notice-hole-coordinates", f"The position of the empty cell is: {r}, {c}"), "yellow", ["bold"])

reference_board = utilities.compute_tiling(0, 2**k, 0, 2**k, r, c)

def check_tile(r, c, border_cells):
    if border_cells[0] == reference_board[r][c]:
        pass
    else:
        return False
    if border_cells[1] == 'N' and reference_board[r - 1][c] == 'N':
        pass
    elif border_cells[1] == 'S' and reference_board[r + 1][c] == 'S':
        pass
    else:
        return False
    if border_cells[2] == 'W' and reference_board[r][c - 1] == 'W':
        pass
    elif border_cells[2] == 'E' and reference_board[r][c + 1] == 'E':
        pass
    else:
        return False
    return True

def out_of_borders(k, r, c, border_cells):
    if r < 0:
        return False
    if c < 0:
        return False
    if r > 2**k:
        return False
    if c > 2**k:
        return False
    if border_cells[1] == 'N' and r - 1 < 0:
        return False
    if border_cells[1] == 'S' and r + 1 > 2**k:
        return False
    if border_cells[2] == 'W' and c - 1 < 0:
        return False
    if border_cells[2] == 'E' and c + 1 > 2**k:
        return False
    return True

def trilly_tile(hole_row, hole_col, length):
    utilities.tiling(0, length - 1, 0, length - 1, hole_row, hole_col)
    for i in range(length):
        print(utilities.board[i][:length])

def fill_your_board(corner_row, corner_col, borders):
    your_board[corner_row][corner_col] = borders[0]
    if borders[1] == 'N':
        your_board[corner_row - 1][corner_col] = 'N'
    else:
        your_board[corner_row + 1][corner_col] = 'S'
    if borders[2] == 'E':
        your_board[corner_row][corner_col + 1] = 'E'
    else:
        your_board[corner_row][corner_col - 1] = 'W'

def print_your_board():
    for i in range(2**k):
        print(your_board[i][:2**k])

def place_tile():
    for i in range(2**k):
        for j in range(2**k):
            if i != r or j != c:
                if your_board[i][j] == '0':
                    your_board[i][j] = reference_board[i][j]
                    if your_board[i][j] == 'N':
                        your_board[i + 1][j] = reference_board[i + 1][j]
                        if your_board[i + 1][j] == '1':
                            your_board[i + 1][j + 1] = reference_board[i + 1][j + 1]
                        else:
                            your_board[i + 1][j - 1] = reference_board[i + 1][j - 1]
                    else:
                        your_board[i][j + 1] = reference_board[i][j + 1]
                        if your_board[i][j + 1] == '3':
                            your_board[i + 1][j + 1] = reference_board[i + 1][j + 1]
                        else:
                            your_board[i + 1][j] = reference_board[i + 1][j]
                    return

    
if ENV['goal_min_calls_to_trilly'] == 'one_and_gain_three_calls_at_every_placed_tile':
    allowed_trilly_calls = 1
    incrementable = True
elif ENV['goal_min_calls_to_trilly'] == 'gain_three_calls_at_every_placed_tile':
    allowed_trilly_calls = 0
    incrementable = True
elif ENV['goal_min_calls_to_trilly'] == '4':
    allowed_trilly_calls = 4
    incrementable = False
else: 
    allowed_trilly_calls = 1

if ENV['goal_min_calls_to_place_tile'] == 'k':
    allowed_place_tile_calls = k
elif ENV['goal_min_calls_to_place_tile'] == '1':
    allowed_place_tile_calls = 1
else:
    allowed_place_tile_calls = 1

print("You have four possibilities: ")
print("\t 1. enter a line with 'trilly', the board dimension and the empty cell. This option calls the fairy (if you have the possibility).")
print("\t 2. enter one or more lines with the tiles (one tile per line), you have to specify che corner cell of the tile followed by the characters of the border cells.")
print("\t 3. enter a line with 'place_tile'. This option inserts a random tile for you (if you have the possibility).")
print("\t 4. enter a line with 'print_your_board'. This option print your board with the inserted tiles.")
print("Examples:")
print("\t0,0;2SE")
print("\ttrilly;1;0,0")
print("\tplace_tile")
print("\tprint_your_board")
print("When you have finished, you have to insert a new line with 'end'\n")

line = [0]
while line[0] not in(exceptions):
    line = TALinput(
        str,
        num_tokens=1,
        exceptions = exceptions,
        regex="([0-9]+,[0-9]+);[0-4]([nN]|[sS])([eE]|[wW])|(trilly|TRILLY);[0-9]+;[0-9]+,[0-9]+|(place_tile|PLACE_TILE)|(print_your_board|PRINT_YOUR_BOARD)",
        regex_explained="two numbers (row and col index) separated by a ',' followed by a ';' and the specific tile. Otherwise 'trilly' or another function. (it is not case sensitive)",
        TAc=TAc
    )
    if line[0] not in(exceptions):
        line = line[0].split(';')                   
        if line[0].lower() == 'trilly' and allowed_trilly_calls > 0:
            new_k = int(line[1])
            if new_k >= k:
                TAc.print(LANG.render_feedback("error-size-board-trilly", "You are not allowed to call trilly the fairy on a board of the same dimension of the given one."), "red", ["bold"])

            if ENV['goal_min_calls_to_trilly'] != 'any':
                allowed_trilly_calls -= 1   

            new_r = int(line[2].split(',')[0])
            new_c = int(line[2].split(',')[1])
            trilly_tile(new_r, new_c, 2**(new_k))

        elif line[0].lower() == 'trilly' and allowed_trilly_calls <= 0:
            TAc.print(LANG.render_feedback("error-zero-trilly-calls", "You are not allowed to call trilly the fairy."), "red", ["bold"])

        elif line[0].lower() == 'place_tile' and allowed_place_tile_calls > 0:
            if ENV['goal_min_calls_to_place_tile'] != 'any':
                allowed_place_tile_calls -=1

            place_tile()

        elif line[0].lower() == 'place_tile' and allowed_place_tile_calls <= 0:
            TAc.print(LANG.render_feedback("error-zero-place_tile-calls", "You are not allowed to call place_tile."), "red", ["bold"])

        elif line[0].lower() == 'print_your_board':
            print_your_board()

        else:
            r_corner_cell = int(line[0].split(',')[0])
            c_corner_cell = int(line[0].split(',')[1])
            border_cells = line[1].upper()
            
            if r_corner_cell == r and c_corner_cell == c:
                TAc.print(LANG.render_feedback("error-empty-cell-covered", "You have covered the cell that must remain empty."), "red", ["bold"])
            elif not utilities.out_of_borders(k, r_corner_cell, c_corner_cell, border_cells):
                TAc.print(LANG.render_feedback("error-out-of-borders", "You have place a tile out of the borders."), "red", ["bold"])
            elif not utilities.check_tile(r_corner_cell, c_corner_cell, border_cells):
                TAc.print(LANG.render_feedback("error-wrong-tile", "You have place a tile in the wrong place."), "red", ["bold"])
            else:
                fill_your_board(r_corner_cell,c_corner_cell, border_cells)
                if incrementable:
                    allowed_trilly_calls += 3
                    TAc.print(LANG.render_feedback("correct-tile", f"Weel done! You have gained three trilly calls. Now you have {allowed_trilly_calls} trilly calls"), "green", ["bold"])
                else:
                    TAc.print(LANG.render_feedback("correct-tile", f"Weel done!"), "green", ["bold"])


exit(0)
