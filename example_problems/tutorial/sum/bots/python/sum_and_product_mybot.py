#!/usr/bin/env python3
import math
from bot_lib import Bot

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    s,p = map(int, line.split() )
    Δ = int(math.sqrt(s*s-4*p))
    x1 = (s - Δ)//2
    x2 = s - x1
    BOT.print(f"{x1} {x2}")
