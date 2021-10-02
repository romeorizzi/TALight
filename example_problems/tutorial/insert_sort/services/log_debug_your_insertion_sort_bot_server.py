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


#ENV = Env(problem, service, args_list)
#TAc = TALcolors(ENV)
#LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
def read_logs():
    pattern = re.compile("^(#LOG_flush_tmp_buffer_on_pos [0-9]+)$|"
                         "^(#LOG_load_next_input_element_in_tmp_buffer (OK, got [0-9]+|NO MORE))$|"
                         "^(#LOG_clone_ele_in_pos [0-9]+ one_step_to_the_right)$|"
                         "^(#LOG_compare_what_in_pos [0-9]+ with_what_in_tmp_buffer [<>=])$|"
                         "^(#LOG_output_final_array ([0-9]+))$")
    i = 1
    with open(argv[1], 'r') as f:
        for line in f.readlines():
            if re.match(pattern, line):
                yield i, line[1:].strip()
            i += 1

try:
    input_array = list(map(int, argv[2:]))
    insert_sort = insert_sort_lib.InsertSort(input_array)
    for e1, e2 in zip_longest(insert_sort.generate_log_when_sorting(), read_logs()):
        try:
            # if feedback = default or stop at first error
            #if e1 != e2[1]:
            #    print(f"Error in line {e2[0]}: {e2[1]}.")
            # elif feedback = tell what's right instead
            if e1 != e2[1]:
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
                    if e1[-1] == e2[1][-1]:
                        trail = f"You are comparing the wrong element to the buffer. The right line should be:\n{e1}"
                    else:
                        trail = f"The comparison is right, but the result or the array value is not. The right line should be:\n{e1}"
                elif "output" in e1 and "output" in e2[1]:
                    trail = f"Your final array is not well sorted. The right line should be:\n{e1}"
                else:
                    trail = f"This operation is not right. The right operation should be:\n{e1[1]}"

                print(f"Error in line {e2[0]}: {e2[1]}. \n" + trail)
                exit(1)
        except TypeError:
            print(f"Error: EOF reached, which means your solution file is incomplete or empty.")
            exit(1)
except ValueError:
    print("Input not valid. Only integer numbers.")
    exit(1)

print("Congrats, your solution is right.")


"""
NON SI BADI ALLE COSE SOTTO, POTREBBERO SERVIRE MA VERRANNO PROBABILMENTE ELIMINATE.
    log_array = [""]
    
    
    def input_array_format(n: int, array: str):
        arraylista = array.lstrip(" ").split(" ")
        if len(arraylista) != n:
            return print("#Error: " + str(n) + " is not the right length, should be " + str(len(arraylista)))
    
        return print("Your array: " + str(arraylista))   
    
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
