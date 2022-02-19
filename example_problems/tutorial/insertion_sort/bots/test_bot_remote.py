#!/usr/bin/env python3
from sys import argv
from bot_lib import Bot
import random

BOT = Bot(report_inputs=True,reprint_outputs=True)

def compare(pos_cmp):
    print(f"CMD_COMPARE_ELE_IN_TMP_BUFFER_WITH_ELE_IN_POS {pos_cmp}") 
    cmp = BOT.input()
    return True if cmp == '<' else False # true <, False >=

def load_next_input_element_in_tmp_buffer():
    print("CMD_LOAD_NEXT_INPUT_ELEMENT_IN_TMP_BUFFER")
    return BOT.input()    

n_ordered = 0
while load_next_input_element_in_tmp_buffer() != '0':
    pos_cmp = n_ordered - 1
    if(pos_cmp >= 0):
        while pos_cmp >= 0 and compare(pos_cmp):
            print(f"CMD_CLONE_TO_ITS_RIGHT_ELE_IN_POS {pos_cmp}")
            pos_cmp -= 1
    print(f"CMD_FLUSH_TMP_BUFFER_ELE_IN_POS {pos_cmp+1}")
    n_ordered += 1
print("CMD_OUTPUT_FINAL_SORTED_ARRAY")
