#!/usr/bin/env python3
import math
from bot_lib import Bot

BOT = Bot(report_inputs=True,reprint_outputs=True)

while True:
    line = BOT.input()
    s,d = map(int, line.split() )
    x1 = (s + d) // 2
    x2 = (s - d) // 2
    print(f"{x1} {x2}")
