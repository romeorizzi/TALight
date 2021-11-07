#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors

import board2tok_utilities as utilities

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('k',int),
    ('r',int),
    ('c',int),
    ('dispel_first_rows_of_a_tiling',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
LANG.print_opening_msg()
    
# START CODING YOUR SERVICE: 
k=ENV['k']
r=ENV['r']
c=ENV['c']
dispel_first_rows_of_a_tiling=ENV['dispel_first_rows_of_a_tiling']

# a 2^kx2^k board always admits a tiling
TAc.print(LANG.render_feedback("admits-tiling", "The board admits a tiling."), "green", ["bold"])
if k==0:
    TAc.print(LANG.render_feedback("no-tile-to-insert", "There are no tiles to insert."), "red", ["bold"])
    exit(0)
if r > 2**k - 1 or r < 0:
    TAc.print(LANG.render_feedback("row-out-of-bound", "The empty cell row coordinate exceeds the board bounds."), "red", ["bold"])
    exit(0)
if c > 2**k - 1 or c < 0:
    TAc.print(LANG.render_feedback("col-out-of-bound", "The empty cell column coordinate exceeds the board bounds."), "red", ["bold"])
    exit(0)

utilities.tiling(0, (2**k) - 1, 0, (2**k) - 1, r, c)

dispel_first_rows_of_a_tiling = 2**k if dispel_first_rows_of_a_tiling > 2**k else dispel_first_rows_of_a_tiling

for i in range(dispel_first_rows_of_a_tiling):
    print(utilities.board[i][:2**k])
exit(0)
