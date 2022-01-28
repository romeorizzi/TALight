#!/usr/bin/env python3
import sys
from time import sleep
from bot_lib import Bot


BOT = Bot(report_inputs=True,reprint_outputs=True)

# Getting array
print("CMD_GET_DIM")

array_len = int(BOT.input())

swap = True
right_pos = 1
while swap:
    swap = False
    for i in range(array_len-1):
        print(f"CMD_COMPARE_CONSEC_ELEM {i}")
        swap = (BOT.input() == 'True')
        if(swap):
            print(f"CMD_SWAP_CONSEC_ELEM {i}")
            swap = True
    right_pos += 1

print("CMD_FINISHED")

sleep(1)