#!/usr/bin/env python3
import math
from bot_lib import Bot

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    n = int(line)
    BOT.print(f"{n} 0")
