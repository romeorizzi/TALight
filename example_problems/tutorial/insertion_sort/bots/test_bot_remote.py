#!/usr/bin/env python3
from sys import argv
from bot_lib import Bot


BOT = Bot(report_inputs=True,reprint_outputs=True)

# Asking dimensions
print("CMD_GET_DIM")
N = int(BOT.input())

n_ordered = 0
while n_ordered < N:
    print("CMD_LOAD_NEXT_INPUT_ELEMENT_IN_TMP_BUFFER")
    pos_cmp = n_ordered - 1
    if(pos_cmp >= 0):
        print(f"CMD_COMPARE_WHAT_IN_TMP_BUFFER_WITH_WHAT_IN_POS {pos_cmp}") 
        cmp = BOT.input()
        cmp = True if cmp == '<' else False # true <, False >=
        while pos_cmp >= 0 and cmp:
            print(f"CMD_CLONE_TO_ITS_RIGHT_ELE_IN_POS {pos_cmp}")
            pos_cmp -= 1
    print(f"CMD_FLUSH_TMP_BUFFER_ELE_IN_POS {pos_cmp+1}")
    n_ordered += 1
print("CMD_FINISHED")
