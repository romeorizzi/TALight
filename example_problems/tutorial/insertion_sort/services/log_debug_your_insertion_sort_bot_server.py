#!/usr/bin/env python3
from sys import exit
import re
import random
from itertools import zip_longest

import insert_sort_lib
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from sys import stdout, stderr, exit, argv

# METADATA OF THIS TAL_SERVICE:
problem = "insert_sort"
service = "log_debug_your_insertion_sort_bot_server"
args_list = [
    ('feedback', str),
    ('lang', str),
]


# ENV = Env(problem, service, args_list)
# TAc = TALcolors(ENV)
# LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# TODO: convertire tutto in versione TAlight
class DebugYourInsertSort:

    def __init__(self, input_arr, input_file, feedback):
        self.input_array = input_arr
        self.filename = input_file
        self.feedback = feedback

    @staticmethod
    def read_logs(filename):
        pattern = re.compile("^(#LOG_flush_tmp_buffer_on_pos [0-9]+)$|"
                             "^(#LOG_load_next_input_element_in_tmp_buffer (OK, got [0-9]+|NO MORE))$|"
                             "^(#LOG_clone_ele_in_pos [0-9]+ one_step_to_the_right)$|"
                             "^(#LOG_compare_what_in_pos [0-9]+ with_what_in_tmp_buffer [<>=])$|"
                             "^(#LOG_output_final_array ([0-9]+ )*[0-9])$")
        i = 1
        with open(filename, 'r') as f:
            for line in f.readlines():
                if re.match(pattern, line):
                    yield i, line[1:].strip()
                i += 1

    def check_if_insert_sort(self):
        try:
            insert_sort = insert_sort_lib.InsertSort(self.input_array)
            for e1, e2 in zip_longest(insert_sort.generate_log_when_sorting(), self.read_logs(self.filename)):
                try:
                    if e1 != e2[1] and self.feedback == "tell_whats_right_instead":
                        if "flush" in e1 and "flush" in e2[1]:
                            trail = f"Flush operation from buffer is right, but {e2[1][-1]} is not the right value. The value to be flushed should be:\n{e1}"
                        elif "load" in e1 and "load" in e2[1]:
                            if "OK" in e1 and "NO MORE" in e2[1]:
                                trail = f"Load of the next input element on buffer is right, but the array is still not empty. The right line should be:\n{e1}"
                            elif "NO MORE" in e1 and "OK" in e2[1]:
                                trail = f"Load of the next input element on buffer is right, but the array is empty. The right line should be:\n{e1}"
                            else:
                                trail = f"Load of the next input element in buffer is right, but the current buffer value is not right. The right line should be:\n{e1}"
                        elif "clone" in e1 and "clone" in e2[1]:
                            trail = f"Cloning operation is right, but you are cloning the wrong element. The right line should be:\n{e1} "
                        elif "compare" in e1 and "compare" in e2[1]:
                            if e1[24] != e2[1][24]:
                                trail = f"You are comparing the wrong array element to the buffer. The right line should be:\n{e1}"
                            else:
                                trail = f"Your comparison result is not right. The right line should be:\n{e1}"
                        elif "output" in e1 and "output" in e2[1]:
                            trail = f"Your final array is not right. The right line should be:\n{e1}"
                        else:
                            trail = f"This operation is not right. The right operation should be:\n{e1[1]}"

                        return f"Error in line {e2[0]}: {e2[1]}. \n" + trail

                    elif e1 != e2[1] and self.feedback == "just_signal_first_error":
                        return f"Error in line {e2[0]}: {e2[1]}."
                except TypeError:
                    return f"Error: EOF reached, which means your solution file is incomplete or empty. Next line should be:\n{e1}"
        except ValueError:
            return "Input not valid. Only integer numbers."

        return "Congrats, your solution is right."


if __name__ == "__main__":
    input_array = (list(map(int, argv[2:])))
    filename = argv[1]
    feedback = "tell_whats_right_instead"
    debug = DebugYourInsertSort(input_array, filename, feedback)
    result = debug.check_if_insert_sort()
    print(result)
