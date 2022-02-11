#!/usr/bin/env python3
from bot_lib import Bot

import chococroc_lib as cl

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    conf_string='It is your turn to move from conf ('
    if conf_string in line:
        index_end=line.find(')', len(conf_string))
        numbers=line[len(conf_string):index_end]
        s,d = map(int, numbers.split(',') )
        m,n = cl.computer_move(s,d)
        print(f"{m} {n}")
    if line=='You won!' or line=='You lost!':
        exit(0)
