#!/usr/bin/env python3
from os import POSIX_FADV_NOREUSE
from re import L
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import board2tok_utilities as utilities

# METADATA OF THIS TAL_SERVICE:
problem="board2tok"
service="verify_tiling_server"
args_list = [
    ('k',int),
    ('r',int),
    ('c',int),
    ('silent', bool),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
LANG.print_opening_msg()
    
# START CODING YOUR SERVICE: 
k=ENV['k']
r=ENV['r']
c=ENV['c']
board = [['0' for _ in range(1024)] for _ in range(1024)]

if r > 2**k - 1 or r < 0:
    TAc.print(LANG.render_feedback("row-out-of-bound", "The empty cell row coordinate exceeds the board bounds."), "red", ["bold"])
    exit(0)
if c > 2**k - 1 or c < 0:
    TAc.print(LANG.render_feedback("col-out-of-bound", "The empty cell column coordinate exceeds the board bounds."), "red", ["bold"])
    exit(0)

TAc.print(LANG.render_feedback("notice-instructions", "You can insert the board tiling line by line or provide the service with a file containing the board tiling."), "yellow", ["bold"])

line = [0]
for i in range(2**k):
    line = TALinput(
        str,
        num_tokens=1,
        TAc=TAc
    )
    board[i] = list(line[0])

for i in range(2**k):
    for j in range(2**k):
        if i == r and j == c and board[i][j] != '0':
            TAc.print(LANG.render_feedback("error-no-empty-cell", f"You have not left empty the correct cell ({r},{c})."), "red", ["bold"])
            exit(0)
        if board[i][j] == '0' and (i != r or j != c):
            TAc.print(LANG.render_feedback("error-wrong-empty-cell", "You have left empty the wrong cell."), "red", ["bold"])
            exit(0)
        if board[i][j] == '1' and board[i][j+1] != 'E':
            TAc.print(LANG.render_feedback("error-1-right-est-tile", "You have inserted a wrong tile. The tile with corner '1' must have 'E' on the right."), "red", ["bold"])
            exit(0)
        if board[i][j] == '2' and board[i][j + 1] != 'E':
            TAc.print(LANG.render_feedback("error-2-right-est-tile", "You have inserted a wrong tile. The tile with corner '2' must have 'E' on the right."), "red", ["bold"])
            exit(0)
        if board[i][j] == '3' and board[i][j - 1] != 'W':
            TAc.print(LANG.render_feedback("error-3-left-west-tile", "You have inserted a wrong tile. The tile with corner '3' must have 'W' on the left."), "red", ["bold"])
            exit(0)
        if board[i][j] == '4' and board[i][j - 1] != 'W':
            TAc.print(LANG.render_feedback("error-4-left-west-tile", "You have inserted a wrong tile. The tile with corner '4' must have 'W' on the left."), "red", ["bold"])
            exit(0)
        if board[i][j] == '1' and board[i - 1][j] != 'N':
            TAc.print(LANG.render_feedback("error-1-up-north-tile", "You have inserted a wrong tile. The tile with corner '1' must have 'N' on the top."), "red", ["bold"])
            exit(0)
        if board[i][j] == '2' and board[i + 1][j] != 'S':
            TAc.print(LANG.render_feedback("error-2-down-south-tile", "You have inserted a wrong tile. The tile with corner '2' must have 'S' on the bottom."), "red", ["bold"])
            exit(0)
        if board[i][j] == '3' and board[i + 1][j] != 'S':
            TAc.print(LANG.render_feedback("error-3-down-south-tile", "You have inserted a wrong tile. The tile with corner '3' must have 'S' on the bottom."), "red", ["bold"])
            exit(0)
        if board[i][j] == '4' and board[i - 1][j] != 'N':
            TAc.print(LANG.render_feedback("error-4-up-north-tile", "You have inserted a wrong tile. The tile with corner '4' must have 'N' on the top."), "red", ["bold"])
            exit(0)
        if board[i][j] == 'N' and board[i + 1][j] != '1' and board[i + 1][j] != '4':
            TAc.print(LANG.render_feedback("error-north-tile", "You have inserted a wrong tile. The tile with on the top 'N' must have '1' or '4' on the bottom."), "red", ["bold"])
            exit(0)
        if board[i][j] == 'S' and board[i - 1][j] != '2' and board[i - 1][j] != '3':
            TAc.print(LANG.render_feedback("error-south-tile", "You have inserted a wrong tile. The tile with on the bottom 'S' must have '2' or '3' on the top."), "red", ["bottom"])
            exit(0)
        if board[i][j] == 'E' and board[i][j - 1] != '1' and board[i][j - 1] != '2':
            TAc.print(LANG.render_feedback("error-est-tile", "You have inserted a wrong tile. The tile with on the right 'E' must have '1' or '2' on the left."), "red", ["bold"])
            exit(0)
        if board[i][j] == 'W' and board[i][j + 1] != '3' and board[i][j + 1] != '4':
            TAc.print(LANG.render_feedback("error-west-tile", "You have inserted a wrong tile. The tile with on the left 'W' must have '3' or '4' on the right."), "red", ["bold"])
            exit(0)

TAc.print(LANG.render_feedback("correct-tiling", "Well done! You have inserted a correct tiling."), "green", ["bold"])

exit(0)
