#!/usr/bin/env python3
import math
from bot_lib import Bot

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    n = int(line)
    print(f"{n//2} {(n+1)//2}")
