#!/usr/bin/env python3
from bot_lib import Bot

import par_game_lib as pl

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    cur_formula,cur_nim = map(str,line.split())
    cur_nim=int(cur_nim)
    formula,nim=pl.computer_decision_move(cur_formula,cur_nim)
    if formula=='':
        formula=')('
    print(f"{formula} {nim}")