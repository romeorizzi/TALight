#!/usr/bin/env python3
from bot_lib import Bot

import cypher_game_lib as cl

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    cur_number, = map(int,line.split())
    number=cl.computer_move(cur_number)
    print(f"{number}")
