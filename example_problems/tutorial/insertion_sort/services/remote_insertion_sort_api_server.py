#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from sys import stdout, stderr, exit, argv

from insert_sort_machine_lib import InsertionSortMachine, AbstractMachineOperatingError
from insert_sort_lib import InsertionSort_machine_plus_algo
import random

# METADATA OF THIS TAL_SERVICE:
problem = "insert_sort"
service = "remote_insertion_sort_api"
args_list = [
    ('feedback', str),
    ('lang', str),
    ('goal', str),
    ('interactive', bool)
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

def input_cmd():
    line = input()
    while line[:4] != "CMD_":
        line = input()
    return line


max_value = 30
max_array = 20

# Generating array
length = random.randint(1, max_array)
array = [random.randrange(1, max_value, 1) for i in range(length)]
insertion_sort = InsertionSort_machine_plus_algo([], log_on_console=False)
ins_sort_ref_iterator = insertion_sort.generate_log_while_sorting()

print(array, file=stderr)

# 1. Asking length
line = input_cmd()

if "CMD_GET_DIM" not in line:
    TAc.print(LANG.render_feedback("no-array-input-first", f'No! Right now I was expecting you to ask the length of the array.'), "yellow", ["bold"])
    exit(0)
else:
    print(len(array))

# Next, applying the sorting algorithm
time_for_next_load_or_end = True
finished = False
i = 0
try:
    while not finished:
        line = input_cmd()
        print(line, file=stderr)

        if("CMD_COMPARE_WHAT_IN_TMP_BUFFER_WITH_WHAT_IN_POS") in line:
            cmp = insertion_sort.compare_ele_in_tmp_buffer_with_ele_in_pos(int(line[-1]))
            cmp = '<' if cmp == True else '>=' # true <, False >=
            print(cmp)

        if "CMD_LOAD_NEXT_INPUT_ELEMENT_IN_TMP_BUFFER" in line:
            if not time_for_next_load_or_end:
                print(f"! porca merda", file=stderr)
                TAc.print(LANG.render_feedback("wrong-place-for-loading-a-new-ele", f'No! Right now I was not expecting the loading of a new element in the tmp_buffer since the tmp_buffer is NOT empty! It currently contains the integer {new_ele}.'), "yellow", ["bold"])
                exit(0)
            
            if(i > len(array)): # no other elements
                print(0)
            else:
                new_ele = array[i]
                i += 1

                insertion_sort.append_to_input_stream(new_ele)
                time_for_next_load_or_end = False
        if "CMD_FLUSH_TMP_BUFFER_ELE_IN_POS" in line:
            time_for_next_load_or_end = True

        if "CMD_FINISHED" in line:
            if not time_for_next_load_or_end:
                TAc.print(LANG.render_feedback("wrong-place-for-final-output", f'No! Right now I was not expecting the output of the final array since an element introduced in the tmp_buffer (the integer {new_ele}) is still there!'), "yellow", ["bold"])
                exit(0)
            else:
                finished = True
        
        std_line = next(ins_sort_ref_iterator).upper().split(' (')[0]
        std_line = std_line.replace("COMPARE_ELE_", "COMPARE_WHAT_").replace("WITH_ELE_IN","WITH_WHAT_IN")
        
        '''
        if(std_line[3:] == line[3:]):
            TAc.OK()
            TAc.print(LANG.render_feedback("line-of-log-ok", f'Your log is fully coherent till here ({std_line})'), "yellow", ["bold"])
        else:
            TAc.print(LANG.render_feedback("line-of-log-wrong", f'No! Here, the InsertionSort algorithm once implemented on our InsertionSortMachine would have produced the following line of log "{std_line}"'), "yellow", ["bold"])
            exit(0)
        '''
        if(std_line[3:] != line[3:]):
            TAc.print(LANG.render_feedback("line-of-log-wrong", f'No! Here, the InsertionSort algorithm once implemented on our InsertionSortMachine would have produced the following line of log "{std_line}"'), "yellow", ["bold"])
            exit(0)

except AbstractMachineOperatingError as inst:
    err_code, err_msg = inst.args
    TAc.print(LANG.render_feedback(err_code, f'No! Error in operating the InsertionSort Abstract Machine: {err_msg}'), "red", ["bold"])
    exit(0)

TAc.print(LANG.render_feedback("final-congrats",'CONGRATS! The log sent to the service id fully coherent with the execution of InsertionSort. \u2714'), "yellow", ["bold"])
exit(0)
