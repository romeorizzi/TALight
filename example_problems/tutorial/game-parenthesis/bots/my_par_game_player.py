#!/usr/bin/env python3
from bot_lib import Bot

import par_game_lib as pl

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    cur_formula, = map(str,line.split())
    formula=pl.computer_move(cur_formula)
    if formula=='':
        formula=')('
    print(f"{formula}")
