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


ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
def read_logs():
    pattern = re.compile("(#LOG_flush_tmp_buffer_on_pos [0-9]+)|"
                         "(#LOG_load_next_input_element_in_tmp_buffer (OK|NO MORE))|"
                         "(#LOG_clone_ele_in_pos [0-9]+ one_step_to_the_right)|"
                         "(#LOG_compare_what_in_pos [0-9]+ with_what_in_tmp_buffer [<>=])|"
                         "(#LOG_output_final_array ([0-9]+))")
    i = 1
    with open(argv[1], 'r') as f:
        for line in f.readlines():
            if re.match(pattern, line):
                yield i, line[1:].replace("\n", "").rstrip().lstrip()
            i += 1


if ENV['feedback'] == 'only_signal_first_error':
    try:
        input_array = list(map(int, argv[2:]))
        insert_sort = insert_sort_lib.InsertSort(input_array)
        for e1, e2 in zip_longest(insert_sort.generate_log_when_sorting(), read_logs()):
            try:
                if e1 != e2[1]:
                    TAc.print(f"Error in line {e2[0]}: your log was {e2[1]}, should be {e1}.\n")
                    exit(1)
            except TypeError:
                TAc.print(f"Error: EOF reached, next log was {e1}")
                exit(1)
    except ValueError:
        TAc.print("Input not valid. Only integer numbers.")
        exit(1)




"""
NON SI BADI ALLE COSE SOTTO, POTREBBERO SERVIRE MA VERRANNO PROBABILMENTE ELIMINATE.
    log_array = [""]
    
    
    def input_array_format(n: int, array: str):
        arraylista = array.lstrip(" ").split(" ")
        if len(arraylista) != n:
            return print("#Error: " + str(n) + " is not the right length, should be " + str(len(arraylista)))
    
        return print("Your array: " + str(arraylista))
    
    
    def insert_sort(array_inp: list):
        log_array.append("LOG_input_array " + str(array_inp))
        for i in range(1, len(array_inp)):
            j = i - 1
            log_array.append("LOG_memory_load_from_pos " + str(j))
            key = array_inp[i]
            while j >= 0 and array_inp[j] > key:
                cond = [True if j >= 0 and array_inp[j] > key else False]
                log_array.append("LOG_compare_what_in_pos" + str(j) + " less_than_what_in_memory " + str(cond))
                array_inp[j + 1] = array_inp[j]
                log_array.append("LOG_copy_from_pos " + str(j) + " to_pos " + str(j+1))
                j -= 1
            array_inp[j + 1] = key
            log_array.append("LOG_memory_write_on_pos " + str(j+1))
    
        log_array.append("LOG_output_array " + str(array_inp))
        return array_inp
    
    
    print(f"#Waiting for your n-dimensional array.\n#Format: [n,array]. Each value of the array must be separated by "
          f"spaces. "
          " Only integer numbers.")
    
    array = input()
    pattern = re.compile(r"^[0-9]+,[\s]*[0-9]+(\s+[0-9]+)*$")
    if not pattern.match(str(array)):
        print("#INVALID INPUT FORMAT.\n#Format: [n, array]. Each value of the array must be separated by spaces. Only "
              "integer numbers.")
        exit()
    
    arraylist = array.split(",")
    input_array_format(int(arraylist[0]), arraylist[1])
    print("Now, you can use ONLY those primitives: "
          "LOG_input_array <n> <input_array_of_length_n>"
          "LOG_memory_load_from_pos <i>"
          "LOG_memory_write_on_pos <i>"
          "LOG_copy_from_pos <i> to_pos <j>"
          "LOG_compare_what_in_pos <i> less_than_what_in_memory <outcome>"
          "LOG_output_array <n> <output_array_of_length_n>"
"""
