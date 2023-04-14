#!/usr/bin/env python3
from bot_lib import Bot

import cypher_game_lib as cl

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    cur_number,cur_nim = map(int,line.split())
    cur_nim=int(cur_nim)
    number,nim=cl.computer_move_nim(cur_number,cur_nim)
    print(f"{number} {nim}")
