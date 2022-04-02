#!/usr/bin/env python3
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from insertion_sort_lib import InsertionSort_machine_plus_algo
from insertion_sort_machine_lib import AbstractMachineOperatingError

# METADATA OF THIS TAL_SERVICE:
problem = "insertion_sort"
service = "log_debug_your_insertion_sort_bot_server"
args_list = [
    ('interactive', bool),
    ('feedback', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    
# START CODING YOUR SERVICE:

insertion_sort = InsertionSort_machine_plus_algo([], log_on_console=False)
ins_sort_ref_iterator = insertion_sort.generate_log_while_sorting()
finished = False
time_for_next_load_or_end = True
try:
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
        if "LOG_flush_tmp_buffer_ele_in_pos" in line:
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
except AbstractMachineOperatingError as inst:
    err_code, err_msg = inst.args
    TAc.print(LANG.render_feedback(err_code, f'No! Error in operating the InsertionSort Abstract Machine: {err_msg}'), "red", ["bold"])
    exit(0)

TAc.print(LANG.render_feedback("final-congrats",'CONGRATS! The log sent to the service id fully coherent with the execution of InsertionSort. \u2714'), "yellow", ["bold"])

TAc.Finished(only_term_signal=True)
exit(0)
