#!/usr/bin/env python3
import math
from bot_lib import Bot

BOT = Bot(report_inputs=True,reprint_outputs=True)

while True:
    line = BOT.input()
    n = int(line)
    print(f"{n} 0")
