#!/usr/bin/env python3
from bot_lib import Bot

import chococroc_lib as cl

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    cur_m,cur_n,cur_nim = map(int,line.split())
    m,n,nim=cl.computer_decision_move(cur_m,cur_n,cur_nim)
    print(f"{m} {n} {nim}")
