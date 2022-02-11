#!/usr/bin/env python3
from bot_lib import Bot

import chococroc_lib as cl

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    cur_m,cur_n = map(int,line.split())
    m,n=cl.computer_move(cur_m,cur_n)
    print(f"{m} {n}")