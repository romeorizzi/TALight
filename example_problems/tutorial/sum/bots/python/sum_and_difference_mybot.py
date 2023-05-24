#!/usr/bin/env python3
import math
from bot_lib import Bot

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    s,d = map(int, line.split() )
    x1 = (s + d) // 2
    x2 = (s - d) // 2
    BOT.print(f"{x1} {x2}")
