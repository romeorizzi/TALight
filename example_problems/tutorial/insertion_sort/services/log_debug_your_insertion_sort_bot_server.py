#!/usr/bin/env python3
from sys import exit
from time import sleep

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import insert_sort_lib

# METADATA OF THIS TAL_SERVICE:
problem = "insert_sort"
service = "log_debug_your_insertion_sort_bot_server"
args_list = [
    ('interactive', bool),
    ('feedback', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    
# START CODING YOUR SERVICE:

insertion_sort = insert_sort_lib.InsertionSort([])
ins_sort_ref_iterator = insertion_sort.generate_log_while_sorting()
finished = False
time_for_next_load_or_end = True
while not finished:
    if ENV['interactive']:
        print()
    line = input()
    while line[:4] != "LOG_":
        line = input()
    if "LOG_load_next_input_element_in_tmp_buffer" in line:
        if not time_for_next_load_or_end:
            TAc.print(LANG.render_feedback("wrong-place-for-loading-a-new-ele", f'No! Right now I was not expecting the loading of a new element in the tmp_buffer since the tmp_buffer is NOT empty! It currently contains the integer {new_ele}.'), "yellow", ["bold"])
            exit(0)
        new_ele = int(line.split("(got ")[1].split(")")[0])
        insertion_sort.append_to_input_stream(new_ele)
        time_for_next_load_or_end = False
    if "LOG_flush_tmp_buffer_on_pos" in line:
        time_for_next_load_or_end = True
    if "LOG_output_final_sorted_array" in line:
        if not time_for_next_load_or_end:
            TAc.print(LANG.render_feedback("wrong-place-for-final-output", f'No! Right now I was not expecting the output of the final array since an element introduced in the tmp_buffer (the integer {new_ele}) is still there!'), "yellow", ["bold"])
            exit(0)
        else:
            finished = True
    std_line = next(ins_sort_ref_iterator)
    if std_line == line:
        TAc.OK()
        TAc.print(LANG.render_feedback("line-of-log-ok", f'Your log is fully coherent till here ({std_line})'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("line-of-log-wrong", f'No! Here, the InsertionSort algorithm once implemented on our InsertionSortMachine would have produced the following line of log "{std_line}"'), "yellow", ["bold"])
        exit(0)        

TAc.print(LANG.render_feedback("final-congrats",'CONGRATS! The log sent to the service id fully coherent with the execution of InsertionSort. \u2714'), "yellow", ["bold"])
exit(0)
